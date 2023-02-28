import pandas as pd
from pathlib import Path
from utils import replace_genre, fix_paths


fix_paths()
data_path = Path("../data/pitchfork.csv")
org_df = pd.read_csv(data_path, dtype={"releaseyear": int})
org_df.head()
# replace unknown genres
org_df["genre"] = org_df["genre"].apply(replace_genre)

# remove duplicate reviews
df = org_df.drop_duplicates(subset=["album", "reviewauthor"], keep="first").reset_index(
    drop=True
)

df.to_csv(r"../data/bucket/preprocessed-pitchfork.csv", index=True)
