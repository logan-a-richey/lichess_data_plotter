#!/usr/bin/env python3

from flask import Flask, Response, render_template, request, redirect, url_for, jsonify
from dataclasses import dataclass, field
import json
import pymysql
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# matplotlib.use('Agg')
# from pandas import to_datetime
from collections import defaultdict
from datetime import datetime
import os 
import subprocess 

from elo_calc import update_elo 

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
WORK_FOLDER = "work"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(WORK_FOLDER, exist_ok=True)

# default global variable
my_username = "larichey"

################################################################################
# File upload form and loading methods 

@app.route("/")
def index():
    return render_template("index.html")  # upload form

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Paths for done flag
    done_file = os.path.join(WORK_FOLDER, "done.txt")

    # If leftover done.txt exists, clear it
    if os.path.exists(done_file):
        os.remove(done_file)

    # Run parser in a new process (non-blocking)
    subprocess.Popen(
        ["python3", "db_loader.py", filepath, done_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

    return redirect(url_for("loading"))

@app.route("/loading")
def loading():
    return render_template("loading.html")

@app.route("/status")
def status():
    done_file = os.path.join(WORK_FOLDER, "done.txt")
    if os.path.exists(done_file):
        return jsonify({"status": "done"})
    else:
        return jsonify({"status": "processing"})

def get_most_common_user():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()

    sql_white_result = "SELECT white, count(white) as k from my_games group by white order by k desc limit 1"
    sql_black_result = "SELECT black, count(black) as k from my_games group by black order by k desc limit 1"
    
    dbh.execute(sql_white_result)
    white_name, white_count = dbh.fetchone()

    dbh.execute(sql_black_result)
    black_name, black_count = dbh.fetchone()
    
    connection.close()

    if white_count >= black_count:
        return white_name
    else:
        return black_name

################################################################################
# Dashboard methods 

@app.route("/dashboard")
def dashboard():
    my_username = get_most_common_user()

    return render_template(
        "dashboard.html",
        my_username=my_username
    )

@app.route("/get_results_pie_chart")
def get_results_pie_chart():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()

    sql_white_result = "SELECT COUNT(*) FROM my_games WHERE (white=%s AND result=%s) "
    sql_black_result = "SELECT COUNT(*) FROM my_games WHERE (black=%s AND result=%s) "

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
        black_results=black_results,
        my_username=my_username
    )

@app.route("/get_games_per_month")
def get_games_per_month():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()

    sql = """
        SELECT YEAR(my_date) AS year, MONTH(my_date) AS month, COUNT(*) AS games
        FROM my_games
        WHERE white = %s OR black = %s
        GROUP BY year, month
        ORDER BY year, month;
    """
    dbh.execute(sql, (my_username, my_username))
    rows = dbh.fetchall()
    connection.close()

    # Restructure into a dict: { year: {month: count} }
    results = {}
    max_games = 0

    for year, month, games in rows:
        if year not in results:
            results[year] = {m: 0 for m in range(1, 13)}  # init all months to 0
        results[year][month] = games
        if games > max_games:
            max_games = games

    # Prepare for Chart.js (flat lists of months/games)
    months = [f"{r[0]}-{r[1]:02d}" for r in rows]
    counts = [r[2] for r in rows]

    return render_template(
        "games_per_month.html",
        results=results,
        months=months,
        counts=counts,
        max_games=max_games if max_games > 0 else 1, #avoid div by zero
        zip=zip,
        my_username=my_username
    )

@app.route("/get_most_common_openings")
def get_most_common_openings():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()

    # Top 10 White openings
    sql_white = """
        SELECT short_opening, COUNT(*) AS cnt
        FROM my_games
        WHERE white = %s
        GROUP BY short_opening
        ORDER BY cnt DESC
        LIMIT 10
    """

    dbh.execute(sql_white, (my_username,))
    white_rows = dbh.fetchall()

    # Top 10 Black openings
    sql_black = """
        SELECT short_opening, COUNT(*) AS cnt
        FROM my_games
        WHERE black = %s
        GROUP BY short_opening
        ORDER BY cnt DESC
        LIMIT 10
    """
    dbh.execute(sql_black, (my_username,))
    black_rows = dbh.fetchall()

    connection.close()

    # white_rows = list(white_rows)
    # black_rows = list(black_rows)

    # Separate into lists for Chart.js
    white_labels = [row[0] for row in white_rows]
    white_counts = [row[1] for row in white_rows]
    black_labels = [row[0] for row in black_rows]
    black_counts = [row[1] for row in black_rows]

    # Pad table rows to max(10) so both columns align
    max_len = max(len(white_rows), len(black_rows))
    
    # white_rows_padded = white_rows + [("", 0)] * (max_len - len(white_rows))
    # black_rows_padded = black_rows + [("", 0)] * (max_len - len(black_rows))

    white_rows_padded = white_rows + (("", 0),) * (max_len - len(white_rows))
    black_rows_padded = black_rows + (("", 0),) * (max_len - len(black_rows))

    combined_rows = list(zip(range(1, max_len+1), white_rows_padded, black_rows_padded))

    return render_template(
        "most_common_openings.html",
        white_labels=white_labels,
        white_counts=white_counts,
        black_labels=black_labels,
        black_counts=black_counts,
        combined_rows=combined_rows,
        my_username=my_username
    )

@dataclass 
class PlayerData:
    name: str
    highest_elo: int = 0
    current_win_streak: int = 0
    current_lose_streak: int = 0
    num_win_streaks: int = 0
    num_lose_streaks: int = 0
    win_sites: list[str] = field(default_factory=list)
    lose_sites: list[str] = field(default_factory=list)

@app.route("/get_adoption_data")
def get_adoption_data():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor()
    
    sql = """
    SELECT id, white, black, result, site, whiteelo, blackelo
    FROM my_games
    WHERE white=%s OR black=%s
    ORDER BY my_date ASC
    """
    
    dbh.execute(sql, (my_username, my_username) )
    rows = dbh.fetchall()

    connection.close()
    
    players = {}  # key: opponent name, value: PlayerData

    for row in rows:
        game_id, white, black, result, site, whiteelo, blackelo = row
        
        # Determine opponent and perspective
        if white == my_username:
            opponent = black
            my_color = "white"
            my_elo = whiteelo
            opp_elo = blackelo
        else:
            opponent = white
            my_color = "black"
            my_elo = blackelo
            opp_elo = whiteelo
        
        if opponent not in players:
            players[opponent] = PlayerData(name=opponent, highest_elo=opp_elo)
        else:
            players[opponent].highest_elo = max(players[opponent].highest_elo, opp_elo)
        
        pdata = players[opponent]
        
        # Determine win/loss/draw for my_username
        if result == "1-0":
            my_win = white == my_username
        elif result == "0-1":
            my_win = black == my_username
        else:  # draw
            my_win = None
        
        if my_win is True:
            # Increment win streak, reset lose streak
            pdata.current_win_streak += 1
            pdata.current_lose_streak = 0
            
            if pdata.current_win_streak >= 10:
                pdata.num_win_streaks += 1
                pdata.win_sites.append(site)
                pdata.current_win_streak = 0
        elif my_win is False:
            # Increment lose streak, reset win streak
            pdata.current_lose_streak += 1
            pdata.current_win_streak = 0
            
            if pdata.current_lose_streak >= 10:
                pdata.num_lose_streaks += 1
                pdata.lose_sites.append(site)
                pdata.current_lose_streak = 0
        else:
            # draw resets both streaks
            pdata.current_win_streak = 0
            pdata.current_lose_streak = 0
    
    # prepare data for tables:
    adopted = [p for p in players.values() if p.num_win_streaks > 0]
    adopted.sort(key=lambda x: x.num_win_streaks, reverse=True)

    # Players who adopted my_username
    been_adopted = [p for p in players.values() if p.num_lose_streaks > 0]
    been_adopted.sort(key=lambda x: x.num_lose_streaks, reverse=True)
    
    top_adopted = adopted[:10]
    top_been_adopted = been_adopted[:10]

    scatter_adopted = [{"x": p.highest_elo, "y": p.num_win_streaks, "name": p.name} for p in top_adopted]
    scatter_been_adopted = [{"x": p.highest_elo, "y": p.num_lose_streaks, "name": p.name} for p in top_been_adopted]

    return render_template(
        "adoption_data.html",
        adopted=adopted,
        been_adopted=been_adopted,
        top_adopted=top_adopted,
        top_been_adopted=top_been_adopted,
        scatter_adopted=scatter_adopted,
        scatter_been_adopted=scatter_been_adopted,
        my_username=my_username
    )
 
@app.route("/get_top_wins")
def get_top_wins():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn)
    dbh = connection.cursor(pymysql.cursors.DictCursor)

    sql = """
    SELECT id, event, site, white, black, result, 
           whiteelo, blackelo, whitetitle, blacktitle, 
           whiteratingdiff, blackratingdiff, my_date
    FROM my_games
    WHERE white=%s OR black=%s
    ORDER BY my_date ASC
    """
    dbh.execute(sql, (my_username, my_username))
    rows = dbh.fetchall()
    connection.close()

    top_rated_wins = []
    top_rated_titled_wins = []
    top_casual_wins = []
    top_casual_titled_wins = []

    for g in rows:
        # Am I white or black?
        am_white = g["white"] == my_username
        opp_name = g["black"] if am_white else g["white"]
        opp_elo = g["blackelo"] if am_white else g["whiteelo"]
        opp_title = g["blacktitle"] if am_white else g["whitetitle"]

        # Did I win?
        i_won = (am_white and g["result"] == "1-0") or \
                (not am_white and g["result"] == "0-1")
        if not i_won:
            continue

        # Rated vs casual
        is_casual = ("casual" in g["event"].lower()) or \
                    (not g["whiteratingdiff"] and not g["blackratingdiff"])

        # Titled opponent?
        is_titled = bool(opp_title.strip())

        record = {
            "opp_name": opp_name,
            "opp_elo": opp_elo,
            "opp_title": opp_title,
            "site": g["site"],
            "date": g["my_date"],
            "game_id": g["id"]
        }

        if not is_casual and not is_titled:
            top_rated_wins.append(record)
        elif not is_casual and is_titled:
            top_rated_titled_wins.append(record)
        elif is_casual and not is_titled:
            top_casual_wins.append(record)
        else:
            top_casual_titled_wins.append(record)

    # Sort each category by opp_elo, highest first, and take top 50
    num_games = 100
    key_sort = lambda r: r["opp_elo"]
    top_rated_wins = sorted(top_rated_wins, key=key_sort, reverse=True)[:num_games]
    top_rated_titled_wins = sorted(top_rated_titled_wins, key=key_sort, reverse=True)[:num_games]
    top_casual_wins = sorted(top_casual_wins, key=key_sort, reverse=True)[:num_games]
    top_casual_titled_wins = sorted(top_casual_titled_wins, key=key_sort, reverse=True)[:num_games]

    return render_template(
        "top_wins.html",
        top_rated_wins=top_rated_wins,
        top_rated_titled_wins=top_rated_titled_wins,
        top_casual_wins=top_casual_wins,
        top_casual_titled_wins=top_casual_titled_wins,
        my_username=my_username
    )

