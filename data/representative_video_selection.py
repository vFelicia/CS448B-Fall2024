import pandas as pd
import numpy as np
from scipy.stats import zscore

# Load the dataset
file_path = 'master_metadata.csv'
df = pd.read_csv(file_path)

# Preprocess data: attempt to infer the date format, handling missing or incorrect dates
df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')
df.fillna(0, inplace=True)

# Normalize dates to ensure consistency (optional, depending on your needs)
# df['publish_date'] = df['publish_date'].dt.normalize()

# Calculate Z-scores for relevant columns within each channel (Local Z-scores)
df['views_z_local'] = df.groupby('channel_name')['views'].transform(zscore)
df['likes_z_local'] = df.groupby('channel_name')['likes'].transform(zscore)
df['comments_z_local'] = df.groupby('channel_name')['comments'].transform(zscore)
df['publish_date_z_local'] = df.groupby('channel_name')['publish_date'].transform(lambda x: zscore(x.astype(np.int64)))

# Calculate Z-scores for relevant columns across the entire dataset (Global Z-scores)
df['views_z_global'] = zscore(df['views'])
df['likes_z_global'] = zscore(df['likes'])
df['comments_z_global'] = zscore(df['comments'])
df['publish_date_z_global'] = zscore(df['publish_date'].astype(np.int64))

# Filter channels with at least 5 videos
channel_counts = df['channel_name'].value_counts()
channels_to_include = channel_counts[channel_counts >= 5].index
filtered_df = df[df['channel_name'].isin(channels_to_include)].copy()  # Use .copy() to avoid SettingWithCopyWarning

# Compute Composite Representative Scores
filtered_df['local_composite_score'] = filtered_df[['views_z_local', 'likes_z_local', 'comments_z_local', 'publish_date_z_local']].apply(lambda x: np.sum(np.abs(x)), axis=1)
filtered_df['popularity_score'] = filtered_df[['views_z_local', 'likes_z_local']].apply(lambda x: np.sum(np.abs(x)), axis=1)
filtered_df['global_composite_score'] = filtered_df[['views_z_global', 'likes_z_global', 'comments_z_global', 'publish_date_z_global']].apply(lambda x: np.sum(np.abs(x)), axis=1)

# Rank videos by representativeness (scores close to zero rank higher) within each channel
filtered_df = filtered_df.sort_values(['channel_name', 'local_composite_score'])

# Select up to the most representative n% of videos per channel where local composite score is below 1, whichever comes first
def select_dynamic_videos(group):
    prop_channel = 0.5
    top_n = int(np.ceil(len(group) * prop_channel))  # Calculate the number of videos to select based on the threshold
    # representative_videos = group[group['local_composite_score'] < 1].head(top_n)  # Select videos under the local composite score threshold
    representative_videos = group.sort_values('local_composite_score').head(top_n)

    return representative_videos


# fn that creates mixture of "most popuplar" and "most representative",
# tweakable by 
def mixed_dynamic_videos(group):
    prop_channel = 0.5
    num_popular = 4
    top_n = int(np.ceil(len(group) * prop_channel))  # Calculate the number of videos to select based on the threshold
    
    # Sort the group based on 'popularity_score' and 'local_composite_score'
    popular_videos = group.sort_values('popularity_score', ascending=False).head(num_popular)  # Top 4 most popular videos
    representative_videos = group.sort_values('local_composite_score').head(top_n)  # Next 8 to 12 most representative videos
    
    # Merge the two sets
    mixed_representative_videos = pd.concat([popular_videos, representative_videos]).drop_duplicates().reset_index(drop=True)
    
    return mixed_representative_videos.


representative_videos_per_channel = filtered_df.groupby('channel_name').apply(select_dynamic_videos).reset_index(drop=True)
mixed_representative_videos_per_channel = filtered_df.groupby('channel_name').apply(mixed_dynamic_videos).reset_index(drop=True)

# Keep only the specified columns and both composite scores
columns_to_keep = [
    'channel_name', 'video_title', 'video_url', 'publish_date', 
    'video_length', 'views', 'likes', 'comments', 
    'transcript_filename', 'Tier (1, 2, or 3)', 
    'local_composite_score', 'global_composite_score'
]

final_output = representative_videos_per_channel[columns_to_keep]

# Count the number of selected videos per channel
final_channel_counts = final_output['channel_name'].value_counts()

# Filter the output to include only channels with at least 5 selected videos
final_channels_to_include = final_channel_counts[final_channel_counts >= 5].index
final_filtered_output = final_output[final_output['channel_name'].isin(final_channels_to_include)]

# Save the filtered result to a file
output_file_path = 'representative_videos_per_channel.csv'
final_filtered_output.to_csv(output_file_path, index=False)