import json
import sys
from pathlib import Path
import pandas as pd


class PrefCode:
    """都道府県コードクラス"""

    def __init__(self):
        """イニシャライザ

        """
        self.__pref_code_json_path = Path("./e_stat/assets/pref_code.json")
        self.__pref_code_df = self._pref_json_to_df()

    def _read_json(self):
        """jsonを読み込んで辞書に変換する

        Returns:
            Union[dict, list]: jsonを変換した辞書またはリスト

        """
        json_path = self.__pref_code_json_path
        with json_path.open() as file:
            return json.load(file)

    def _dict_in_list_to_df(self, dicts):
        """フラットな同じキーを持つ辞書のリストをdfに変換

        Args:
            dicts (list): 辞書のリスト

        Returns:
            pd.DataFrame: 変換されたdf

        """
        return pd.DataFrame(dicts)

    def _pref_json_to_df(self):
        if isinstance(self._read_json(), list):
            return self._dict_in_list_to_df(self._read_json())
        print(f"{self.__pref_code_json_path}はdfに変換できません。システムを終了します。")
        sys.exit(1)

    def code_to_name(self, pref_code):
        """都道府県コードを都道府県名に変換する

        Args:
            pref_code (int):  都道府県コード

        Returns:
            str: 都道府県名

        """
        df = self.__pref_code_df
        try:
            pref_name = list(df[df["prefCode"] == pref_code]["prefName"])[0]
            return pref_name
        except BaseException:
            print(f"{df}からデータを抽出できません。システムを終了します。")
            sys.exit(1)

    def name_to_code(self, pref_name):
        """都道府県名を都道府県コードに変換する

        Args:
            pref_name (str): 都道府県名

        Returns:
            int: 都道府県コード

        """
        df = self.__pref_code_df
        try:
            pref_code = list(df[df["prefName"] == pref_name]["prefCode"])[0]
            return pref_code
        except BaseException:
            print(f"{df}からデータを抽出できません。システムを終了します。")
            sys.exit(1)
