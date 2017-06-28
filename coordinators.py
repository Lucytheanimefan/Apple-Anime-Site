import logging

import requests

log = logging.getLogger(__name__)


class MalCoordinator(object):
    """
    Coordinator that interfaces with MyAnimeList.net
    """
    def fetch_animelist(self, username):
        """
        Fetches the animelist for a given user.

        :param string username: Given user

        :return: Raw JSON.
        :rtype: list[dict[string, object]]
        """
        url = 'https://myanimelist.net/animelist/{}/load.json'.format(username)
        r = requests.get(url)
        my_list = r.json()

        # TODO: Update database with data and return objects
        return my_list

    @staticmethod
    def filter_top_anime(animelist):
        """
        Returns the titles of anime that are marked as Completed and have a perfect score.

        :param list[dict[string, object]] animelist: Given anime list

        :return: Set of anime titles
        :rtype: set[string]
        """
        def top_anime_filter(entry):
            return entry['status'] == 2 and entry['score'] == 10

        def get_title(entry):
            return entry['anime_title']

        return set(map(get_title, filter(top_anime_filter, animelist)))
