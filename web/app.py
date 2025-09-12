#!/usr/bin/env python3

from flask import Flask, Response, render_template, request

import json
import pymysql
import matplotlib
matplotlib.use('Agg')

my_username = "larichey"
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_results_pie_chart")
def get_results_pie_chart():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()

    sql_white_result = "SELECT COUNT(*) FROM my_games WHERE (white=%s AND result=%s)"
    sql_black_result = "SELECT COUNT(*) FROM my_games WHERE (black=%s AND result=%s)"

    white_results = {"wins": 0, "losses": 0, "draws": 0}
    black_results = {"wins": 0, "losses": 0, "draws": 0}

    # White perspective
    dbh.execute(sql_white_result, (my_username, "1-0"))
    white_results["wins"] = dbh.fetchone()[0]
    dbh.execute(sql_white_result, (my_username, "0-1"))
    white_results["losses"] = dbh.fetchone()[0]
    dbh.execute(sql_white_result, (my_username, "1/2-1/2"))
    white_results["draws"] = dbh.fetchone()[0]

    # Black perspective
    dbh.execute(sql_black_result, (my_username, "0-1"))
    black_results["wins"] = dbh.fetchone()[0]
    dbh.execute(sql_black_result, (my_username, "1-0"))
    black_results["losses"] = dbh.fetchone()[0]
    dbh.execute(sql_black_result, (my_username, "1/2-1/2"))
    black_results["draws"] = dbh.fetchone()[0]

    connection.close()

    return render_template(
        "results_pie_chart.html",
        white_results=white_results,
        black_results=black_results
    )

@app.route("/get_games_per_month")
def get_games_per_month():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()

    sql = """
        SELECT DATE_FORMAT(my_date, '%%Y-%%m') AS month, COUNT(*) AS games
        FROM my_games
        WHERE white = %s OR black = %s
        GROUP BY month
        ORDER BY month;
    """
    dbh.execute(sql, (my_username, my_username))
    rows = dbh.fetchall()
    connection.close()

    months = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    return render_template("games_per_month.html", months=months, counts=counts, zip=zip)

if __name__ == "__main__":
    app.run(debug=True)

