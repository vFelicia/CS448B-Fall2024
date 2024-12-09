# Videos for Qualitative Analysis
This folder contains the lists of videos for qualitative analysis found in [this Google Sheet](https://docs.google.com/spreadsheets/d/1VCSVIrSLdExD71Kd045u8A3p_fbAgwOzr1_TvZRKt2A/edit?usp=sharing). 

There are two relevant tabs in this Google Sheet and therefore two .csv files in this folder: one for instructional videos and one for promotional videos. The instructional videos list has undergone multiple rounds of updates but is relatively stable. The promotional videos list is an ongoing project --- the Google Sheet will have the most up-to-date list.

### Instructional Videos
Variables
| Variable | Description | Example |
| ------ | ------ | ------ |
| Channel Name or Channel Handle | Either the Youtube channel name or channel handle of the relevant video. (Note: old versions of the script output the channel handle and the newest version outputs the channel name.) | 'Black Girls Code'
| Video Title | The title of the relevant Youtube vide. | 'Introducing CodeBytes!'
| Video URL | The URL of the relevant Youtube video. | https://www.youtube.com/watch?v=SZ_iQ4SY1AA
| Transcript Link | The Google Drive link to a file containing the video transcript in two formats: with timecodes in the version output by the Youtube API and cleaned (as a string, extraneous text removed). | 'introducingcodebytes.txt'
| Publish Date | Date on which the relevant Youtube video was published.| '11/5/20' |
| Video Length | The length of the video, as output by the Youtube API (in variations of dd:hh:mm:ss format). | '1:18', '26:40:00', '0:32', etc. |
| Views | The view count of the Youtube video at the time of running the script. | 27792 |
| Likes | The number of likes of the Youtube video at the time of running the script. | 359 |
| Comments | The number of comments on the Youtube video at the time of running the script. | 0 |
| Transcript Filename in Github | The name of the file which contains the relevant viedo's transcript in this Github repository. | 'introducingcodebytes.txt' |
| BatchID | The round/batch in which a given video was sent to the Qualitative Team. | 2 |
| Date Generated | The date in which the metadata and transcript was generated. | 'Thu 7/18/2024' |

### Promotional Videos
Variables
| Variable | Description | Example |
| ------ | ------ | ------ |
| Channel Name (HANDLE) | The handle of the relevant Youtube channel. | 'BlackGirlsCode' |
| Video Title | The title of the relevant Youtube video. | 'Join the Movement to #PayItForward' |
| Video URL | The URL of the relevant Youtube video. | https://www.youtube.com/watch?v=HwzY8kOjAgw |
| Transcript Link | The Google Drive link to a file containing the video transcript in two formats: with timecodes in the version output by the Youtube API and cleaned (as a string, extraneous text removed). | 'howtocodein2022fromzerotocareerlevel.txt' |

