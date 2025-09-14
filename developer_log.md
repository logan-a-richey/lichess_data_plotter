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
* added css to configure the sizing of image, html tables, and hypertext

## Sep 12, 2025
* created graphs 3 and 4; opening frequency and adoption data
* explored plotting with Chart.js
* explored javascript to allow for dynamic display options.
* html table sorting and ordering
* Chart.js on click behavior to warp to entry in html table

## Sep 13, 2025
* applied css style sheets to all graphs
* separated js from html - putting it in its own file
* debugged canvas and div formatting in html
* significantly improved user experience
* added elo simulation for casual bullet games
* checkbox to toggle visibility of elements, update using javascript functions

## Sep 14, 2025
* improved performance on rating simulation by adding indexes to desired database cols, used datetime instead of pandas to parse my_date
* created get_most_common_user function. now we can automatically detect the user from the <games.pgn> file.
* explored Gunicorn usage with Flask 
* changed current index.html -> dashboard.html
* created file upload page, loading page, dashboard page
* working full-stack application

Skills learned: Flask + Gunicorn, HTML + CSS + Javascript techniques, basic GET and POST requests, file upload form feature, more complex sql queries. 

