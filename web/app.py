#!/usr/bin/env python3

from flask import Flask, Response, render_template, request

from dataclasses import dataclass, field

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

    sql_white_result = """
    SELECT COUNT(*) FROM my_games WHERE (white=%s AND result=%s)
    """
    sql_black_result = """
    SELECT COUNT(*) FROM my_games WHERE (black=%s AND result=%s)
    """

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
        zip=zip
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
        combined_rows=combined_rows
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

    return render_template(
        "adoption_data.html",
        adopted=adopted,
        been_adopted=been_adopted,
        top_adopted=top_adopted,
        top_been_adopted=top_been_adopted,
        my_username=my_username
    )

if __name__ == "__main__":
    app.run(debug=True)

