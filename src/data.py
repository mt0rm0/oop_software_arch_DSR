import logging

import pandas as pd
import sqlite3

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataCleaningPipeline:
    def _load_data(self, filepath: str) -> None:
        # Load data
        df: pd.DataFrame = pd.read_csv(filepath)
        print("Data loaded successfully.")
        self.df = df

    def _validate_columns(self) -> None:
        # Validate columns
        if not all(
            col in self.df.columns for col in ["id", "name", "email", "signup_date"]
        ):
            print("Missing some columns...")

    def _clean_data(self) -> None:
        # Clean data - Data Cleaning
        self.df["email"] = self.df["email"].str.lower()
        self.df["signup_date"] = pd.to_datetime(self.df["signup_date"])
        self.df = self.df.dropna(subset=["id", "email"])
        print("Cleaning done.")

    def _transform_data(self) -> None:
        # Transform data - Feature Engineering
        self.df["days_since_signup"] = (
            pd.Timestamp.now() - self.df["signup_date"].dt.days
        )

    def _save_to_db(self) -> None:
        # Save to database
        conn = sqlite3.connect("data/cleaned_customers.db")
        df.to_sql("customers", conn, if_exists="replace", index=False)
        conn.close()
        print("Data written to database.")

    def run(self, filepath: str):
        # Run the pipeline
        self._load_data(filepath)
        self._validate_columns()
        self._clean_data()
        self._transform_data()
        self._save_to_db()

        print("Pipeline finished.")


if __name__ == "__main__":
    filepath = "data/customers.csv"
    dcp = DataCleaningPipeline()
    dcp.run(filepath)
