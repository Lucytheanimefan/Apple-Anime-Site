import logging

import requests

from models import mal

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
        :rtype: list[mal.MalEntry]
        """
        url = 'https://myanimelist.net/animelist/{}/load.json'.format(username)
        r = requests.get(url)
        json_entries = r.json()

        entries = []

        if isinstance(json_entries, dict):
            log.error(u"Error while fetching top anime for {}".format(username))
            return entries

        for json_entry in json_entries:
            entry = mal.MalEntry()
            entry.anime_id = json_entry['anime_id']
            entry.title = json_entry['anime_title']
            entry.user_status = mal.MalEntryUserStatus(json_entry['status'])
            entry.airing_status = mal.MalEntryAiringStatus(json_entry['anime_airing_status'])
            entry.watched_episodes = json_entry['num_watched_episodes']
            entry.total_episodes = json_entry['anime_num_episodes']
            entry.user_score = json_entry['score']
            entries.append(entry)

        return entries

    @staticmethod
    def filter_top_anime(animelist):
        """
        Returns the titles of anime that are marked as Completed and have a perfect score.

        :param list[mal.MalEntry] animelist: Given anime list

        :return: Set of anime titles
        :rtype: set[string]
        """
        def top_anime_filter(entry):
            """

            :param mal.MalEntry entry:
            :return:
            """
            return entry.airing_status in [
                mal.MalEntryAiringStatus.aired, mal.MalEntryAiringStatus.airing
            ] and entry.user_score == 10

        def get_title_image(entry):
            """

            :param mal.MalEntry entry:
            :return:
            """
            # TODO: Figure out another way to get image
            return (entry.title,
                    'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                    '?s=a7baec80c50ad64f591ee6040c21cc77')

        return set(map(get_title_image, filter(top_anime_filter, animelist)))

    # TODO: Determine the following
    # 1) Most watched anime (watching or completed, all time)
    # 2) Most completed anime (completed, all time)
    # 3) Highest score (all time)
