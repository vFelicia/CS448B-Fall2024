# ################################################################################
# ################################################################################

# """
# This Python script retrieves trancripts with timecodes in MM:SS format for YouTube videos specified in the input text file.

# Dependencies:
# - Google API Client Library for Python (`googleapiclient`)
# - YouTube Transcript/Subtitle API (`youtube-transcript-api`)
# - `re` module for text manipulation
# - `os` module for operating system interactions

# Outputs:
# - Transcripts for each video, saved in separate text files. Each transcript is compiled in a new folder, titled according to the relevant channel or playlist.
# - (If a transcript is unavailable for a video, a placeholder file indicating the unavailability is created.)

# Process:
# 1. Call the `read_input_file` function to extract video titles and URLs from the input file.
# 2. Retrieve transcripts for each video using the YouTube API.
# 3. Call the `seconds_to_minutes` function to get timecodes in MM:SS format.
# 2. Call `clean_filename` to clean the title for use in the filename.
# 3. Save the cleaned transcripts in separate text files.
# 4. Print status messages indicating which videos were transcribed successfully and which ones had unavailable transcripts.

# Usage:
# - Make sure you have run yt_api_videos_list_from_playlist or yt_api_videos_list_from_channel to generate the input file in the proper format.
# - Set your YouTube API key in the script's API_KEY variable.
# - Run the script from the command line with the appropriate command-line arguments:
#   `python <script_name>.py -<input_file_path>`
# - Example usage: `python yt_api_transcript_helper.py -CodeBytes_videos_list.txt`
# """

import os
import pandas as pd
import re
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from tqdm import tqdm
import csv_from_playlist
import playlist_controller

def clean_transcript(caption_response):
    if caption_response:
        text = re.sub(r"<.*?>", "", caption_response)  # Remove XML tags
        text = re.sub(r"\n{2,}", "\n", text)  # Remove extra newlines
        text = re.sub(r"\n", " ", text)  # Replace newlines with spaces
        return text.strip()
    else:
        return ""

def clean_filename(filename):
    filename = filename.lower()
    filename = re.sub(r'[^a-z0-9]', '', filename)
    return filename

def seconds_to_minutes_seconds(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes):02}:{int(seconds):02}"

def get_timestamped_transcript(transcript):
    return "\n".join([f"{seconds_to_minutes_seconds(t['start'])} - {t['text']}" for t in transcript])

def get_cleaned_transcript(transcript):
    # Remove timestamps
    transcript = re.sub(r'\d{1,4}:\d{2}\s-\s', '', transcript)  
    # Remove specific tags
    transcript = transcript.replace('[Music]', '').replace('[Applause]', '')  
    # Remove non-text items like dashes and colons
    transcript = re.sub(r'[-:]', '', transcript)  
    # Remove extra spaces and newlines
    transcript = re.sub(r'\s+', ' ', transcript)  
    return transcript.strip()

# def has_transcript_boolean(directory_path):
#     """
#     Checks the contents of text files in the specified directory.
#     Returns False if any text file contains "Transcript unavailable",
#     otherwise returns True.
#     """
#     for filename in os.listdir(directory_path):
#         file_path = os.path.join(directory_path, filename)
#         if os.path.isfile(file_path) and file_path.endswith('.txt'):
#             with open(file_path, 'r') as file:
#                 content = file.read().strip()
#                 if content == "Transcript unavailable":
#                     return False

