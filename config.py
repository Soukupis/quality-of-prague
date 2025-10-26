#TODO: App configuration (env vars, theme, etc.)
import os

class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 300))
    DATA_PATH = os.getenv("DATA_PATH", "data/dataset.csv")
    BOOTSTRAP_THEME = os.getenv("BOOTSTRAP_THEME", "CYBORG")