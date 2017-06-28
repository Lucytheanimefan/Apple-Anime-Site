import logging

import requests

log = logging.getLogger(__name__)


class MalCoordinator(object):
    def fetch_animelist(self, username):
        url = 'https://myanimelist.net/animelist/{}/load.json'.format(username)
        r = requests.get(url)
        my_list = r.json()

        return my_list

    @staticmethod
    def filter_top_anime(animelist):
        def top_anime_filter(entry):
            return entry['status'] == 2 and entry['score'] == 10

        def get_title(entry):
            return entry['anime_title']

        return set(map(get_title, filter(top_anime_filter, animelist)))
