# Paths
DATA_PATH = "./data/"
PARTIAL_PATH = ["raw/", "interim/", "processed/", "external/"]

RAW_DATA_PATH, INTERIM_DATA_PATH, PROCESSED_DATA_PATH, EXTERNAL_DATA_PATH = [
    DATA_PATH + item for item in PARTIAL_PATH
]