def transcribe_videos():
    global new_videos 
    new_videos = 0
    try:
        video_data = pd.read_csv(csv_from_playlist.FILE_PATH)
    except FileNotFoundError:
        print(f"Error: The file {csv_from_playlist.FILE_PATH} was not found.")
        return

    unique_channels = video_data["channel_name"].unique()
    unique_videos = set(video_data["video_url"])  # Set of unique video URLs to avoid duplicates
    total_transcribed = []
    total_not_transcribed = []
    channel_name = unique_channels[0]
    # for channel_name in unique_channels:
        
    # Create a directory for each unique channel if it doesn't already exist
    channel_dir = f"{channel_name.lower()}_transcripts"
    
    if os.path.exists(channel_dir):
        playlist_controller.skipped_channels += 1
        # print(f"Skipping {channel_name}, transcripts already exist.\n")
        return

    os.makedirs(channel_dir, exist_ok=True)

    # Filter videos for the current channel
    channel_videos = video_data[video_data["channel_name"] == channel_name]

    unavailable_videos = []
    transcribed_videos = []

    total_videos = len(channel_videos)
    with tqdm(total=total_videos, desc=f"Processing playlist: {channel_name}", unit="video") as pbar:
        for index, row in channel_videos.iterrows():
            video_title = row["video_title"]
            video_url = row["video_url"]
            video_id = video_url.split("v=")[-1]

            # Skip duplicates
            if video_url not in unique_videos:
                # print(f"\nSkipping duplicate video: {video_title}")
                continue

            clean_title = clean_filename(video_title.strip())
            
            output_file_path = os.path.join(channel_dir, f"{clean_title}.txt")
            ## duplicate name handling
            counter = 1
            while os.path.exists(output_file_path):
                counter += 1
                output_file_path = os.path.join(channel_dir, f"{clean_title}_{counter}.txt")
            #
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                transcript_text = get_timestamped_transcript(transcript)

                with open(output_file_path, "w") as file:
                    file.write(transcript_text)
                
                transcribed_videos.append(clean_title)
                total_transcribed.append(clean_title)
                unique_videos.remove(video_url)
                # print(f"Transcribed video: {video_title} | Saved to {output_file_path}")
            except Exception as e:
                # unavailable_file_path = os.path.join(channel_dir, f"{clean_title}_transcript_unavailable.txt")
                # with open(unavailable_file_path, "w") as file:
                #     file.write("Transcript unavailable")
                unavailable_videos.append(clean_title)
                total_not_transcribed.append(clean_title)
                unique_videos.remove(video_url)
                # print(f"Transcript unavailable for video: {video_title}")
                video_data = video_data[video_data["video_url"] != video_url]
                video_data.to_csv(csv_from_playlist.FILE_PATH, index=False)

                # Remove from master_metadata
                try:
                    master_metadata = pd.read_csv('master_metadata.csv')
                    master_metadata = master_metadata[master_metadata["video_url"] != video_url]
                    master_metadata.to_csv('master_metadata.csv', index=False)
                    print(f"Removed {video_url} from master_metadata.csv")
                except FileNotFoundError:
                    print("Error: The file master_metadata.csv was not found.")
            pbar.update(1)

    print(f"\nTranscribed {len(total_transcribed)} videos \n ")
    print(f"Updating master_metadata.csv with {len(total_transcribed)} new entries.")
    if len(total_not_transcribed) > 0:
        print(f"Transcripts unavailable for {len(total_not_transcribed)} videos: \n")
        for video in total_not_transcribed:
            print(video)
    new_videos = len(total_transcribed)


def create_raw_strings_for_all_folders():
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    n_successful = 0
    folders = []
    folder_names = []
    no_transcripts = 0
    n_skipped = 0
    # Iterate through each folder in the parent directory
    for folder_name in os.listdir(parent_directory):
        source_folder = os.path.join(parent_directory, folder_name)
        
        # Check if the folder name ends with "_transcripts"
        if os.path.isdir(source_folder) and folder_name.endswith("_transcripts"):
            # Create the new folder for human-readable transcripts
            nlp_folder = f"{source_folder}_for_machines"
            if os.path.exists(nlp_folder):
                n_skipped += 1
                # print(f"Skipping {folder_name}, machine transcripts already exist.\n")
                folders.append(nlp_folder)  # Add even skipped folders
                folder_names.append(nlp_folder)
                continue
            
            os.makedirs(nlp_folder, exist_ok=True)

            # Iterate through each .txt file in the source folder
            for filename in os.listdir(source_folder):
                # if filename.endswith(".txt") and not filename.endswith("_transcript_unavailable.txt"):
                file_path = os.path.join(source_folder, filename)
                with open(file_path, "r") as file:
                    transcript_text = file.read()

                cleaned_transcript = get_cleaned_transcript(transcript_text)
                nlp_file_path = os.path.join(nlp_folder, filename)
                
                # Write the human-readable transcript
                with open(nlp_file_path, "w") as file:
                    file.write(cleaned_transcript)

    # print(f"Skipping {n_skipped} channels where machine transcripts already exist.\n")
    print(f"\nSkipping {n_skipped} channels where transcript folders already exist.")

