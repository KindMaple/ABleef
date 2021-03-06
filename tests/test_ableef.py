"""
TODO
fetch_daily_meta_info()
- [x] 1日分のBleeeeeefingページのメタ情報をJSONで取得する
    - [x] 2021-10-23のBleeeeeefingページのメタ情報をDictで返す
    - [x] 2021-10-24のBleeeeeefingページのメタ情報をDictで返す
fetch_daily_content()
- [x] 1日分のBleeeeeefingページの内容をJSONで取得する
    - [x] 2021-10-23のBleeeeeefingページのメタ情報をDictで返す
    - [x] 2021-10-24のBleeeeeefingページのメタ情報をDictで返す
to_slack_format()
- [x] 空のリストが渡されたら空文字列を返す
- [x] Slackに投稿する文字列を返す
    - [x] その他を本文そのまま連結して返す
    - [x] heading_2をボールド体に変換する
    - [x] bulleted_list_itemを"・"で始まる文字列に変換する
"""
import datetime
from typing import Any, Dict, List

import pytest

from ableef.lib import fetch_daily_content, fetch_daily_meta_info, to_slack_format


class Test_fetch_meta_info:
    def test_2021_10_23のBleeeeeefingページのメタ情報をDictで返す(self):
        today: datetime.date = datetime.date(2021, 10, 23)
        result: Dict[str, Any] = fetch_daily_meta_info(today)
        assert result["properties"]["名前"]["title"][0]["plain_text"] == "2021/10/23"
        assert result["properties"]["日付"]["date"]["start"] == "2021-10-23"

    def test_2021_10_24のBleeeeeefingページのメタ情報をDictで返す(self):
        today: datetime.date = datetime.date(2021, 10, 24)
        result: Dict[str, Any] = fetch_daily_meta_info(today)
        assert result["properties"]["名前"]["title"][0]["plain_text"] == "2021/10/24"
        assert result["properties"]["日付"]["date"]["start"] == "2021-10-24"


class Test_fetch_daily_content:
    def test_2021_10_23のBleeeeeefingページのメタ情報をDictで返す(self):
        block_id: str = "43ca1c50-e2a3-4c8e-b936-4693e6e202c8"
        result: List[Dict[str, Any]] = fetch_daily_content(block_id)
        assert result[1]["type"] == "bulleted_list_item"
        assert result[1]["bulleted_list_item"]["text"][0]["plain_text"] == "hoge"

    def test_2021_10_24のBleeeeeefingページのメタ情報をDictで返す(self):
        block_id: str = "76659722-c2fc-4de4-ae72-92b4c2b306a9"
        result: List[Dict[str, Any]] = fetch_daily_content(block_id)
        assert result[1]["type"] == "bulleted_list_item"
        assert (
            result[1]["bulleted_list_item"]["text"][0]["plain_text"]
            == "Bleeeeeefing自動投稿スクリプトをテスト駆動開発+非公式ライブラリなしで書き直し（dailyの投稿部まで）"
        )


class Test_to_slack_format:
    def test_空のリストが渡されたら空文字列を返す(self):
        result: str = to_slack_format([])
        assert result == ""

    def test_その他を本文そのまま連結して返す(self, mock_content):
        result: str = to_slack_format(mock_content)
        assert "Problems" in result
        assert "hoge" in result

    def test_heading_2をボールド体に変換する(self, mock_content):
        result: str = to_slack_format(mock_content)
        assert "*Problems*" in result

    def test_bulleted_list_itemを中黒で始まる文字列に変換する(self, mock_content):
        result: str = to_slack_format(mock_content)
        assert "・hoge" in result


@pytest.fixture(scope="session")
def mock_content():
    return [
        {
            "archived": False,
            "created_time": "2021-10-23T12:36:00.000Z",
            "has_children": False,
            "heading_2": {
                "text": [
                    {
                        "annotations": {
                            "bold": False,
                            "code": False,
                            "color": "default",
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                        },
                        "href": None,
                        "plain_text": "Problems",
                        "text": {"content": "Problems", "link": None},
                        "type": "text",
                    }
                ]
            },
            "id": "4fcf10f2-08f4-4155-be1f-25d3b16b901a",
            "last_edited_time": "2021-10-23T12:37:00.000Z",
            "object": "block",
            "type": "heading_2",
        },
        {
            "archived": False,
            "bulleted_list_item": {
                "text": [
                    {
                        "annotations": {
                            "bold": False,
                            "code": False,
                            "color": "default",
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                        },
                        "href": None,
                        "plain_text": "hoge",
                        "text": {"content": "hoge", "link": None},
                        "type": "text",
                    }
                ]
            },
            "created_time": "2021-10-23T12:37:00.000Z",
            "has_children": False,
            "id": "6f8c41b7-4bd5-495c-8e48-7e88bb5583d1",
            "last_edited_time": "2021-10-23T12:37:00.000Z",
            "object": "block",
            "type": "bulleted_list_item",
        },
    ]
