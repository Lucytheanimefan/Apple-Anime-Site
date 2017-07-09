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


        expected_top_anime = {
            (
                'Ouran Koukou Host Club',
                'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                '?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                'Byousoku 5 Centimeter',
                'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                '?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                'Tengen Toppa Gurren Lagann',
                'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                '?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                'Toradora!',
                'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                '?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                'Bakemonogatari',
                'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                '?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                'ReLIFE',
                'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                '?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                'One Punch Man',
                'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                '?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                'Kimi no Na wa.',
                'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                '?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
        }

        actual_top_anime = coordinator.filter_top_anime(actual_result)

        assert_set_equal(expected_top_anime, actual_top_anime)

        mocked_requests.get.assert_called_once_with(
            'https://myanimelist.net/animelist/katzenbaer/load.json')
        mocked_requests.get.return_value.json.assert_called_once()
