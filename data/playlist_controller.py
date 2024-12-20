# 
import argparse
import csv_from_playlist 
import playlist_transcript_helper
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import numpy as np
import os
global metadata_dupes 
metadata_dupes = int(0)
global skipped_channels
skipped_channels = 0

# API_KEY = "AIzaSyCe8NA-YF6fObjYjUr8nKFX0ZFycl39fWo" #Elias
# API_KEY = "AIzaSyDytKnvxq-wB61dyviuzOoI2wdyrnlLqpI" #Nora

def update_master_metadata(new_csv_file):
    # Read the new CSV file
    # new_data = pd.read_csv(new_csv_file)
    new_data = pd.read_csv(new_csv_file)
    
    # Read the master metadata CSV file
    try:
        master_data = pd.read_csv('master_metadata.csv')
        all_data = pd.read_csv('master_metadata_all_videos.csv')
    except FileNotFoundError:
        master_data = pd.DataFrame()
        all_data = pd.DataFrame()
    
    # Append new data to the master data
    master_data = pd.concat([master_data, new_data], ignore_index=True)

    # Append new data to the raw uncleaned data
    all_data = pd.concat([all_data, new_data], ignore_index=True)
    
    # Remove duplicates based on video_url
    master_data.drop_duplicates(subset='video_url', keep='first', inplace=True)
    all_data.drop_duplicates(subset='video_url', keep='first', inplace=True)
    
    # Read the relevant channels log file
    relevant_channels_log = pd.read_excel('relevant_channels_log.xlsx', sheet_name='queries_to_channels')
    
    # Create a mapping from channel in English to Tier (1, 2, or 3)
    tier_mapping = relevant_channels_log.set_index('channel in English')['Tier (1, 2, or 3)'].to_dict()
    
    # Map the tier values to the master data
    master_data['Tier (1, 2, or 3)'] = master_data['channel_name'].map(tier_mapping)
    all_data['Tier (1, 2, or 3)'] = all_data['channel_name'].map(tier_mapping)
    
    # Identify channels without a tier and ask the user for input
    missing_tiers = master_data[master_data['Tier (1, 2, or 3)'].isna()]['channel_name'].unique()
    
    new_entries = []
    
    for channel in missing_tiers:
        while True:
            try:
                tier = int(input(f"Enter tier (1, 2, or 3) for the channel '{channel}': "))
                if tier in [1, 2, 3]:
                    master_data.loc[master_data['channel_name'] == channel, 'Tier (1, 2, or 3)'] = tier
                    new_entries.append({'channel in English': channel, 'Tier (1, 2, or 3)': tier})
                    break
                else:
                    print("Invalid input. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a numeric value 1, 2, or 3.")
    
    # Update the relevant channels log with new entries
    if new_entries:
        new_entries_df = pd.DataFrame(new_entries)
        relevant_channels_log = pd.concat([relevant_channels_log, new_entries_df], ignore_index=True)
    
    # Save the updated master data back to the master CSV file
    master_data.to_csv('master_metadata.csv', index=False)
    all_data.to_csv('master_metadata_all_videos.csv', index=False)
    
    # Save the updated relevant channels log back to the Excel file
    with pd.ExcelWriter('relevant_channels_log.xlsx', engine='openpyxl') as writer:
        relevant_channels_log.to_excel(writer, sheet_name='queries_to_channels', index=False)

def standardize_types_in_directory():
    counts = 0
    # Get the current directory
    directory = os.path.dirname(os.path.abspath(__file__))
    
    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            # Read the CSV file
            # df = pd.read_csv(filepath, error_bad_lines=False, encoding='utf-8')
            df = pd.read_csv(filepath)

            # Convert specified columns to integer type
            columns_to_convert = ["views", "likes", "comments", "Tier (1, 2, or 3)"]
            for column in columns_to_convert:
                if column in df.columns:
                    df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(int)
            
            # Save the modified DataFrame back to CSV
            df.to_csv(filepath, index=False)
            counts += 1
    print(f"Standardized {counts} csv files with int64 types")

def get_transcript_filenames(transcript_folders):
    filenames = set()
    for folder in transcript_folders:
        # if os.path.exists(folder):
        for filename in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, filename)):
                filenames.add(filename)
    return filenames

