**README for "Data" Directory in "identity\_specific\_coding\_education" Repository**

**1\. Introduction**  
 The /data directory houses various data files, transcripts, scripts, and utilities that facilitate the collection, processing, and analysis of YouTube videos from specific coding education channels. The directory is designed to support both qualitative and quantitative research efforts, particularly in understanding how coding education is delivered across different platforms and audiences.

**2\. Directory Structure**  
 Database Files (CSVs and xlsx)  
   ├── master\_metadata.csv  
   ├── Beginner's Code Zone\_metadata.csv  
   ├── CS50 Made Easy with Rahul\_metadata.csv  
   ├── relevant\_channels\_log.xlsx  
   ├── …  
Transcripts (3 variations per channel transcribed)  
   ├── alvinblox\_transcripts/  
   ├── alvinblox\_transcripts\_for\_humans/  
   ├── alvinblox\_transcripts\_for\_machines/  
   ├── …  
Python Scripts  
   ├── playlist\_controller.py  
   ├── transcript\_playlist\_helper.py  
   ├── …  
Executables (to run python scripts from shell in /data)  
   ├── controller  
Other Folders  
   ├── qualitative\_team\_videos/  
   ├── playlist\_links/  
   	├── TAP Playlist Links.xlsx  
Utilities  
   ├── README  
	  
**3\. Metadata Files**  
CSV files containing metadata for videos from various coding channels or programs   
Metadata are comprised of the following categories (dtypes listed on right)  
*channel\_name            object*  
*video\_title             object*  
*video\_url               object*  
*publish\_date            object*  
*video\_length            object*  
*views                    int64*  
*likes                    int64*  
*comments                 int64*  
*transcript\_filename     object*  
*Tier (1, 2, or 3\)        int64*  
Master Metadata files

* master\_metadata \- CSV containing metadata for every transcribed video. Updated with each code run.   
* master\_metadata\_all\_videos \- CSV containing metadata for every video processed, regardless of transcription status. Updated with each new playlist\_csv that is processed.   
* master\_metadata\_all\_videos\_cleaned \- CSV containing metadata for every transcribed video, cleaned in analysis/summarize\_and\_check\_data scripts. 

Playlist Metadata Files

* Any file beginning in “Upload…” or “\[channel name\]” is a metadata file built from video data from the associated channel(s) in the playlist.  Before generating transcripts, the file will mirror the filtered rows by‘channel\_name’ in master\_metadata\_all\_videos. After generating transcripts, the file should mirror the filtered rows by ‘channel\_name’ in master\_metadata, as non-transcript rows are removed.

Relevant Channels Log(.xlsx)

* relevant\_channels\_log.xlsx \- A log file listing channels considered relevant for the project, as determined by YouTube search protocol with 49 terms.  The log includes metadata categories: Top 10 from channel sent to qual team, Tier (1, 2, or 3), Search term, Channel in English, Channel Handle, Notes / Channel ID, Audience, URL, Subscriber count, Identity-specific, Rank, and Date Accessed.

**4\. Transcript Files**     
There are three types of transcripts in channel, sorted into folders by the following naming conventions:  
1\. Original Transcripts (\[channel\_name\]\_transcripts)

- Timestamped transcripts directly from YouTube, tab-spacing by line on time intervals.  
- Useful for manual/qualitative review.  

2\. Human-Readable Transcripts (\[channel\_name\]\_for\_humans)

- Contains two sections \- Useful for manual/qualitative review:  
  - “With Timestamps” \- Timestamped transcripts directly from YouTube, tab-spacing by line on time intervals. Useful for manual/qualitative review.  
  - “Cleaned transcript” \- Cleaned version of timestamped transcript, filtering out timestamps, timestamp-based spacing, and items like “\[Music\]”. 

3\. Machine-Readable Transcripts (\[channel\_name\]\_for\_machines)

- Contains cleaned transcript as unformatted plain text with no heading.   
- Useful for machine/quantitative analysis like NLP or word-frequency charts

Example Transcript formats:

* /black girls code\_transcripts/adayinthelifeofasoftwareengineeratriotgames.txt  
  *00:00 \- as a software engineer at write games I*  
  *00:02 \- usually start by waking up either going*  
  *00:06 \- into the office or starting at home and*

  *….*

    
* /black girls code\_transcripts\_for\_humans/adayinthelifeofasoftwareengineeratriotgames.txt  
  *With timestamps:*  
    
  *00:00 \- as a software engineer at write games I*  
  *00:02 \- usually start by waking up either going*  
  *00:06 \- into the office or starting at home and*  
  		*….*  
    
  *Cleaned transcript:*  
    
  *as a software engineer at write games I usually start by waking up either going into the office or starting at home and* 

  ….

    
* /black girlscode\_transcripts\_for\_humans/adayinthelifeofasoftwareengineeratriotgames.txt  
  *as a software engineer at write games I usually start by waking up either going into the office or starting at home and*   
  		….

**5\. Scripts and Utilities**    
 Overview of Python scripts available in the directory. See files for info on individual functions.

- csv\_from\_playlist.py: Script for extracting CSV data from YouTube playlists.  Populates master\_metadata.csv and creates playlist\_specific CSVs.  
- playlist\_transcript\_helper.py: Helper script for processing transcripts and creating transcript directories  
- playlist\_controller.py: Controller script that runs the above processing functions. Updates master\_metadata, checks for and resolves inconsistencies between master\_metadata and \_transcripts folders, prints out terminal dialog with summary statistics for each run of code.

**6\. Executables**  
controller: Executable script for running playlist\_controller.py from command\_line

- To build/update the database, clone [our repository](https://github.com/cogtoolslab/identity\_specific\_coding\_education) and do the following steps:   
  1\. Open terminal or command line on your local machine  
  2\. Enter the following to navigate the directory where the repo exists on your local machine  
      (mac) cd YOUR/LOCAL/PATH/identity\_specific\_coding\_education/data        
     (windows) cd YOUR\\LOCAL\\PATH\\identity\_specific\_coding\_education\\data  
  3\. Enter the following to access the script interface  
      (mac) ./controller  
      (windows) .\\controller.exe  
  4\. Enter the URL(s) for playlist(s) that you want process, each in quotes, followed by the number 1 or 2, to select the API Key.    
       Correct format: "URL" "URL" "URL" \[1 or 2\]   


  *The number of URLs here is purely demonstrative.  You can enter as many URLs as you please, as long as it follows the format shown above.*

  5\. Upon completion, you should see the folllowing in your terminal/command-line (numbers will differ based on your database)

    	 21480 total videos were collected from 67 unique channels, 16206 were successfully transcribed from 65 unique channels.
         There are 2 channels awaiting transcription.  
    	 Untranscribed channels are: \['programmingknowledge2', 'bk hindi kahani'\]  
  FAQs:

  You should generally be able to use either key without issue, if one stops working, try the other one.  Contact me at eapple25@stanford.edu if you have more specific questions about API keys.

**7\. Other Folders**

- qualitative\_team\_videos/: Folder containing curated list of videos selected for manual review by qualitative team.    
- playlist\_links/:  Folder containing “Tap Playlist Links.xlsx”, a workbook with templates for tracking progress while database building.   
