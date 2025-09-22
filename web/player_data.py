# player_data.py 

from dataclasses import dataclass, field

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
