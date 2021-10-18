# youtube-comment-analysis
This project goes through six steps to form a complete end to end project.  The final deliverable is hosted on the Google Cloud and can be see at the following web address:

https://conductive-well-329218.uc.r.appspot.com/

The complete project goes through the following six steps:
1. Pull all parent comments for a given YouTube channel using YouTube's API
2. Upload the data into a relational database using Google BigQuery in Python
3. Query the database for the information using Python
4. Perform a sentiment and TF-IDF analysis on the comments
5. Build a Dash dashboard to display the analysis
6. Host the Dash dashboard on the web using Google Cloud

*NOTE:* Since the data set was so large, for the csv files uploaded to GitHub, only 60,000 of the more than 600,000 comments are in the files.  However, for the final dashboard I am hosting and is accessible via the link above, it includes an analysis of all 600,000+ comments.
