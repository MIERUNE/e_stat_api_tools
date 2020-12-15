from ..utils import csv_string_to_df, get_api_response, stats_res_formatter


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
        self.stats_meta_data_df = None

    def create_stats_meta_data_df(self):
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
