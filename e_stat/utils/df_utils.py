import io
from pathlib import Path

import pandas as pd
import requests


def get_api_response(url):
    """URLを指定してレスポンスオブジェクトを返す

    Args:
        url (str): URL

    Returns:
        Response: レスポンスオブジェクト

    """
    return requests.get(url)


def extraction_df(df, columns):
    """dfから指定キーのみ抜き出す

    Args:
        df (pd.DataFrame): データフレーム
        columns (list): 必要なカラム

    Returns:
        pd.DataFrame: pandasのデータフレーム

    """
    return df[columns]


def df_to_flatten_d_list(df):
    """データフレームを辞書のリストに加工する

    Args:
        df (pd.DataFrame): 辞書のリストへ変換したいdf

    Returns:
        list: データフレームのカラムを格納した辞書のリスト

    """
    _dict = df.to_dict('index')
    return [v for v in _dict.values()]


def csv_file_to_df(path):
    """csvファイルをデータフレームに変換

    Args:
        path (str): csvのパス文字列

    Returns:
        pd.DataFrame: csvファイルを変換したdf

    """
    csv_path = Path(path)
    return pd.read_csv(str(csv_path.resolve()),
                       encoding="utf-8", dtype=str)


def csv_string_to_df(csv_str):
    """csv形式の文字列オブジェクトをデータフレームに変換

    Args:
        csv_str (str): csv形式の文字列オブジェクト

    Returns:
        pd.DataFrame: csv形式の文字列オブジェクトを変換したdf

    """
    return pd.read_csv(
        io.StringIO(csv_str),
        encoding="shift-jis",
        dtype=str)


def output_csv_from_df(df, path, file_name):
    """データフレームを受け取り、csvを返す

    Args:
        df (pd.DataFrame): 書き出し対象のデータフレーム
        path (str): アウトプットするディレクトリのパス文字列
        file_name (str): 書き出すファイルの名称

    """
    dir_path = Path(path)
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
    output_path = dir_path / file_name
    df.to_csv(str(output_path.resolve()),
              encoding="utf-8", index=False)
    print(f"{output_path.resolve()}を書き出しました。")
