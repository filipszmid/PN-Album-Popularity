#  type: ignore
# pylint: disable-all
"""Data preprocessing"""

from pathlib import Path

import pandas as pd
from constants import PATH_TO_BUCKET
from utils import fix_paths, filter_none


class DataPreprocessingWorkflow:
    def __init__(self):
        fix_paths()
        self.data_path = Path("../data/pitchfork.csv")
        self.df_initial = pd.read_csv(self.data_path, dtype={"releaseyear": int})

    def replace_unknown_genres(self) -> None:
        self.df_initial["genre"] = self.df_initial["genre"].apply(filter_none)

    def remove_duplicate_reviews(self) -> pd.DataFrame:
        df = self.df_initial.drop_duplicates(
            subset=["album", "reviewauthor"], keep="first"
        ).reset_index(drop=True)
        return df

    def save_final_df(self, df: pd.DataFrame) -> None:
        df.to_csv(PATH_TO_BUCKET + "preprocessed-pitchfork.csv", index=True)


if __name__ == "__main__":
    workflow = DataPreprocessingWorkflow()
    workflow.replace_unknown_genres()
    df = workflow.remove_duplicate_reviews()
    workflow.save_final_df(df)
