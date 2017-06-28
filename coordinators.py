import logging

import requests

log = logging.getLogger(__name__)


class MalCoordinator(object):
    def fetch_animelist(self, username):
        url = 'https://myanimelist.net/animelist/{}/load.json'.format(username)
        r = requests.get(url)
        my_list = r.json()

        return my_list
