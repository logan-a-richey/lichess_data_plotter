#!/usr/bin/env python3

from flask import Flask, Response, render_template, jsonify

import json
import sqlite3
import re

import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import os 
import io

import pymysql
import json

# load db creditials

my_username = "larichey"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get_results_pie_chart")
def get_results_pie_chart():
    return render_template("results_pie_chart.html")

@app.route("/plot.png")
def plot_png():
    # Database functions:
    dsn = {}
    try:
        with open("my_dsn.json", "r") as file:
            dsn = json.load(file)
    except Exception as e:
        print("[E] Could not load dsn : {}".format(e))
    
    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()

    # Queries
    sql_white_result = "select count(*) from my_games where (white=%s and result=%s)"
    sql_black_result = "select count(*) from my_games where (black=%s and result=%s)"

    white_results = {
        "wins": 0,
        "losses": 0,
        "draws": 0
    }
    black_results = {
        "wins": 0,
        "losses": 0,
        "draws": 0
    }
    
    # valid_results = ["1-0", "1/2-1/2", "0-1"]

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
    
    print("[INFO] ", white_results, black_results)

    # Now build 2 pie charts side by side
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].pie(
        list(white_results.values()),
        labels=list(white_results.keys()),
        autopct="%1.1f%%"
    )
    axs[0].set_title("As White")

    axs[1].pie(
        list(black_results.values()),
        labels=list(black_results.keys()),
        autopct="%1.1f%%"
    )
    axs[1].set_title("As Black")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return Response(buf.getvalue(), mimetype="image/png")

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5000)

