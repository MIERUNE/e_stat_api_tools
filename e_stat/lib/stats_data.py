from ..utils import csv_string_to_df, get_api_response, output_csv_from_df


class StatsData:
    """統計情報を取り扱うクラス"""

    def __init__(
            self,
            app_id,
            stats_table_id,
            output_dir,
            areas,
            class_codes,
            years):
        """イニシャライザ

        Args:
            app_id (str): e-statAPIのAPIkey
            stats_table_id (str): 取得したい統計情報の統計表ID
            output_dir (str): ファイル吐き出し先ディレクトリのパス文字列
            areas (list): 標準地域コードのリスト
            class_codes (list): 統計表メタデータのクラスコードのリスト（取得したい詳細項目）
            years (list): データを取得したい年度のリスト

        """
        # api_key
        self.app_id = app_id

        # 統計情報
        self.stats_table_id = stats_table_id
        self.output_dir = output_dir

        self.areas = ",".join(areas)
        self.class_codes = ",".join(class_codes)
        self.years = ",".join([str(y) + "100000" for y in years])

        self.detail_url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData" \
            f"?appId={self.app_id}" \
            f"&cdArea={self.areas}" \
            f"&cdCat01={self.class_codes}" \
            f"&cdTime={self.years}" \
            f"&statsDataId={self.stats_table_id}" \
            f"&lang=J&metaGetFlg=N&cntGetFlg=N&explanationGetFlg=N&annotationGetFlg=N&sectionHeaderFlg=2"

        self.stats_df = self._create_stats_df()

    def _create_stats_df(self):
        """統計表をAPIから取得して、データフレームとして返す

        Returns:
            pd.DataFrame: 統計表のデータフレーム

        """
        print(f"統計表を取得します。URL={self.detail_url}")
        res = get_api_response(self.detail_url)
        row_text = res.text
        return csv_string_to_df(row_text)

    def df_to_csv(self):
        output_csv_from_df(
            self.stats_df,
            self.output_dir,
            "statistics_data.csv")
