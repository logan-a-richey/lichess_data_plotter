## ideas for plot 

1. pie chart: opening choice for white, black
2. stacked bar graph: number of games per month
3. whisker plot: bullet rating per month, per season
4. line plot: estimated casual bullet rating (elo formula) vs actual bullet rating
5. html table: adoption data, been adopted data
6. bar chart: game length (number of moves) {grouped in ranges of 10}
7. average opponent rating per month; whisker opp rating (low, low mid, med, high mid, high)
8. pie chart : checkmating piece, terminating piece (p, n, b, r, q, k)
9. pie chart variant type 
10. html tables:
    top 10 highest rated bullet wins 
    top 10 highest casual bullet wins
    top 10 highest rated titled bullet wins
    top 10 highest casual titled bullet wins
    html table: link to worst losses
    html table: link to goofiest wins
    html table: link to goofiest losses

# note:
- terminating move is the 2nd-to-last word of the pgn field.
- ending in # if checkmate.
- king can also be O-O or O-O-O
- promotion is the name of the promoting type. For example: e8=R is R. h8=Q is Q.

# goofy games;
games starting in a3, a4, h3, h4, b4, g4, f3, Na3, Nh3
games starting in ...a6 ...a5, ...h6, ...h5, ...b5, ...g5, ...f6, ...Na6, ...Nh6

# TODO 
step 0:
* upload new games file, db parses, reload page, show index dashboard
* extend data to other players 
* combobox for previous player data files 

graph 1: openings
* pie charts not side by side

graph 2: games per month
* chart width needs to fill width of div

graph 3: most common openings
* no css
* need to separate table
* triple bar chart for opening to show win-loss-draw for each
* p usr was most successful at x opening, least to y opening

graph 4: adoption
* no css
* remove bar chart

graph 5: top wins
* no css
* back at bottom 

graph 6: casual rating simulation
* plot differently? 
* datasets: [highest, avg, lowest] per month
* make line plot width 100%
* p text to explain data. 

graph 7: termination type (ie checkmate with pawn, rook, king, etc.)
* not impl
