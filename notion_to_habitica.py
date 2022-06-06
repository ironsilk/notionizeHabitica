from notion_wrapper import Notion
from habitica_wrapper import Habitica
import os
from dotenv import load_dotenv
import dateutil.parser as d_util
from utils import setup_logger

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
HABITICA_TOKEN = os.getenv("HABITICA_TOKEN")
HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")

TYPE_MAPPING = {
    'Habit': 'habit',
    'To Do': 'todo',
    'Daily': 'daily',
}

DAYS = {
    'Sunday': 'su',
    'Monday': 'm',
    'Tuesday': 't',
    'Wednesday': 'w',
    'Thursday': 'th',
    'Friday': 'f',
    'Saturday': 's'
}

DIFFICULTY_MAPPING = {
    'Trivial': '0.1',
    'Easy': '1',
    'Medium': '1.5',
    'Hard': '2',
}


class Sync():
    def __init__(self, notion_token, habitica_token, habitica_user_id):
        self.notion = Notion(notion_token)
        self.habitica = Habitica(habitica_user_id, habitica_token)
        self.mandatory_fields = [
            'Name',
            'TaskType',
        ]
        self.logger = setup_logger("NotionToHabitica")

    def item_is_incomplete(self, item):
        # Don't pass references to other objects columns.

        for field in self.mandatory_fields:
            if not item['properties'][field][item['properties'][field]['type']] \
                    and item['properties'][field]['type'] != 'checkbox':
                return True
        return False

    def parse_repeat_days(self, days):
        days = [DAYS[x['name']] for x in days]
        skipped_days = [x for x in DAYS.values() if x not in days]
        return {x: False for x in skipped_days}

    def make_habitica_item(self, notion_item, type):

        item = {
            'type': type,
            'text': notion_item['properties']['Name']['title'][0]['plain_text'],
            'frequency': notion_item['properties']['Frequency']['select']['name'].lower(),
            'attribute': notion_item['properties']['Attribute']['select']['name'][:3].lower(),
            'everyX': notion_item['properties']['RepeatEvery']['number'],
            'startDate': notion_item['properties']['StartDate']['date']['start'] if
            notion_item['properties']['StartDate']['date'] else None,
            'priority': DIFFICULTY_MAPPING[notion_item['properties']['Difficulty']['select']['name']],
            # 'tags': 'to_implement?',  # TODO category would be nice
        }
        if type == 'habit':
            item['up'] = 1 if notion_item['properties']['Up']['checkbox'] else 0
            item['down'] = 1 if notion_item['properties']['Down']['checkbox'] else 0

        elif type == 'daily':
            freq = item['frequency']
            if freq == 'weekly':
                item['repeat'] = self.parse_repeat_days(notion_item['properties']['WeeklyRepeatOn']['multi_select'])
            elif freq == 'monthly':
                if notion_item['properties']['MonthlySameWeekday']['checkbox']:
                    item['weeksOfMonth'] = True
                else:
                    item['daysOfMonth'] = True

        elif type == 'todo':
            item['date'] = item['startDate']
        else:
            pass  # Return error, not implemented.
        return item

    def sync_habitca_challenges(self):
        """
        Updates select options from Notion column Challenge with
        all available challenges in Habitica
        :return:
        """
        self.logger.info("Syncing habitica challenges...")
        challenge_names = self.habitica.get_challenges()
        if challenge_names:
            challenge_names = [x['shortName'] for x in challenge_names['data']]
            payload = {
                "properties": {
                    "ChallengeName": {
                        "select": {
                            'options': [{'name': x} for x in challenge_names]
                        }
                    },
                }}
            self.notion.update_database(NOTION_DATABASE_ID, payload)
            self.logger.info("Done!")
        else:
            self.logger.info("No challenges found.")

    def sync_tasks(self):
        self.logger.info("Syncing tasks...")
        notion_items = self.notion.get_all_db_items(NOTION_DATABASE_ID)
        # Filter out those with incomplete data:
        notion_items = [x for x in notion_items if not self.item_is_incomplete(x)]
        # Update each item in Habitica if necessary
        for notion_item in notion_items:
            item_type = TYPE_MAPPING[notion_item['properties']['TaskType']['select']['name']]
            # if notion_item['properties']['TaskType']['select']['name'] == 'Habit':
            try:
                habitica_item = self.habitica.get_task(
                    notion_item['properties']['habitica_id']['rich_text'][0]['plain_text'])
            except IndexError:
                habitica_item = None
            if habitica_item:
                # Update Habitica item
                if d_util.parse(notion_item['last_edited_time']) > d_util.parse(habitica_item['data']['updatedAt']):
                    self.logger.info(f"Updating notion item "
                                     f"|{notion_item['properties']['Name']['title'][0]['plain_text']}| "
                                     )
                    item = self.make_habitica_item(notion_item, item_type)
                    self.habitica.update_habit(
                        notion_item['properties']['habitica_id']['rich_text'][0]['plain_text'],
                        item
                    )
                else:
                    # Nothing's changed, pass
                    self.logger.info(f"Skipping notion item "
                                     f"|{notion_item['properties']['Name']['title'][0]['plain_text']}| "
                                     f":  no changes")
            else:
                # New item, insert into Habitica.
                if notion_item['properties']['ChallengeName']['select']:
                    # Get challenges to fetch the ChallengeID
                    challenges = self.habitica.get_challenges()
                    idd = [x for x in challenges['data'] if
                           x['shortName'] == notion_item['properties']['ChallengeName']['select']['name']][0]['id']
                    result = self.habitica.insert_challenge_habit(idd, self.make_habitica_item(notion_item, item_type))
                else:
                    result = self.habitica.insert_habit(self.make_habitica_item(notion_item, item_type))
                # And update item in Notion
                if result['success']:
                    payload = {
                        "properties": {
                            "habitica_id": {
                                "rich_text": [
                                    {
                                        "text": {
                                            "content": result['data']['_id']
                                        }
                                    }
                                ]
                            },
                        }}

                    self.notion.update_page(notion_item['id'], payload)
                else:
                    self.logger.error(f"Had trouble inserting habit into Habitica. Please investigate: "
                                      f"{result.json()}")

        self.logger.info("Done!")
        return notion_items

    def sync_all(self):
        self.sync_habitca_challenges()
        self.sync_tasks()


if __name__ == '__main__':
    s = Sync(NOTION_TOKEN, HABITICA_TOKEN, HABITICA_USER_ID)
    s.sync_all()
