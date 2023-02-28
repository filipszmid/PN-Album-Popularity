#  type: ignore
# pylint: disable-all
"""Data preprocessing"""

from pathlib import Path
import pandas as pd

from utils import replace_genre, fix_paths
from constants import PATH_TO_BUCKET

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

df.to_csv(PATH_TO_BUCKET + "preprocessed-pitchfork.csv", index=True)