def drop_blanks():
    start_len = 0
    end_len = 0
    try:
        # List all folders ending with "_transcripts"
        transcript_folders = [f for f in os.listdir() if os.path.isdir(f) and f.endswith('_transcripts')]

        # Get all transcript filenames from the folders
        transcript_filenames = get_transcript_filenames(transcript_folders)

        # Read the master metadata CSV file
        master_metadata = pd.read_csv('master_metadata.csv')
        start_len = len(master_metadata)

        # Filter rows where transcript_filename exists in the set of valid filenames
        master_metadata = master_metadata[master_metadata['transcript_filename'].isin(transcript_filenames)]

        # Save the updated DataFrame back to the CSV file
        master_metadata.to_csv('master_metadata.csv', index=False)
        end_len = len(master_metadata)
        
        rows_removed = start_len - end_len

        print(f"Removed {rows_removed} rows with missing transcript files from master_metadata.csv")

    except FileNotFoundError:
        print("The file 'master_metadata.csv' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def fill_missing_rows():
    try:
        # List all folders ending with "_transcripts"
        transcript_folders = [f for f in os.listdir() if os.path.isdir(f) and f.endswith('_transcripts')]

        # Get all transcript filenames from the folders
        transcript_filenames = get_transcript_filenames(transcript_folders)

        # Read the master metadata CSV files
        master_metadata = pd.read_csv('master_metadata.csv')
        master_metadata_all_videos = pd.read_csv('master_metadata_all_videos.csv')

        # Check if the function should run (if len(set of filenames from folders) > len(set of 'transcript_filename' filenames))
        if len(set(transcript_filenames)) <= len(set(master_metadata['transcript_filename'])):
            print("No new files to process. Function will not run.")
            return

        # Create a buffer of missing filenames
        existing_filenames = set(master_metadata['transcript_filename'])
        missing_filenames = set(transcript_filenames) - existing_filenames

        # Filter rows from master_metadata_all_videos for the missing filenames
        missing_rows = master_metadata_all_videos[master_metadata_all_videos['transcript_filename'].isin(missing_filenames)]

        # Append missing rows to master_metadata
        master_metadata = pd.concat([master_metadata, missing_rows], ignore_index=True)

        # Save the updated DataFrame back to the CSV file
        master_metadata.to_csv('master_metadata.csv', index=False)

        print(f"Added {len(missing_rows)} missing rows to master_metadata.csv")

    except FileNotFoundError:
        print("The file 'master_metadata.csv' or 'master_metadata_all_videos.csv' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def count_txt_files_in_folders():
    transcript_folders = [f for f in os.listdir() if os.path.isdir(f) and f.endswith('_transcripts')]
    num_transcripts = 0
    transcribed_channels = []

    for folder in transcript_folders:
        num_files = len([f for f in os.listdir(folder) if f.endswith('.txt')])
        num_transcripts += num_files
        transcribed_channels.append(folder.replace('_transcripts', ''))

    return num_transcripts, transcribed_channels

def summary_stats():
    cleaned_metadata = pd.read_csv('master_metadata.csv')
    uncleaned_metadata = pd.read_csv('master_metadata_all_videos.csv')
    # uncleaned_channel_names = uncleaned_metadata['channel_name'].unique()
    # for channel in uncleaned_channel_names:
    #     channel = channel.lower()
    uncleaned_channel_names = [channel.lower() for channel in uncleaned_metadata['channel_name'].unique()]
    null_vals = [np.nan, "in PHP", "Bk Hindi Kahani"]

 # Count the number of .txt files in transcript folders
    num_transcripts, transcribed_channels = count_txt_files_in_folders()

    print(f"{len(uncleaned_metadata)} total videos were collected from {len(uncleaned_channel_names)} unique channels, {num_transcripts} were successfully transcribed from {len(transcribed_channels)} unique channels.")
    print(f"There are {len(list(set(uncleaned_channel_names) - set(transcribed_channels) - set(null_vals)))} channels awaiting transcription.")
    print(f"Untranscribed channels are: {list(set(uncleaned_channel_names) - set(transcribed_channels) - set(null_vals))}")
    print("Note: Learn Coding and Programming with Vishal are entirely in Hindi. Do not try to transcribe!")
    # print(transcribed_channels)

def process_playlist(playlist_url, api_key):
    csv_from_playlist.build_rows(playlist_url, api_key)
    update_master_metadata(csv_from_playlist.FILE_PATH)
    # playlist_transcript_helper.transcribe_videos()

def main():
    # API KEYS
    API_KEY_1 = "AIzaSyCe8NA-YF6fObjYjUr8nKFX0ZFycl39fWo" #Elias
    API_KEY_2 = "AIzaSyDytKnvxq-wB61dyviuzOoI2wdyrnlLqpI" #Nora
    
    parser = argparse.ArgumentParser(description='Process YouTube videos to generate metadata and transcripts.')
    # parser.add_argument('source', choices=['channel', 'playlist'], help='Source type: channel or playlist')
    parser.add_argument('urls_and_key', nargs='+', help='Channel ID or Playlist URLs followed by API Key')
    # parser.add_argument('api_key', help='Needs API Key')
    args = parser.parse_args()

    # if args.source == 'playlist':
    playlist_urls = args.urls_and_key[:-1]
    api_key_choice = args.urls_and_key[-1]

    # Determine which API key to use based on the input
    if api_key_choice == '1':
        api_key = API_KEY_1
    elif api_key_choice == '2':
        api_key = API_KEY_2
    else:
        raise ValueError("Invalid API key choice. Please select 1 or 2.")

    for playlist_url in playlist_urls:
        process_playlist(playlist_url, api_key)
        playlist_transcript_helper.transcribe_videos()

    # function below works on entire dataset(all csvs)
    playlist_transcript_helper.create_human_readable_transcripts_for_all_folders()
    playlist_transcript_helper.create_raw_strings_for_all_folders()
    standardize_types_in_directory()
    drop_blanks() # THIS REMOVES ROWS WITHOUT TRANSCRIPT MATCHES. DO NOT RUN UNTIL YOUR DATABASE IS BUILT.
    fill_missing_rows() # THIS FILLS MISSING ROWS BASED ON WHAT TRANSCRIPTS ARE GENERATED, FILLING FROM ALL_VIDEOS
    summary_stats()


if __name__ == '__main__':
    main()

    
#### RUN PROCESS PLAYLIST WITHOUT TRANSCRIPT HELPER OR DROP_BLANKS ####
#### VERIFY CSV BUILT CORRECTLY - MASTER METADATA == MASTER METADATA ALL VIDEOS - COMMENT OUT DROP_BLANKS ####
#### RUN TRANSCRIPT HELPER TRANSCRIBE VIDEOS ONLY! #####
#### RE-ENABLE DROP_BLANKS(), TRANSCRIPT HELPERS FOR MACHINE AND HUMAN READABLE ####
#### RUN AND VERIFY NUMBER OF TRANSCRIPTS WITH NUMBER OF ROWS IN CSV, THREE TRANSCRIPT FOLDERS FOR EACH CHANNEL ####