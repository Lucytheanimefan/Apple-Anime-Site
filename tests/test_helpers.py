from mock import MagicMock, patch, call, ANY, mock_open, sentinel, PropertyMock
from nose_parameterized import parameterized, param
from nose.tools import raises, assert_equal, assert_true, assert_raises, assert_list_equal
from os.path import join, dirname, abspath
from tests import helpers


class TestHelpers(object):
    @patch('tests.helpers.os.path.isdir')
    def test_find_resources_dir(self, mocked_isdir):
        # arrange
        mocked_isdir.side_effect = [False, False, True]

        start_dir = '/foo/bar/baz'
        expected_result = '/foo/test_resources'

        # act
        actual_result = helpers.find_test_resources_dir(start_dir)

        # assert
        assert_equal(expected_result, actual_result)
        assert_list_equal(mocked_isdir.mock_calls, [
            call('/foo/bar/baz/test_resources'),
            call('/foo/bar/test_resources'),
            call('/foo/test_resources'),
        ])

    @patch('tests.helpers.os.path.isdir')
    def test_find_resources_dir_cant_find(self, mocked_isdir):
        # arrange
        mocked_isdir.return_value = False

        start_dir = '/foo/bar/baz'
        expected_result = None

        # act
        actual_result = helpers.find_test_resources_dir(start_dir)

        # assert
        assert_equal(expected_result, actual_result)
        assert_list_equal(mocked_isdir.mock_calls, [
            call('/foo/bar/baz/test_resources'),
            call('/foo/bar/test_resources'),
            call('/foo/test_resources'),
            call('/test_resources'),
        ])
