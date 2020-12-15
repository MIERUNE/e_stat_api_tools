import geopandas as gpd


class GdfDissolve:
    """gdfのジオメトリをマージするためのクラス"""

    def __init__(self, gdf, columns):
        """イニシャライザ

        Args:
            gdf (gpd.geodataframe.GeoDataFrame): geopandasのデータフレーム
            columns (list): 抽出対象となるカラム名のリスト

        """
        self.org_gdf = gdf
        self.columns = columns
        self.new_gdf: gpd.GeoDataFrame = self._extraction_gdf()

    def _extraction_gdf(self):
        """gdfから指定キーのみ抜き出す

        Returns:
            gpd.GeoDataFrame: geopandasのデータフレーム

        """
        return self.org_gdf[self.columns]

    def join_columns(self, new_column_name, org_column, add_column):
        """指定カラムを連結する

        Args:
            new_column_name (str): 新規作成するカラム名
            org_column (str): 連結元のカラム
            add_column (str): 連結させたいカラム

        """
        self.new_gdf[new_column_name] = self.new_gdf[org_column] + \
            self.new_gdf[add_column]

    def dissolve_poly(self, column):
        """指定カラム名のフィールド値が同じの場合にジオメトリを結合

        Args:
            column (str): キーとなるカラムの名称

        """
        print(f"gdfを指定キー({column})で結合します。")
        # dissolveで結合したキーはインデックスになってしまうのでreset_index()でカラムに変換
        self.new_gdf: gpd.GeoDataFrame = self.new_gdf.dissolve(
            by=column).reset_index()