def do_matplot_rating_sim():
    with open("my_dsn.json") as file:
        dsn = json.load(file)
    connection = pymysql.connect(**dsn)
    dbh = connection.cursor(pymysql.cursors.DictCursor)
    sql = """
    SELECT id, event, site, white, black, result, 
           whiteelo, blackelo, my_date
    FROM my_games
    WHERE 
        (white=%s OR black=%s) 
        AND (white not like %s) 
        AND (black not like %s) 
        AND event='casual bullet game'
    ORDER BY my_date ASC
    """
    dbh.execute(sql, (my_username, my_username, '%lichess AI%', '%lichess AI%') )
    rows = dbh.fetchall()
    connection.close()
    
    test_elo = 1500 # starting rating
    times = []
    ratings = []

    for g_idx, g in enumerate(rows):
        usr_elo = 1200
        opp_elo = 1200
        # Rated vs casual
        is_casual: bool = ("casual" in g["event"].lower()) or \
                    (not g["whiteratingdiff"] and not g["blackratingdiff"])
        usr_is_white = g["white"] == my_username 
        usr_result = "draw"
        if usr_is_white:            
            usr_elo = g["whiteelo"]
            opp_elo = g["blackelo"]
            if g["result"] == "1-0":
                usr_result = "win"
            elif g["result"] == "0-1":
                usr_result = "loss"
            else:
                usr_result = "draw"
        else:
            # usr_is_black    
            opp_elo = g["whiteelo"]
            usr_elo = g["blackelo"]
            if g["result"] == "0-1":
                usr_result = "win"
            elif g["result"] == "1-0":
                usr_result = "loss"
            else:
                usr_result = "draw"
        test_elo, _ = update_elo(test_elo, opp_elo, usr_result)
        # x axis (time), y axis (rating)
        # times.append(g["my_date"])
        times.append(g_idx)
        ratings.append(test_elo)
    
    max_elo = max(ratings)
    avg_elo = int(sum(ratings) / len(ratings))
    print("[INFO] max casual elo =~ {}".format(max_elo))
    print("[INFO] avg casual elo =~ {}".format(avg_elo))
    
    # DEBUG
    plt.plot(times, ratings)
    plt.ylabel("Elo")
    plt.title("Casual Rating Sim")
    plt.show()
    return 

