import requests
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()

HABITICA_TOKEN = os.getenv("HABITICA_TOKEN")
HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")
DB_API = "https://habitica.com/export/userdata.json"
DB_API = "https://habitica.com/api/v3/tasks/user"


print(HABITICA_TOKEN)
headers = {
    "x-client": f"{HABITICA_USER_ID}-notionizeHabitica",
    "x-api-user": f"{HABITICA_USER_ID}",
    "x-api-key": f"{HABITICA_TOKEN}",
}

pprint(requests.get(DB_API, headers=headers).json())
