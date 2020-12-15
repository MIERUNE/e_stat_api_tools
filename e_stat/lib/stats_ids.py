import sys
from pathlib import Path

import pandas as pd

from ..utils import csv_file_to_df, csv_string_to_df, df_to_flatten_d_list, extraction_df, get_api_response, \
    output_csv_from_df, stats_res_formatter, validation_stats_url


class StatsIds:
    """統計表ID一覧を扱うクラス"""

    def __init__(
            self,
            app_id,
            gov_stats_code,
            necessary_columns=[
                "政府統計コード",
                "政府統計名"]):
        """イニシャライザ

        Args:
            app_id (str): e-statAPIのAPIkey
            gov_stats_code (str): 政府統計コード
            necessary_columns (list): 政府統計コードの中の必要なカラム名を指定

        """
        # api_key
        self.app_id = app_id

        # 取得する政府統計コード
        self.gov_stats_code = gov_stats_code

        # 政府統計コード一覧
        self.__gov_stats_codes_csv_path = "./e_stat/assets/government_statistics_codes.tsv"
        self.gov_stats_codes_df: pd.DataFrame = self._read_gov_stats_codes_tsv(
            self.__gov_stats_codes_csv_path, "shift-jis")
        self.__necessary_columns = necessary_columns
        self.gov_stats_codes_dict = self._gov_stats_codes_to_dict()

        # 統計表ID一覧
        # デフォルトでGISで扱いやすい社会・人口統計体系（00200502）のデータフレームを生成する
        self.__stats_table_ids_url = f"http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsList" \
                                     f"?appId={self.app_id}&lang=J&statsCode={self.gov_stats_code}" \
                                     f"&searchKind=1&explanationGetFlg=N"
        self.__default_stats_table_ids_csv = "./e_stat/assets/default_stats_table_ids.csv"
        self.default_stats_table_ids_df = csv_file_to_df(
            self.__default_stats_table_ids_csv)

        self.stats_table_ids_df = self._create_stats_table_ids_df()

    """プロパティ"""

    @property
    def stats_table_ids_url(self):
        return self.__stats_table_ids_url

    @stats_table_ids_url.setter
    def stats_table_ids_url(self, url):
        if validation_stats_url(url):
            self.__stats_table_ids_url = url
        else:
            print("stats_urlにはe-statのURLを入力してください。")

    """政府統計コード"""

    def _read_gov_stats_codes_tsv(self, path, encoding):
        """政府統計コード一覧のdfを生成する

        Args:
            path (str): dfに変換するtsvのパス文字列

        Returns:
            pd.DataFrame: pandasのデータフレーム

        """
        file_path = Path(path)
        resolve_path_str = str(file_path.resolve())
        return pd.read_table(resolve_path_str, encoding=encoding, dtype=str)

    def _gov_stats_codes_to_dict(self):
        """政府統計コードの名称とコードを辞書のリストで取得する

        Returns:
            dict: データフレームから必要なカラムのみ抜き出した辞書

        """
        try:
            extracted_df = extraction_df(
                self.gov_stats_codes_df, self.__necessary_columns)
        except KeyError:
            print("tsvに存在するカラム名を指定してください。システムを終了します。")
            sys.exit(1)
        return df_to_flatten_d_list(extracted_df)

    """統計表ID一覧"""

    def _create_stats_table_ids_df(self):
        """統計表ID一覧をAPIから取得して、データフレームとして返す

        Returns:
            pd.DataFrame: 統計表情報一覧のデータフレーム

        """
        res = get_api_response(self.__stats_table_ids_url)
        row_text = res.text
        csv_str = self._stats_table_ids_res_formatting(row_text)
        df = csv_string_to_df(csv_str)
        self.stats_table_ids_df = df
        return df

    def stats_table_ids_to_dict(
            self,
            columns=[
                "TABLE_INF",
                "STAT_CODE",
                "STAT_NAME",
                "TITLE",
                "COLLECT_AREA"]):
        """統計表ID一覧のdfからコード必要なカラムのみの辞書のリストで取得

        Args:
            columns (list): 抽出対象のカラム名

        Returns:
            list: 辞書のリスト

        Notes:
            columnsに空のリストを渡すとカラムを削らずそのまま辞書として返す

        """
        df = self._return_stats_table_ids_df()
        # columnsを空にするとカラムを削らずそのまま辞書として返す
        if not columns:
            df_to_flatten_d_list(df)
        try:
            extracted_df = extraction_df(
                df, columns)
        except KeyError:
            print("データフレームに存在するカラム名を指定してください。システムを終了します。")
            sys.exit(1)
        return df_to_flatten_d_list(extracted_df)

    def stats_table_ids_to_csv(
            self,
            path="./e_stat/assets/",
            file_name="stats_table_ids.csv"):
        """統計表ID一覧のdfをcsvファイルとして保存する

        Args:
            path (str): csvを保存するパス文字列
            file_name (str): 保存するファイルの名称

        """
        df = self._return_stats_table_ids_df()
        output_csv_from_df(df, path, file_name)

    def _return_stats_table_ids_df(self):
        """stats_table_ids_dfが存在すればstats_table_ids_dfを、なければdefault_stats_table_ids_dfを返す

        Returns:
            pd.DataFrame: 統計表ID一覧のデータフレーム

        """
        return self.default_stats_table_ids_df if self.stats_table_ids_df is None else self.stats_table_ids_df

    def _stats_table_ids_res_formatting(self, text):
        """統計表ID一覧取得APIのcsv風のレスポンスの先頭を削除してcsv形式の文字列を返す

        Args:
            text (str): 統計表ID一覧取得APIのcsv風のレスポンス

        Returns:
            str: 統計表ID一覧取得APIのcsv部分のみを抽出した文字列

        """
        pettern_row_text = r'.*"STAT_INF"\n(.*)'
        return stats_res_formatter(text, pettern_row_text)
