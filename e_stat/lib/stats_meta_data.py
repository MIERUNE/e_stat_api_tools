import sys

from ..utils import csv_string_to_df, df_to_flatten_d_list, extraction_df, get_api_response, output_csv_from_df, \
    stats_res_formatter


class StatsMetaData:
    """統計表情報の詳細情報（メタデータ）を取り扱うクラス"""

    def __init__(self, app_id, stats_table_id):
        """イニシャライザ

        Args:
            app_id (str): e-statAPIのAPIkey
            stats_table_id (str): 取得したい統計情報の統計表ID

        """
        # api_key
        self.app_id = app_id

        # 統計情報
        self.stats_data_id = stats_table_id
        self.default_url = f"http://api.e-stat.go.jp/rest/3.0/app/getSimpleMetaInfo" \
                           f"?appId={self.app_id}" \
                           f"&lang=J&statsDataId={self.stats_data_id}&explanationGetFlg=N"
        self.stats_meta_data_df = self._create_stats_meta_data_df()

    def _create_stats_meta_data_df(self):
        """統計表ID一覧をAPIから取得して、データフレームとして返す

        Returns:
            pd.DataFrame: 統計表情報一覧のデータフレーム

        """
        res = get_api_response(self.default_url)
        row_text = res.text
        csv_str = self._stats_meta_data_res_formatting(row_text)
        df = csv_string_to_df(csv_str)
        self.stats_meta_data_df = df
        return df

    def _stats_meta_data_res_formatting(self, text):
        """統計表ID一覧取得APIのcsv風のレスポンスの先頭を削除してcsv形式の文字列を返す

        Args:
            text (str): 統計表ID一覧取得APIのcsv風のレスポンス

        Returns:
            str: 統計表ID一覧取得APIのcsv部分のみを抽出した文字列

        """
        pattern_row_text = r'.*"CLASS_INF"\n(.*)'
        return stats_res_formatter(text, pattern_row_text)

    def to_dict(
            self,
            columns=[
                "CLASS_OBJ_NAME",
                "CLASS_CODE",
                "CLASS_NAME"]):
        """統計表メタデータのdfからコード必要なカラムのみの辞書のリストで取得

        Args:
            columns (list): 抽出対象のカラム名

        Returns:
            list: 辞書のリスト

        Notes:
            columnsに空のリストを渡すとカラムを削らずそのまま辞書として返す

        """
        df = self.stats_meta_data_df
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

    def to_csv(
            self,
            path="./e_stat/assets/",
            file_name="meta_data.csv"):
        """統計表メタデータのdfをcsvファイルとして保存する

        Args:
            path (str): csvを保存するパス文字列
            file_name (str): 保存するファイルの名称

        """
        df = self.stats_meta_data_df
        output_csv_from_df(df, path, file_name)
