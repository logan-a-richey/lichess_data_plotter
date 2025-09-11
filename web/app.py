#!/usr/bin/env python3

'''
CREATE TABLE `my_games` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `event` varchar(255) NOT NULL DEFAULT '',
  `site` varchar(255) NOT NULL DEFAULT '',
  `my_date` datetime NOT NULL,
  `white` varchar(20) NOT NULL DEFAULT '',
  `black` varchar(20) NOT NULL DEFAULT '',
  `result` varchar(8) NOT NULL DEFAULT '1/2-1/2',
  `gameid` varchar(20) NOT NULL DEFAULT '',
  `whiteelo` int unsigned NOT NULL DEFAULT '1200',
  `blackelo` int unsigned NOT NULL DEFAULT '1200',
  `whitetitle` varchar(8) NOT NULL DEFAULT '',
  `blacktitle` varchar(8) NOT NULL DEFAULT '',
  `whiteratingdiff` varchar(8) NOT NULL DEFAULT '',
  `blackratingdiff` varchar(8) NOT NULL DEFAULT '',
  `variant` varchar(20) NOT NULL DEFAULT 'Standard',
  `timecontrol` varchar(20) NOT NULL DEFAULT '',
  `eco` varchar(20) NOT NULL DEFAULT '',
  `opening` varchar(255) NOT NULL DEFAULT '',
  `short_opening` varchar(255) NOT NULL DEFAULT '',
  `termination` varchar(20) NOT NULL DEFAULT '',
  `move_times` varchar(5000) NOT NULL DEFAULT '',
  `pgn` varchar(5000) NOT NULL DEFAULT '',
  `is_goofy` boolean NOT NULL DEFAULT 0,   
  `last_piece` char(1) NOT NULL DEFAULT 'P',
  PRIMARY KEY (`id`),
  UNIQUE KEY `gameid` (`gameid`),
  KEY `my_date` (`my_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
'''

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
def index(self):
    return render_template('index.html')

class ResultsPieChart:
    def __init__(self): 
        pass

    @app.route("/get_results_pie_chart")
    def get_results_pie_chart(self):
        return render_template("results_pie_chart.html")

    @app.route("/plot_results_pie_chart.png")
    def plot_results_pie_chart():
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

        white_results = { "wins": 0, "losses": 0, "draws": 0 }
        black_results = { "wins": 0, "losses": 0, "draws": 0 }
        
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
        
        # print("[INFO] ", white_results, black_results)

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

class NumberOfGamesPerMonth:
    def __init__(self):
        pass

    @app.route("/get_number_of_games_per_month")
    def get_number_of_games_per_month():
        return render_template("number_of_games_per_month.html")

    @app.route("/get_number_of_games_per_month")
    def plot_number_of_games_per_month():
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        return Response(buf.getvalue(), mimetype="image/png")

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5000)

