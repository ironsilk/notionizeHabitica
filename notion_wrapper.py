import requests.exceptions

from utils import error_wrap


class Notion:
    def __init__(self, token):
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-02-22"

        })

    @error_wrap
    def get_db(self, db_name):
        """
        Returns the database object
        :param db_name:
        :return:
        """
        endpoint = f"https://api.notion.com/v1/databases/{db_name}"
        return self.s.get(endpoint)

    def get_all_db_items(self, db_name, start_cursor=None, results=None):
        """
        Returns a list of all items in a database
        :param results:
        :param start_cursor:
        :param db_name:
        :return:
        """
        @error_wrap
        def get_db_items(endpt, start_cursor=None):
            return self.s.post(endpt, data={}, params={'start_cursor': start_cursor})

        endpoint = f"https://api.notion.com/v1/databases/{db_name}/query"
        response = get_db_items(endpoint, start_cursor)
        if results:
            results.extend(response)
        else:
            results = response
        if response['next_cursor']:
            return self.get_all_db_items(db_name,
                                         response['next_cursor'],
                                         results
                                         )
        return results['results']


if __name__ == '__main__':
    from pprint import pprint
    from dotenv import load_dotenv
    import os
    load_dotenv()

    NOTION_TOKEN = os.getenv("NOTION_TOKEN")

    n = Notion(NOTION_TOKEN)
    n.get_db('db973d91ef46443baca7ad58f6a41ed4')
    pprint(n.get_all_db_items('db973d91ef46443baca7ad58f6a41ed4'))
