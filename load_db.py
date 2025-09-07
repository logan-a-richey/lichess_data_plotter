#!/usr/bin/env python3

# chess file parser
# v2

import pymysql
import json
import sys
import re
from tqdm import tqdm 
from dataclasses import dataclass, asdict
from typing import List

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
batch = []
batch_size = 2500

SQL = """
insert into my_games (
    event, site, my_date, white, black, result, gameid,
    whiteelo, blackelo, whitetitle, blacktitle,
    whiteratingdiff, blackratingdiff,
    variant, timecontrol, eco, opening, short_opening, termination,
    move_times, pgn, is_goofy, last_piece
) values (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
) on duplicate key update
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
    short_opening = values(short_opening),
    termination = values(termination),
    move_times = values(move_times),
    pgn = values(pgn),
    is_goofy = values(is_goofy),
    last_piece = values(last_piece)
"""

@dataclass
class ChessGame:
    event: str = ""
    site: str = ""
    my_date: str = ""
    white: str = ""
    black: str = ""
    result: str = ""
    gameid: str = ""
    whiteelo: str = ""
    blackelo: str = ""
    whitetitle: str = ""
    blacktitle: str = ""
    whiteratingdiff: str = ""
    blackratingdiff: str = ""
    variant: str = ""
    timecontrol: str = ""
    eco: str = ""
    opening: str = ""
    short_opening: str = ""
    termination: str = ""
    move_times: str = ""
    pgn: str = ""
    is_goofy: bool = False
    last_piece: str = ""

def insert_batch(records: List[ChessGame]):
    if not records:
        return
    try:
        values = [(
            r.event, r.site, r.my_date, r.white, r.black, r.result, r.gameid,
            r.whiteelo, r.blackelo, r.whitetitle, r.blacktitle,
            r.whiteratingdiff, r.blackratingdiff,
            r.variant, r.timecontrol, r.eco, r.opening, r.short_opening, r.termination,
            r.move_times, r.pgn, r.is_goofy, r.last_piece
        ) for r in records]

        dbh.executemany(SQL, values)
        connection.commit()
    except Exception as e:
        print(f"Batch insert error: {e}")

def create_and_insert_game(record: dict):
    # do_db_insert(record)
    
    global batch
    global batch_size

    is_goofy_value =  1 if record.get("is_goofy") else 0

    game = ChessGame(
        event=record.get("event", ""),
        site=record.get("site", ""),
        my_date="{} {}".format(
            record.get("utcdate", "").replace('.', '-'),
            record.get("utctime", "")
        ),
        white=record.get("white", ""),
        black=record.get("black", ""),
        result=record.get("result", ""),
        gameid=record.get("gameid", ""),
        whiteelo=record.get("whiteelo", ""),
        blackelo=record.get("blackelo", ""),
        whitetitle=record.get("whitetitle", ""),
        blacktitle=record.get("blacktitle", ""),
        whiteratingdiff=record.get("whiteratingdiff", ""),
        blackratingdiff=record.get("blackratingdiff", ""),
        variant=record.get("variant", ""),
        timecontrol=record.get("timecontrol", ""),
        eco=record.get("eco", ""),
        opening=record.get("opening", ""),
        short_opening=record.get("short_opening", ""),
        termination=record.get("termination", ""),
        move_times=record.get("move_times", ""),
        pgn=record.get("pgn", ""),
        is_goofy=is_goofy_value,
        last_piece=record.get("last_piece", "P")
    )
    batch.append(game)
    if len(batch) >= batch_size:
        insert_batch(batch)
        batch = []

def main():
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
    
    global batch
    global batch_size 

    for line in tqdm(fh, total=total_lines, desc="Processing..."):
        line = line.strip()
        if not line: continue
        if line.startswith("#"): continue
        
        # metadata
        if line.startswith("["):
            match = re.match(r'^\s*\[(\w+)\s*"(.*?)".*$', line)
            if match:
                k, v = match.groups()
                k = k.lower()
                if ("elo" in k and "?" in v): v = 1200
                # new game - clear record
                if k == "event": record = {}
                record[k] = v
                if k == "opening":
                    first_word = v.split()[0]
                    record["short_opening"] = first_word
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
            
            is_goofy = False
            last_piece = 'P'
            
            # last_piece check:
            # last_move[-1] is the result string 0-1, 1/2-1/2, or 1-0
            last_move = simple_pgn.split()[-2].strip("+").strip("#")
            pieces = ['R', 'N', 'B', 'Q', 'K']
            for p in pieces:
                if p in last_move:
                    last_piece = p
            # castling (King move)
            if ("O-O" in last_move or "O-O-O" in last_move):
                last_piece = 'K'
            # pawn promotion
            if ("=" in last_move):
                last_piece = last_move[-1] 
                if last_piece not in pieces:
                    print("Unknown piece: {}. Setting to -> P.".format(last_piece))
                    last_piece = 'P'
            
            # is_goofy check
            pgn = record.get("pgn")
            if pgn:
                first_move = pgn.split()[1] 
                second_move = pgn.split()[2] 
                goofy_white_moves = ["a3", "a4", "b4", "f3", "g4", "h3", "h4", "Na3", "Nh3"]
                goofy_black_moves = ["a6", "a5", "b5", "f6", "g5", "h6", "h5", "Na6", "Nh6"]
                for m1, m2 in zip(goofy_white_moves, goofy_black_moves):
                    if (first_move == m1 or second_move == m2):
                        is_goofy = True 
            
            record["is_goofy"] = is_goofy
            record["last_piece"] = last_piece 
        
            create_and_insert_game(record) 

    # insert trailing partial batch
    if batch:
        insert_batch(batch)
    
    fh.close()
    connection.close()

if __name__ == "__main__":
    main()

