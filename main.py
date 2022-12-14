import requests
from datetime import datetime
import time


class SOFManager:
    def __init__(self):
        self.host = 'https://stackoverflow.com/'

    def unix_timestamp_2_days_ago(self):
        date_time = datetime.now()
        date_time = datetime(date_time.year,
                             date_time.month,
                             date_time.day - 2)

        return time.mktime(date_time.timetuple())

    def get_questions(self, search_uri):
        response = requests.get('https://api.stackexchange.com/' + search_uri)
        response_code = response.status_code
        json_response = response.json()
        if response_code == 200:
            for item in json_response['items']:
                print(f"Title: {item['title']}\n"
                      f"Date: {datetime.utcfromtimestamp(item['creation_date']).strftime('%Y-%m-%d %H:%M:%S')}\n"
                      f"Username: {item['owner']['display_name']}\n"
                      f"Link: {item['link']}\n"
                      f"Tags: {', '.join(item['tags'])}\n"
                      f"---------------------------------------")
            return json_response['has_more']
        else:
            print(f'Searching aborted with code {response_code}')
            return False

    def print_related_questions(self):
        has_more = True
        current_page = 1
        unix_time = self.unix_timestamp_2_days_ago()
        while has_more:
            search_uri = f'questions?fromdate={int(unix_time)}&page={current_page}' \
                         f'&order=desc&sort=creation&tagged=Python&site=stackoverflow'
            has_more = self.get_questions(search_uri)
            current_page += 1


if __name__ == '__main__':
    sof_manager = SOFManager()
    sof_manager.unix_timestamp_2_days_ago()
    sof_manager.print_related_questions()
