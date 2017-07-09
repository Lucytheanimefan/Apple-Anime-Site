import json
from os.path import join

from mock import patch, sentinel
from nose.tools import assert_set_equal

from models import common, mal

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

        user = common.User(sentinel.dsid)
        _ = mal.MalUser(sentinel.mal_username, user)

        expected_result = {
            (
                u'Ouran Koukou Host Club',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'Byousoku 5 Centimeter',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'Tengen Toppa Gurren Lagann',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'Toradora!',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'Bakemonogatari',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'ReLIFE',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'One Punch Man',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'Kimi no Na wa.',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'Amanchu!',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
            (
                u'Toki wo Kakeru Shoujo',
                u'https://myanimelist.cdn-dena.com/r/96x136/images/anime/7/79999.jpg'
                u'?s=a7baec80c50ad64f591ee6040c21cc77'
            ),
        }

        with open(request_result_fpath) as f:
            r = json.load(f)
            mocked_requests.get.return_value.json.return_value = r

            # act
            actual_result = coordinator.fetch_animelist(user)
            """:type: list[mal.MalEntry]"""

        # assert
        actual_top_anime = coordinator.filter_top_anime(actual_result)

        assert_set_equal(expected_result, actual_top_anime)

        mocked_requests.get.assert_called_once_with(
            'https://myanimelist.net/animelist/sentinel.mal_username/load.json')
        mocked_requests.get.return_value.json.assert_called_once()