@app.route("/get_rating_simulation")
def get_rating_simulation():
    with open("my_dsn.json") as file:
        dsn = json.load(file)

    connection = pymysql.connect(**dsn, cursorclass=pymysql.cursors.DictCursor)
    dbh = connection.cursor()

    sql = """
    SELECT white, black, result, whiteelo, blackelo, my_date
    FROM my_games
    WHERE 
        (white=%s OR black=%s) 
        AND event='casual bullet game'
    ORDER BY my_date ASC
    """
    dbh.execute(sql, (my_username, my_username))
    rows = dbh.fetchall()
    connection.close()

    monthly_elos = defaultdict(list)  # { "YYYY-MM": [elos...] }
    test_elo = 1500
    k_factor = 10
    bot_name = "lichess AI"
    
    for g in rows:
        if bot_name in g["white"] or bot_name in g["black"]:
            continue
        usr_is_white = g["white"] == my_username
        opp_elo = g["blackelo"] if usr_is_white else g["whiteelo"]
        usr_result = "draw"

        if usr_is_white:
            if g["result"] == "1-0": usr_result = "win"
            elif g["result"] == "0-1": usr_result = "loss"
        else:
            if g["result"] == "0-1": usr_result = "win"
            elif g["result"] == "1-0": usr_result = "loss"

        # Simulate Elo
        test_elo, _ = update_elo(test_elo, opp_elo, usr_result, k_factor)

        # Group by YYYY-MM
        # month = to_datetime(g["my_date"]).strftime("%Y-%m")
        month = g["my_date"].strftime("%Y-%m")
        monthly_elos[month].append(test_elo)

    # Aggregate per month
    labels = []
    highs, avgs, lows = [], [], []

    for month in sorted(monthly_elos.keys()):
        elos = monthly_elos[month]
        labels.append(month)
        highs.append(max(elos))
        avgs.append(int(sum(elos) / len(elos)))
        lows.append(min(elos))

    # Debug plot in matplotlib
    # plt.plot(labels, highs, color="green", label="Monthly High")
    # plt.plot(labels, avgs, color="gold", label="Monthly Avg")
    # plt.plot(labels, lows, color="red", label="Monthly Low")
    # plt.ylabel("Elo")
    # plt.title("Casual Rating Sim (Monthly)")
    # plt.xticks(rotation=45)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    
    highest_test_elo = max(highs)
    average_test_elo = int(sum(avgs) / len(avgs))

    # Pass to template
    return render_template(
        "rating_simulation.html",
        labels=labels,
        highs=highs,
        avgs=avgs,
        lows=lows,
        highest_test_elo=highest_test_elo,
        average_test_elo=average_test_elo,
        my_username=my_username
    )

if __name__ == "__main__":
    app.run(debug=False)

