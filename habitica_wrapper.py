import requests

from utils import error_wrap


class Habitica:
    def __init__(self, user_id, token):
        self.s = requests.Session()
        self.s.headers.update({
            "x-client": f"{user_id}-notionizeHabitica",
            "x-api-user": f"{user_id}",
            "x-api-key": f"{token}",
})

    @error_wrap
    def get(self, e):
        return self.s.get(e)

    @error_wrap
    def post(self, e, data=None, json=None):
        if data:
            return self.s.post(e, data=data)
        if json:
            return self.s.post(e, json=json)

    @error_wrap
    def put(self, e, data=None):
        return self.s.put(e, data=data)

    def get_tasks(self):
        """
        Returns user's tasks
        :param user:
        :return:
        """
        endpoint = "https://habitica.com/api/v3/tasks/user"
        return self.get(endpoint)['data']

    def get_task(self, task_alias):
        """
        Search for user's task by alias or taskID
        :param task_alias:
        :return:
        """
        endpoint = f"https://habitica.com/api/v3/tasks/{task_alias}"
        task = self.s.get(endpoint).json()
        if task['success']:
            return task
        else:
            return False

    def get_challenges(self):
        endpoint = "https://habitica.com/api/v3/challenges/user"
        challenges = self.s.get(endpoint, params={'page': 0, 'member': True}).json()
        if challenges['success']:
            return challenges
        else:
            return None

    def insert_habit(self, item):
        """
        Insert a habit, input must be in the form of:
        {
            'alias': '9c9750e6-d36b-403b-b92f-aa76bab62c9c',
            'attribute': 'Strength',
            'down': False,
            'text': 'Example Habit',
            'type': 'habit',
            'up': True
        }
        :param item:
        :return:
        """
        endpoint = 'https://habitica.com/api/v3/tasks/user'
        return self.post(endpoint, json=item)

    def insert_challenge_habit(self, challenge_id, item):
        """
        Insert a habit belonging to a challenge
        :param item:
        :return:
        """
        endpoint = f'https://habitica.com/api/v3/tasks/challenge/{challenge_id}'
        return self.post(endpoint, json=item)

    def update_habit(self, item_id, item):
        endpoint = f"https://habitica.com/api/v3/tasks/{item_id}"
        return self.put(endpoint, data=item)


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()

    HABITICA_TOKEN = os.getenv("HABITICA_TOKEN")
    HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")

    n = Habitica(HABITICA_USER_ID, HABITICA_TOKEN)

