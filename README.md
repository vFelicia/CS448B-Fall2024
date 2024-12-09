# CS448B-Fall2024-Final-Project-Submission

This is repo is an adapted repository of the main one I'm using for research. It has only the essential files needed to run everything, with some specific instruction! 

I foresee some issues if you try to run the code yourself for grading:
* You MIGHT need to run through the pipeline to produce files required for `08-nlp-interactive-visualization.ipynb`, and this is because some files are too big to commit to GitHub. This repo should be finalized by submission so you don't have to, but that means I will not be able to further commit to the repo after I submit it.
* Unfortuantely, some of the Jupyter Notebooks need to be ran on a virtual environment of Python 3.9.0 and you will therefore likely have to install some libraries.
* Please contact me if there's an alternative method for you to see everything to make grading easier -- vgfelica@stanford.edu or on Slack as Vryan Feliciano.

Here's an explanation of what's on the repo as it pertains to the final project:
- `analysis --> NLP Analysis`: This directory will contain all files related to the NLP Analysis. The visualizations are chiefly in the `08-nlp-interactive-visualization.ipynb` Jupyter Notebook.
  - You will still need to run `01-nlp-dataloading-merging` and `02-nlp-preprocessing` to produce `clean_metadata_transcript.csv` and `clean_metadata_transcript.pkl`, which are needed for the visualizatiob code.
  -  The Notebooks that use Python 3.9.0 are `07-nlp-topicmodeling.ipynb` and `08-nlp-interactive-visualization.ipynb`. Everything else runs in Python 3.13.0.
-  `08-nlp-interactive-visualization.ipynb` depends on the following:
  - `clean_metadata_transcript.csv` and `clean_metadata_transcript.pkl`, which are produced in `02-nlp-preprocessing` but needs `01-nlp-dataloading-merging` to run `metadata_transcript.csv` to be proprocessed and cleaned
  - `04-nlp-advanced-analysis` to produce Channel Log-Odds TFD CSV files stored in `Log_Odds_Analysis`
  - `07-nlp-topicmodeling.ipynb` to produce channel topic modeling data produced in the folder `channel_topic_analysis`
- `data`: This directory contains the data used for the research project in general.
- `Python3.9.0-libraries-versions`: This file contains all the libraries + versions needed to run in Python 3.9.0.
- `A3`: Is just my A3 submission!

VIDEO SUBMISSION FOUND HERE: https://youtu.be/s-UoMgOU9E0

Vryan Feliciano -- vgfelica@stanford.edu -- 006371790
