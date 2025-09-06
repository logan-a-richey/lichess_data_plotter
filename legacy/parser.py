#!/usr/bin/env python3

# chess file parser

import pymysql

import json
import sys
import re
from tqdm import tqdm 

# load db creditials
dsn = {}
try:
    with open("my_dsn.json", "r") as file:
        dsn = json.load(file)
except Exception as e:
    print("Could not load dsn : {}".format(e))

# global db connection
connection = pymysql.connect(**dsn)
dbh = connection.cursor()


# insert record into database
def do_db_insert(record: dict):
    try:
        sql = """
        insert into my_games (
            event,
            site,
            my_date,
            white,
            black,
            result,
            gameid,
            whiteelo,
            blackelo,
            whitetitle,
            blacktitle,
            whiteratingdiff,
            blackratingdiff,
            variant,
            timecontrol,
            eco,
            opening,
            termination,
            move_times,
            pgn
        )
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        on duplicate key update 
            event = values(event),
            site = values(site),
            my_date = values(my_date),
            white = values(white),
            black = values(black),
            result = values(result),
            gameid = values(gameid),
            whiteelo = values(whiteelo),
            blackelo = values(blackelo),
            whitetitle = values(whitetitle),
            blacktitle = values(blacktitle),
            whiteratingdiff = values(whiteratingdiff),
            blackratingdiff = values(blackratingdiff),
            variant = values(variant),
            timecontrol = values(timecontrol),
            eco = values(eco),
            opening = values(opening),
            termination = values(termination),
            move_times = values(move_times),
            pgn = values(pgn)
        """
        new_time = "{} {}".format(
            record.get("utcdate", "").replace('.', '-'),
            record.get("utctime", "")
        )

        my_values = (
            record.get("event", ""),
            record.get("site", ""),
            new_time,
            record.get("white", ""),
            record.get("black", ""),
            record.get("result", ""),
            record.get("gameid", ""),
            record.get("whiteelo", ""),
            record.get("blackelo", ""),
            record.get("whitetitle", ""),
            record.get("blacktitle", ""),
            record.get("whiteratingdiff", ""),
            record.get("blackratingdiff", ""),
            record.get("variant", ""),
            record.get("timecontrol", ""),
            record.get("eco", ""),
            record.get("opening", ""),
            record.get("termination", ""),
            record.get("move_times", ""),
            record.get("pgn", "")
        )
        
        dbh.execute(sql, my_values)
        connection.commit()
        # print("Inserted data w/ id: {}".format(dbh.lastrowid))

    except Exception as e:
        print("Error: {}".format(e))

def parse_input_file():
    if len(sys.argv) < 2:
        print("Usage: python parser.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    total_lines = 0 
    with open(filename, 'r', encoding="utf-8") as f:
        total_lines = sum(1 for line in f) # count lines

    try:
        fh = open(filename, 'r', encoding="utf-8")
    except Exception as e:
        print(f"Could not open file. {e}")
        sys.exit(1)

    record = {}

    print("reading ...")

    
    for line in tqdm(fh, total=total_lines, desc="Processing..."):
        # strip leading/trailing whitespace
        line = line.strip()

        # skip empty lines
        if not line:
            continue

        # skip comment lines
        if line.startswith("#"):
            continue

        # metadata
        if line.startswith("["):
            match = re.match(r'^\s*\[(\w+)\s*"(.*?)".*$', line)
            if match:
                k, v = match.groups()
                
                # sanitize inputs
                k = k.lower()
                if ("elo" in k and "?" in v):
                    v = 1200

                # new game - clear record
                if k == "event":
                    record = {}

                record[k] = v

            continue

        # pgn data
        if line.startswith("1."):
            # find all clock values
            clock_values = re.findall(r'\{\s*\[%clk\s*(\d+:\d+:\d+)\]\s*\}', line)

            # update line with clocks + black move markers removed
            simple_pgn = re.sub(r'\{.*?\}', '', line)    # remove {...}
            simple_pgn = re.sub(r'\d+\.{3}', '', simple_pgn)  # remove "1..."
            simple_pgn = re.sub(r'\s+', ' ', simple_pgn).strip()

            move_times = "[" + ", ".join(clock_values) + "]"

            record["move_times"] = move_times
            record["pgn"] = simple_pgn
            
            do_db_insert(record)
            continue

    fh.close()
    connection.close()

if __name__ == "__main__":
    parse_input_file()

