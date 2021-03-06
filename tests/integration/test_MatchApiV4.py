import sys

import pytest

if sys.version_info > (3, 0):
    import unittest.mock as mock
else:
    import mock


@pytest.mark.integration
@pytest.mark.parametrize(
    "region",
    [
        "br1",
        "eun1",
        "euw1",
        "jp1",
        "kr",
        "la1",
        "la2",
        "na",
        "na1",
        "oc1",
        "tr1",
        "ru",
        "pbe1",
    ],
)
class TestMatchApiV4(object):
    @pytest.mark.parametrize("match_id", [12345, 54321, 2, 222222222222222222222])
    def test_by_id(self, mock_context_v4, region, match_id):
        actual_response = mock_context_v4.watcher.match.by_id(region, match_id)

        assert mock_context_v4.expected_response == actual_response
        mock_context_v4.get.assert_called_once_with(
            "https://{region}.api.riotgames.com/lol/match/v4/matches/{match_id}".format(
                region=region, match_id=match_id
            ),
            params={},
            headers={"X-Riot-Token": mock_context_v4.api_key},
        )

    @pytest.mark.parametrize("encrypted_account_id", ["12345", "3333333333333333333"])
    @pytest.mark.parametrize("queue", [None, (5, 4, 3)])
    @pytest.mark.parametrize(
        "begin_end",
        [
            ((None, None), (None, None)),
            ((1234, 4321), (None, None)),
            ((None, None), (1234, 4321)),
        ],
    )
    @pytest.mark.parametrize("season", [None, (1, 11)])
    @pytest.mark.parametrize("champion", [None, (90, 43, 12)])
    def test_matchlist_by_account(
        self,
        mock_context_v4,
        region,
        encrypted_account_id,
        queue,
        begin_end,
        season,
        champion,
    ):
        begin_end_time, begin_end_index = begin_end
        begin_time, end_time = begin_end_time
        begin_index, end_index = begin_end_index

        actual_response = mock_context_v4.watcher.match.matchlist_by_account(
            region,
            encrypted_account_id,
            queue=queue,
            begin_time=begin_time,
            end_time=end_time,
            begin_index=begin_index,
            end_index=end_index,
            season=season,
            champion=champion,
        )

        assert mock_context_v4.expected_response == actual_response

        expected_params = {}
        if queue is not None:
            expected_params["queue"] = queue
        if begin_time is not None:
            expected_params["beginTime"] = begin_time
        if end_time is not None:
            expected_params["endTime"] = end_time
        if begin_index is not None:
            expected_params["beginIndex"] = begin_index
        if end_index is not None:
            expected_params["endIndex"] = end_index
        if season is not None:
            expected_params["season"] = season
        if champion is not None:
            expected_params["champion"] = champion

        mock_context_v4.get.assert_called_once_with(
            "https://{region}.api.riotgames.com/lol/match/v4/matchlists/by-account/{encrypted_account_id}".format(
                region=region, encrypted_account_id=encrypted_account_id
            ),
            params=expected_params,
            headers={"X-Riot-Token": mock_context_v4.api_key},
        )

    @pytest.mark.parametrize("match_id", [0, 54321, 3232323232323223])
    def test_timeline_by_match(self, mock_context_v4, region, match_id):
        actual_response = mock_context_v4.watcher.match.timeline_by_match(
            region, match_id
        )

        assert mock_context_v4.expected_response == actual_response
        mock_context_v4.get.assert_called_once_with(
            "https://{region}.api.riotgames.com/lol/match/v4/timelines/by-match/{match_id}".format(
                region=region, match_id=match_id
            ),
            params={},
            headers={"X-Riot-Token": mock_context_v4.api_key},
        )
