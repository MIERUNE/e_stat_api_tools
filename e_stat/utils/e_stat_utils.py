import re
import sys
from urllib.parse import urlparse

import requests


def stats_res_formatter(text, pattern_row_text):
    """e-statAPIのcsv風のレスポンスの先頭を削除してcsv形式の文字列を返す

    Args:
        text (str): e-statAPIのcsv風のレスポンス
        pattern_row_text (str): マッチさせたいパターンのrow文字列

    Returns:
        str: e-statAPIのcsv部分のみを抽出した文字列

    """
    # 第二引数にre.Sを与えることで.*が改行を認識できるようにする
    pattern = re.compile(pattern_row_text, re.S)
    if match := pattern.match(text):
        return match.groups()[0]
    else:
        print("レスポンスの文字列を整形できません。システムを終了します。")
        sys.exit(1)


def validation_stats_url(url):
    """URLがe-statAPIのものであるか判定

    Args:
        url (str): URL

    Returns:
        bool: e-statのURL風ならTrue

    """
    if not isinstance(url, str):
        return False
    if not len(urlparse(url).scheme) > 0:
        return False
    if not urlparse(url).netloc == "api.e-stat.go.jp":
        return False
    try:
        requests.head(url)
    except requests.exceptions.MissingSchema:
        return False
    return True
