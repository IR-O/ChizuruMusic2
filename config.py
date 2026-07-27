from os import getenv

# Required Variables
API_ID = int(getenv("API_ID", "24208695"))
API_HASH = getenv("API_HASH", "fa96a7eb2dffe7f4cc8ba1399b68d24d")
BOT_TOKEN = getenv("BOT_TOKEN", "6365132039:AAF48I0KgZe4cyHmhMiRx_K634u6BEKApDQ")
SESSION_STRING = getenv("SESSION_STRING", "BQFxZTcAS6lmQ586CKMgSTQtRPUBonBJoTku2NN0vecIwGtqmz4N2bls5T-F37bWuMWEkexHvNtZF0XhodZsdiC6AOmD0CNm27zFkr1M8lCm-hzoGVlZ30aAgSu786py_6brN-lc6zmnflTu7am0Kx26Nl5YwP0slTZBaA9rHnaRy4nh3BgImP2we6SHej6PoqI6o22eyguy0XdsE9q1Jw7RhCF7egNk7fwd1npi0C5FuRJa9ArmnTsfwrWoWYp79BbkC6bkUGbNJ5kO0eTdRUbnZUkl4AxsdeiH7woS_DayoNUrpYjEjPNLRPsloXKjzcV0A47S1Ue0Q9vPDqfqCrq45ef_1wAAAAFI8Y5zAA")

# Optional Variables
OWNER_ID = int(getenv("OWNER_ID", "6045293810"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "6045293810").split()))
MONGO_URL = getenv("MONGO_URL", "mongodb+srv://Irobot:pikkuopbot@cluster0.tccq3ld.mongodb.net/?appName=Cluster0")
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1001772857132"))  # <-- Apni LOG GROUP ID daalein
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "300"))
START_IMG_URL = getenv("START_IMG_URL", "https://graph.org/file/5d73d3a4940ea78fbc7f3.jpg")
