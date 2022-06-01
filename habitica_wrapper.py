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


if __name__ == '__main__':
    from pprint import pprint
    from dotenv import load_dotenv
    import os
    load_dotenv()

    HABITICA_TOKEN = os.getenv("HABITICA_TOKEN")
    HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")

    n = Habitica(HABITICA_USER_ID, HABITICA_TOKEN)
    # pprint(n.get_tasks())
    pprint(n.get_task('a9ee3993-774a-43de-8b95-46aa490bde22'))
