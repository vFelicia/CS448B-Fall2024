################################################################################
# This python file, csv_from_playlist.py uses the YouTube API to compile a csv file
# containing a list of video metadata for a given
# YouTube playlist.
################################################################################
# Run this to generate the csv file video_metadata.csv (or other name of choice)
################################################################################

"""
This Python script uses the YouTube API to compile a text file containing a list of video titles and URLs from a given YouTube playlist. The script takes three inputs:
1. playlist_id: The id of the YouTube playlist.
2. playlist_name: The name of the YouTube playlist.
3, API Key: The API key for accessing the YouTube Data API.

Dependencies:
- Google API Client Library for Python (`googleapiclient`)
- `time` module for adding delays between API requests
- `html` module for unescaping HTML entities
- `sys` module for accessing command-line arguments

Outputs:
- A text file containing a list of video titles and URLs (input file for yt_api_transcript_helper_3.py). Each two-row pair is separated by a tab.

Process:
1. Parse command-line arguments to extract the username and API key.
2. Call the `get_my_channel_id` function to retrieve the channel ID associated with the provided username.
3. Call the `get_channel_videos` function to fetch videos associated with the channel ID using the YouTube API.
4. Call the `export_videos_list_to_txt` function to export the list of videos to a text file.

Usage:
- See controller.py for usage or run independently as follows:
- Run the script from the command line with the appropriate command-line arguments:
  `python yt_api_videos_list_from_channel.py -<username> -<API_KEY>`
- Example usage: `python yt_api_videos_list_from_channel.py -RandomChannel -API_KEY284028`
"""

import os
# import csv
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import isodate
import requests
from tqdm import tqdm
import playlist_transcript_helper
import playlist_controller
import re

# API_KEY = "AIzaSyCe8NA-YF6fObjYjUr8nKFX0ZFycl39fWo"
# FILE_PATH = 'playlist_video_metadata.csv'  #Change "playlist" to something informative about the playlist

class PlaylistNotFoundError(Exception):
    pass

def format_duration(duration):
    # Convert duration to total seconds
    total_seconds = int(duration.total_seconds())
    
    # Calculate days, hours, minutes, and seconds
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format the duration string based on the values
    if days > 0:
        return f"{days}:{hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
    elif hours > 0:
        return f"{hours}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
    else:
        return f"{minutes}:{str(seconds).zfill(2)}"

def get_video_details(video_id, api_key, title_counter):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    if response["items"]:
        item = response["items"][0]
        duration = isodate.parse_duration(item["contentDetails"]["duration"])
        title = item["snippet"]["title"]
        clean_title = playlist_transcript_helper.clean_filename(title.strip())

        # Check if the clean_title already exists in the title_counter for the channel
        if clean_title in title_counter:
            # Increment the counter
            title_counter[clean_title] += 1
            transcript_filename = f"{clean_title}_{title_counter[clean_title]}.txt"
        else:
            # Initialize the counter
            title_counter[clean_title] = 1
            transcript_filename = f"{clean_title}.txt"

        details = {
            "channel_name": item["snippet"]["channelTitle"],
            "video_title": title,
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "publish_date": item["snippet"]["publishedAt"][:10],
            "video_length": format_duration(duration),
            "views": item["statistics"].get("viewCount", 0),
            "likes": item["statistics"].get("likeCount", 0),
            "comments": item["statistics"].get("commentCount", 0),
            "transcript_filename": transcript_filename,
        }
        return details
    else:
        return None

def get_playlist_videos(playlist_id, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)
    videos = []
    next_page_token = None
    total_videos = 0

    # First, get the total number of videos in the playlist for the progress bar
    request = youtube.playlists().list(
        part="contentDetails",
        id=playlist_id
    )
    response = request.execute()
    if response["items"]:
        total_videos = response["items"][0]["contentDetails"]["itemCount"]
    
    title_counter = {}

    with tqdm(total=total_videos, desc="Collecting video details") as pbar:
        while True:
            try:
                request = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()

                for item in response["items"]:
                    video_id = item["snippet"]["resourceId"]["videoId"]
                    video_details = get_video_details(video_id, api_key, title_counter)
                    #  if video_details: #and has_transcript_boolean(video_id, API_KEY):
                    videos.append(video_details)
                    pbar.update(1)

                next_page_token = response.get("nextPageToken")
                if next_page_token is None:
                    break
            except HttpError as e:
                print(f"An error occurred: {e}")
                break

    return videos

# def has_transcript_boolean(video_id, api_key):
#     youtube = build("youtube", "v3", developerKey=api_key)
#     try:
#         captions = youtube.captions().list(part="snippet", videoId=video_id).execute()
#         if 'items' in captions:
#             return True
#         else:
#             return False
#     except HttpError as e:
#         # print(f"Error fetching captions for video ID {video_id}: {e}")
#         return False

def export_videos_list_to_csv(videos, playlist_name, file_path):
    write_header = not os.path.exists(file_path)
    fieldnames = ["channel_name", "video_title", "video_url", "publish_date", 
                  "video_length", "views", "likes", "comments", "transcript_filename"]#,"has_transcript"]

    if os.path.exists(file_path):
        print(f"The filepath already exists. skipping channel.")
        return
    else:
        df = pd.DataFrame(columns=fieldnames)

    df = df[df["channel_name"] != playlist_name]
    new_videos_df = pd.DataFrame(videos)
    df = pd.concat([df, new_videos_df], ignore_index=True)
    df.drop_duplicates(subset=['video_url'], inplace=True)  
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"\nVideo list exported to {file_path}\n")

def get_playlist_id(url):
    # Regular expression to match the playlist ID from the URL
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid playlist URL")
    
def get_playlist_name(playlist_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={playlist_id}&key={api_key}"
    response = requests.get(url).json()
    
    if response["items"]:
        item = response["items"][0]
        playlist_name = item["snippet"]["title"]
        return playlist_name
    return None

def build_rows(url, api_key):
    try:
        # Extract playlist ID from the URL
        playlist_id = get_playlist_id(url)
        global playlist_name
        playlist_name = get_playlist_name(playlist_id, api_key)
        global FILE_PATH 
        FILE_PATH = playlist_name + '_metadata.csv'
    
        # Check if FILE_PATH already exists
        if os.path.exists(FILE_PATH):
            playlist_controller.metadata_dupes += 1
            print(f"\nSkipping {playlist_name}, metadata file already exists.\n")
            return
        
        print("\n")
        videos = get_playlist_videos(playlist_id, api_key)
        export_videos_list_to_csv(videos, playlist_name, FILE_PATH)
    except PlaylistNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()