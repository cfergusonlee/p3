# P3: Wrangle West Springfield OpenStreetMap Data

![West Springfield Map](https://github.com/spacecadet84/p3/blob/master/screen-shots/map.png "West Springfield Map")

This project used data wrangling techniques to explore and clean OpenStreetMap data for West Springfield, MA.  I used Python for most of the cleaning and SQL to create a relational database.  A summary of the process is below:

**Process Overview**
1. Created a smaller test file to reduce system load
2. Cleaned the data in Python
    1. Checked for problem characters in each tag
    2. Cleaned up overabbreviated street names
    3. Fixed incorrect zip codes
    4. Standardize phone numbers
5. Converted from xml to csv
6. Imported the cleaned .csv into a SQL database
7. Explored the database through queries
