import os
import traceback
from time import sleep

from dotenv import load_dotenv

from notion_to_habitica import Sync

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
HABITICA_TOKEN = os.getenv("HABITICA_TOKEN")
HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")


if __name__ == '__main__':
    service = Sync(NOTION_TOKEN, HABITICA_TOKEN, HABITICA_USER_ID)
    while True:
        try:
            service.sync_all()
        except Exception as e:
            service.logger.error(f"Oups: {traceback.format_exc()}")
        service.logger.info("Sleeping 1 minute")
        sleep(60)
