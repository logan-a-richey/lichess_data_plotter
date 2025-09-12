# Developer Log

## Sep 6, 2025
* created a chess game parser to read a lichess pgn file line by line
* originally created the parser in perl before translating to python
* installed and configured mysql server on ubuntu host 
* created sql schema to hold data read from parser
* loaded database with 53,000+ records.
* added additional post-processing to the data; added additional fields to the database schema
* wrote flask web app to read data from the database
* used matplotlib to generate graphs (no image files written to disk, binary data streamed to web browser)
* created several flask app routes to handle webpage. 
* able to display game win-draw-loss data for user for white and black.

Skills learned: sql, mysql_server, pymysql, regex, flask, html, jinga, matplotlib

## Sep 10, 2025
* created graph 2: line graph of games per month
* explored month by month sql query
* explored jinga templating and variables
* added some css to configure the sizing of image, html tables, and hypertext
