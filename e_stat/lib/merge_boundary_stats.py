import geopandas as gpd
import pandas as pd

from ..utils import csv_string_to_df, get_api_response


class MergeBoundaryStats:
    """境界データと統計データをマージするためのクラス"""

    def __init__(
            self,
            app_id,
            stats_table_id,
            boundary_gdf,
            area,
            class_code,
            year):
        """イニシャライザ

        Args:
            app_id (str): e-statAPIのAPIkey
            stats_table_id (str): 取得したい統計情報の統計表ID
            boundary_gdf (gpd.GeoDataFrame): 境界データのgdf
            stats_df (pd.DataFrame): 統計データのdf
            area (str): 標準地域コード
            class_code (str): 統計表メタデータのクラスコード
            year (str): データを取得したい年度

        """
        self.app_id = app_id

        self.stats_table_id = stats_table_id
        self.boundary_gdf = boundary_gdf

        self.area = area
        self.class_code = class_code
        self.year = year + "100000"

        self.detail_url = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData" \
                          f"?appId={self.app_id}" \
                          f"&cdArea={self.area}" \
                          f"&cdCat01={self.class_code}" \
                          f"&cdTime={self.year}" \
                          f"&statsDataId={self.stats_table_id}" \
                          f"&lang=J&metaGetFlg=N&cntGetFlg=N&explanationGetFlg=N&annotationGetFlg=N&sectionHeaderFlg=2"
        self.stats_df = self._extraction_only_year(self._create_stats_df())
        self.merged_df = self._merge_df()

    def _create_stats_df(self):
        """統計表をAPIから取得して、データフレームとして返す

        Returns:
            pd.DataFrame: 統計表のデータフレーム

        """
        print(f"統計表を取得します。URL={self.detail_url}")
        res = get_api_response(self.detail_url)
        row_text = res.text
        return csv_string_to_df(row_text)

    def _extraction_only_year(self, df):
        return df[df["time_code"].str.startswith(str(self.year))]

    def _merge_df(self):
        return pd.merge(
            self.boundary_gdf,
            self.stats_df,
            left_on='AREA_CODE',
            right_on='area_code')
