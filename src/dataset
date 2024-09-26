import pandas as pd


def save_data(df: pd.DataFrame, filename: str) -> None:
    df.to_pickle(f"./data/interim/{filename}.pkl")


def recover_data(filename: str) -> pd.DataFrame:
    return pd.read_pickle("./data/interim/{filename}.pkl")
