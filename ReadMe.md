Purpose: This is the ReadMe for the BaseballAnalytics program.
By: Benjamin Goebel
Date: August 24th, 2017

1. The purpose of this program is to analyze 2016 MLB batting data. Users can
   get and graph stats, as well as, get the MLB season standings.
2. Excluding this file, there are two other files in this program:
   baseball-stats.py and mlb-stats2016.xlsx.
3. The predominant data structure in this program is the pandas' DataFrame. The
   MLB players' batting data is stored in a DataFrame, and the 2016 MLB
   standings are also stored in a DataFrame.
4. The general algorithm for this program is as follows. The user requests
   MLB data via one of the program commands. The program accesses the data from
   the DataFrame and prints out the data to the user.  
5. This program can be compiled using a Makefile. Users running this program
   must have Numpy, pandas and matplotlib installed on their computers.
   Additionally, users must have the Excel file, 'mlb-stats2016.xlsx',
   (provided on Github) in the same directory as this program.

Sources:
1. Python for Data Analysis by Wes McKinney
2. www.packtpub.com/mapt/book/big_data_and_business_intelligence/9781849513265/1/ch01lvl1sec16/plotting-multiple-bar-charts
