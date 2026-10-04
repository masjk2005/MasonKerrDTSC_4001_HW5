# Part 2: animate play 2735, game 2022100210 (PIT vs NYJ, Week 4)
# Animation code: nfl-tracks 1.3.2 by Mohammed Shammeer
#   https://pypi.org/project/nfl-tracks/
#   https://github.com/shammeer-s/nfl-tracks
# The library targets Big Data Bowl 2026 columns, so names are mapped to the
# 2024 names via NFLTracksConfig, and its ball-image helper (needs 2026-only
# ball_land_x/y and a web download) is disabled; the ball is drawn from the
# 'football' rows in the tracking data instead.
import matplotlib
matplotlib.use("Agg")
import os, getpass, socket, time
import importlib.metadata as md
import pandas as pd
from nfl import visuals
from nfl.config import NFLTracksConfig

GAME, PLAY = 2022100210, 2735
D = "/projects/class/spoa4001_u01/SportsTrackingTransformer/data/BigDataBowl_2024/"
f = D + "tracking_week_4.csv"
OUT = "play_2735_game_2022100210.gif"

print("User:", getpass.getuser(), "| Host:", socket.gethostname(), "| Run:", time.ctime())
print("nfl-tracks version:", md.version("nfl-tracks"))
print(f, "|", os.path.getsize(f), "bytes")

parts = []
for chunk in pd.read_csv(f, chunksize=500000):
    sub = chunk[(chunk.gameId == GAME) & (chunk.playId == PLAY)]
    if len(sub):
        parts.append(sub)
data = pd.concat(parts).sort_values(["frameId", "nflId"]).reset_index(drop=True)
print("Rows:", len(data), "| Frames:", data.frameId.min(), "to", data.frameId.max())
print("Clubs:", sorted(data.club.unique()))

cfg = NFLTracksConfig(game_col="gameId", play_col="playId", frame_col="frameId",
                      player_id_col="nflId", player_side_col="club")
colors = {"PIT": "#FFB612", "NYJ": "#125740", "football": "saddlebrown"}

visuals.Play._draw_ball_image = lambda self, ax: None

play = visuals.Play(data, GAME, PLAY, config=cfg)
play.animate(save=True, filename=OUT, kaggle=False, club_colors=colors, fps=10)

print("Saved:", OUT, os.path.getsize(OUT) if os.path.exists(OUT) else "NOT FOUND", "bytes")
