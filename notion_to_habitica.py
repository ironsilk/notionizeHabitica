from notion_wrapper import Notion
from habitica_wrapper import Habitica
import os
from dotenv import load_dotenv
import dateutil as d_util
from pprint import pprint

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HABITICA_TOKEN = os.getenv("HABITICA_TOKEN")
HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")


class Sync():
    def __init__(self, notion_token, habitica_token, habitica_user_id):
        self.notion = Notion(notion_token)
        self.habitica = Habitica(habitica_user_id, habitica_token)
        self.mandatory_fields = [
            'Name',
            'Category',
            'TaskType',
        ]

    def item_is_incomplete(self, item):
        for field in self.mandatory_fields:
            if not item['properties'][field][item['properties'][field]['type']] \
                    and item['properties'][field]['type'] != 'checkbox':
                return True
        return False

    def sync(self):
        notion_items = self.notion.get_all_db_items('db973d91ef46443baca7ad58f6a41ed4')
        # Filter out those with incomplete data:
        notion_items = [x for x in notion_items if not self.item_is_incomplete(x)]
        # Update each item in Habitica if necessary
        for item in notion_items:
            if item['properties']['TaskType'] == 'Habit':
                habitica_item = self.habitica.get_task(item['id'])
                if habitica_item:
                    if d_util.parse(item['last_edited_time']) > d_util.parse(habitica_item['updatedAt']):
                        # Update Habitica item
                        pass
                    else:
                        # Nothing's changed, pass
                        pass
                else:
                    # New item, insert into Habitica.
                    pass
            elif item['properties']['TaskType'] == 'Daily':
                pass
            elif item['properties']['TaskType'] == 'To Do':
                pass

        return notion_items


if __name__ == '__main__':
    s = Sync(NOTION_TOKEN, HABITICA_TOKEN, HABITICA_USER_ID)
    s.sync()
