import pandas as pd, getpass, socket, os, time, hashlib

D = "/projects/class/spoa4001_u01/SportsTrackingTransformer/data/BigDataBowl_2024/"
print("User:", getpass.getuser(), "| Host:", socket.gethostname(), "| Run:", time.ctime())

for f in ["games.csv", "games2.csv"]:
    p = D + f
    md5 = hashlib.md5(open(p, "rb").read()).hexdigest()
    print(f"{p} | {os.path.getsize(p)} bytes | modified {time.ctime(os.path.getmtime(p))} | md5 {md5}")

a = pd.read_csv(D + "games.csv").set_index("gameId")
b = pd.read_csv(D + "games2.csv").set_index("gameId").reindex(a.index)

score_cols = ["homeFinalScore", "visitorFinalScore"]
changed = a.index[(a[score_cols] != b[score_cols]).any(axis=1)]
print("\nGames whose scores differ:", list(changed))

cols = ["week", "homeTeamAbbr", "visitorTeamAbbr"] + score_cols
print("\nOriginal (games.csv):\n", a.loc[changed, cols].to_string())
print("\nModified (games2.csv):\n", b.loc[changed, cols].to_string())