def create_human_readable_transcripts_for_all_folders():
    # Get the directory that the .py file is in
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    n_successful = 0
    folders = []
    folder_names = []
    no_transcripts = 0
    n_skipped = 0
    # Iterate through each folder in the parent directory
    for folder_name in os.listdir(parent_directory):
        source_folder = os.path.join(parent_directory, folder_name)
        
        # Check if the folder name ends with "_transcripts"
        if os.path.isdir(source_folder) and folder_name.endswith("_transcripts"):
            # Create the new folder for human-readable transcripts
            human_readable_folder = f"{source_folder}_for_humans"
            if os.path.exists(human_readable_folder):
                n_skipped += 1
                # print(f"Skipping {folder_name}, human_readable transcripts already exist.\n")
                folders.append(human_readable_folder)  # Add even skipped folders
                folder_names.append(human_readable_folder)
                continue
            
            os.makedirs(human_readable_folder, exist_ok=True)

            # Iterate through each .txt file in the source folder
            for filename in os.listdir(source_folder):
                # if filename.endswith(".txt") and not filename.endswith("_transcript_unavailable.txt"):
                file_path = os.path.join(source_folder, filename)
                with open(file_path, "r") as file:
                    transcript_text = file.read()

                cleaned_transcript = get_cleaned_transcript(transcript_text)
                human_readable_file_path = os.path.join(human_readable_folder, filename)
                
                # Write the human-readable transcript
                with open(human_readable_file_path, "w") as file:
                    file.write(f"With timestamps:\n\n{transcript_text}\n\n")
                    file.write(f"Cleaned transcript:\n\n{cleaned_transcript}\n")

                n_successful += 1
            folders.append(human_readable_folder)
            folder_names.append(human_readable_folder)
    
        # folder_names = [re.search(r'[^/\\]+$', folder).group(0) for folder in folders]
        # print("\nCalculating total number of human-readable transcripts:")
    
    # print(f"\nSkipping {n_skipped} channels where human_readable transcripts already exist.\n")
    for folder in folders:
        files = os.listdir(folder)
        no_files = len([f for f in files if os.path.isfile(os.path.join(folder, f))])
        no_transcripts += no_files
        # print(f"Folder {folder} has {no_files} files.")
    
    
    # if playlist_controller.metadata_dupes == 1:
    #     print(f"\nSkipped {playlist_controller.metadata_dupes} channel, the metadata file already exists.\n")
    # if playlist_controller.skipped_channels == 1:
    #     print(f"Skipped {playlist_controller.skipped_channels} folder where basic transcripts already exist.\n")
    # if n_skipped == 1:
    #     print(f"Skipped {n_skipped} folder where human_readable transcripts already exist.\n")
    
    # if playlist_controller.metadata_dupes > 1:
    #     print(f"\nSkipped {playlist_controller.metadata_dupes} channels, metadata files already exist.\n")
    # if playlist_controller.skipped_channels > 1:
    #     print(f"Skipped {playlist_controller.skipped_channels} folders where basic transcripts already exist.\n")
    # if n_skipped > 1:
    #     print(f"Skipped {n_skipped} folders where human_readable transcripts already exist.\n")
    # print(f"\nmaster_metadata.csv now contains {no_transcripts} videos from {len(folder_names)} channels. \nHuman-readable transcripts created under the following directories:\n")

    master_metadata_path = os.path.join(parent_directory, 'master_metadata.csv')
    if os.path.exists(master_metadata_path):
        with open(master_metadata_path, 'r') as file:
            n_videos = sum(1 for row in file) - 1  # Subtract 1 to exclude the header row
    else:
        n_videos = 0
    
    # print(f"master_metadata.csv now contains {no_transcripts} videos from {len(folder_names)} channels.\n\nHuman-readable transcripts created under the following directories:\n")
    # for folder in folder_names:
    #     print(folder.split('/')[7])