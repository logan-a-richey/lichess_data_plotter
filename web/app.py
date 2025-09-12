#!/usr/bin/env python3

from flask import Flask, Response, render_template, request

import json
import pymysql
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

my_username = "larichey"
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_results_pie_chart")
def get_results_pie_chart():
    ''' Return json to html '''

    # Load DB credentials
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()

    sql_white_result = "SELECT COUNT(*) FROM my_games WHERE (white=%s AND result=%s)"
    sql_black_result = "SELECT COUNT(*) FROM my_games WHERE (black=%s AND result=%s)"

    white_results = {}
    black_results = {}
    
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

@app.route("/plot_results_pie_chart.png")
def plot_results_pie_chart():
    ''' Return Matplotlib Image as Bytes ''' 

    white_results = {
        "wins": int(request.args.get("white_wins", 0)),
        "losses": int(request.args.get("white_losses", 0)),
        "draws": int(request.args.get("white_draws", 0))
    }
    black_results = {
        "wins": int(request.args.get("black_wins", 0)),
        "losses": int(request.args.get("black_losses", 0)),
        "draws": int(request.args.get("black_draws", 0))
    }

    # Plotting code unchanged...
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].pie(list(white_results.values()), labels=list(white_results.keys()), autopct="%1.1f%%")
    axs[0].set_title("As White")
    axs[1].pie(list(black_results.values()), labels=list(black_results.keys()), autopct="%1.1f%%")
    axs[1].set_title("As Black")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype="image/png")

@app.route("/get_games_per_month")
def get_games_per_month():
    ''' Return json to html '''

    # Load DB credentials
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

    return render_template(
        "games_per_month.html",
        months=months,
        counts=counts,
        zip=zip
    )

@app.route("/plot_games_per_month.png")
def plot_games_per_month():
    ''' Return image ''' 

    months = request.args.getlist("months")
    counts = [int(c) for c in request.args.getlist("counts")]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(months, counts, marker="o", linestyle="-", label="Games Played")
    ax.set_title(f"Games per Month for {my_username}")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Games")
    plt.xticks(rotation=45)

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return Response(buf.getvalue(), mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)

