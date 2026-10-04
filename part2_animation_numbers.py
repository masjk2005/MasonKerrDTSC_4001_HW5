# Part 2 (extra): play 2735, game 2022100210, with jersey numbers on the dots
# Base library: nfl-tracks 1.3.2 by Mohammed Shammeer
#   https://pypi.org/project/nfl-tracks/
#   https://github.com/shammeer-s/nfl-tracks
# The library's animate() builds its update function internally, so this script
# repeats its steps (field, colorized frame data, FuncAnimation, PillowWriter)
# and adds one text label per player from the jerseyNumber column.
import matplotlib
matplotlib.use("Agg")
import os, getpass, socket, time
import importlib.metadata as md
import pandas as pd
from matplotlib import animation
from nfl import visuals
from nfl.config import NFLTracksConfig

GAME, PLAY = 2022100210, 2735
D = "/projects/class/spoa4001_u01/SportsTrackingTransformer/data/BigDataBowl_2024/"
f = D + "tracking_week_4.csv"
OUT = "play_2735_game_2022100210_numbers.gif"

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
text_colors = {"PIT": "black", "NYJ": "white"}

play = visuals.Play(data, GAME, PLAY, config=cfg)
frames = sorted(data.frameId.unique())

info = data.dropna(subset=["nflId", "jerseyNumber"]).drop_duplicates("nflId")
fig, ax = visuals.field()
scatter = ax.scatter([], [], s=150, zorder=3, clip_on=False)
labels = {}
for _, r in info.iterrows():
    t = ax.text(0, 0, str(int(r.jerseyNumber)), ha="center", va="center",
                fontsize=6, fontweight="bold", color=text_colors.get(r.club, "black"),
                zorder=5, clip_on=False)
    t.set_visible(False)
    labels[r.nflId] = t
print("Labeled players:", len(labels))

def update(i):
    fd = play._get_colorized_frame_data(frames[i], colors)
    scatter.set_offsets(fd[["x", "y"]])
    scatter.set_color(fd["plot_color"])
    scatter.set_sizes(fd["club"].eq("football").map({True: 40, False: 150}).to_numpy())
    pos = fd.dropna(subset=["nflId"]).set_index("nflId")
    for nid, t in labels.items():
        if nid in pos.index:
            t.set_position((pos.at[nid, "x"], pos.at[nid, "y"]))
            t.set_visible(True)
        else:
            t.set_visible(False)
    return (scatter, *labels.values())

ani = animation.FuncAnimation(fig, update, frames=len(frames), interval=100, blit=True)
ani.save(OUT, writer=animation.PillowWriter(fps=10))
print("Saved:", OUT, os.path.getsize(OUT) if os.path.exists(OUT) else "NOT FOUND", "bytes")
