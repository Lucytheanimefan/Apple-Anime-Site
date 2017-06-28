import json
from os.path import join

from mock import patch
from nose.tools import assert_set_equal

from coordinators import MalCoordinator
from tests.helpers import find_test_resources_dir


class TestMalCoordinator(object):
    @patch('coordinators.requests')
    def test_fetch_animelist(self, mocked_requests):
        # arrange
        request_result_fpath = join(
            find_test_resources_dir(__file__),
            'mal', 'myanimelist_net_animelist_katzenbaer_load.json'
        )

        coordinator = MalCoordinator()

        with open(request_result_fpath) as f:
            r = json.load(f)
            mocked_requests.get.return_value.json.return_value = r

            # act
            actual_result = coordinator.fetch_animelist('katzenbaer')
            """:type: list[dict[string, object]]"""

        # assert
        def top_anime_filter(entry):
            return entry['status'] == 2 and entry['score'] == 10

        def get_title(entry):
            return entry['anime_title']

        expected_top_anime = {
            'Ouran Koukou Host Club',
            'Byousoku 5 Centimeter',
            'Tengen Toppa Gurren Lagann',
            'Toradora!',
            'Bakemonogatari',
            'ReLIFE',
            'One Punch Man',
            'Kimi no Na wa.'
        }

        actual_top_anime = set(map(get_title, filter(top_anime_filter, actual_result)))

        assert_set_equal(expected_top_anime, actual_top_anime)

        mocked_requests.get.assert_called_once_with(
            'https://myanimelist.net/animelist/katzenbaer/load.json')
        mocked_requests.get.return_value.json.assert_called_once()
