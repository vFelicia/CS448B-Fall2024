# Playlist Links
This folder contains the lists of playlist links found on [this Google Sheet](https://docs.google.com/spreadsheets/d/1VOmFL1hTqufmiL6rD64FDOXD5DGDCMM1BWCeBfY8VKs/edit?usp=sharing), which can be run to reproduce our dataset of videos. 

There are currently five tabs in this spreadsheet. The first, "ReadMe," has a quick description of the file. The second, "All Links to Reproduce Dataset," is a template future users can utilize to generate our dataset. "Re-Processing Start 8/11 Reproduce Dataset" is a version of this tab which we used to reproduce our dataset on 8/11. "Small Curated Playlists" has a list of small, hand-curated playlists chosen by relevance to the project. "Playlists for Full Channels" has a list of playlists where each playlist has all the videos on a channel's Youtube page. These full-channel playlists were generated using [this strategy](https://www.reddit.com/r/youtube/comments/145d6hn/viewing_all_channel_videos_as_playlist/), and appear to self-update as channels add more videos.

### All Links to Reproduce Dataset
Variables
| Header | Description | Example |
| ------ | ------ | ------ |
| Channel Name | The name of the relevant Youtube channel. | 'Black Girls Code' |
| Tier | The tier of the Youtube channel. Either 1, 2, or 3, with 1 being top-priority and 3 being lowest-priority.| '1'
| Playlist | The url to the playlist made for the given channel. | 'https://youtube.com/playlist?list=UU8butISFwT-Wl7EV0hUK0BQ&feature=shared'
| English | Whether or not the channel is in English. Either 'TRUE' or 'FALSE.' | 'TRUE'
| Metadata Status | Whether or not the metadata for the channel has been generated. Either 'TRUE' or 'FALSE.' | 'FALSE'
| Transcript Status | Whether the transcripts have been generated for a given channel. Either 'TRUE' or 'FALSE.'| 'FALSE'

### Small Curated Playlists
Variables
| Header | Description | Example |
| ------ | ------ | ------ |
| Channel Name | The name of the relevant Youtube channel. | 'Black Girls Code' |
| Tier | The tier of the Youtube channel. | '2'
| Playlist | The url to the playlist made for the given channel. | 'https://youtube.com/playlist?list=UU8butISFwT-Wl7EV0hUK0BQ&feature=shared'

### Playlists for Full Channels
Variables
| Header | Description | Example |
| ------ | ------ | ------ |
| Channel Name | The name of the relevant Youtube channel. | 'Black Girls Code' |
| Channel Handle | The handle of the relevant Youtube channel. | 'BlackGirlsCode' |
| Tier | The tier of the Youtube channel. | '2'
| Playlist | The url to the playlist made for the given channel. | 'https://youtube.com/playlist?list=UU8butISFwT-Wl7EV0hUK0BQ&feature=shared'