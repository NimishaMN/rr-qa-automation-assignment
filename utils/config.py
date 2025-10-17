import os

BASE_URL = os.getenv("BASE_URL", "https://tmdb-discover.surge.sh/")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
