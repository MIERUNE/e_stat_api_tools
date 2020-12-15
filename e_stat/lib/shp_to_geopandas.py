import sys
from pathlib import Path

import geopandas as gpd


class ShapeToGeoPandas:
    """シェープファイルをGeoDataframeに変換して指定形式で吐き出すクラス"""

    def __init__(self, shp_path):
        """イニシャライザ

        Args:
            shp_path (str): .shpが格納されているzipのパス文字列（.shpファイルの直接参照も可）

        """
        self.shp_path = shp_path
        self.gdf = self._file_to_gdf(shp_path)

    def _suffix_check(self, path, target_suffix):
        """ファイルの拡張子が指定のものかチェック

        Args:
            path (str): チェック対象ファイルのパス文字列
            target_suffix (str): 対象の拡張子

        Returns:
            bool: target_suffixとファイルの拡張子が一致すればTrue

        """
        file_path = Path(path)
        if not file_path.is_file():
            print("パスはファイルを指定してください。システムを終了します。")
            sys.exit(1)
        if file_path.suffix.lstrip('.') == target_suffix:
            return True
        return False

    def _is_zip_file(self, path):
        """対象ファイルの拡張子がzipかどうかチェック

        Args:
            path (str): チェック対象ファイルのパス文字列

        Returns:
            bool: ファイル拡張子がzipならTrue

        """
        return self._suffix_check(path, "zip")

    def _is_shp_file(self, path):
        """対象ファイルの拡張子がshpかどうかチェック

        Args:
            path (str): チェック対象ファイルのパス文字列

        Returns:
            bool: ファイル拡張子がshpならTrue

        """
        return self._suffix_check(path, "shp")

    def _shp_to_gdf(self, path):
        """shpファイルをGeoDataframeに変換する

        Args:
            path (str): shpファイルのパス文字列

        Returns:
            gpd.GeoDataFrame: shpファイルを変換したgdf

        """
        path_str = str(Path(path).resolve())
        return gpd.read_file(path_str)

    def _zip_to_gdf(self, path):
        """zipファイルをGeoDataframeに変換する

        Args:
            path (str): zipファイルのパス文字列

        Returns:
            gpd.GeoDataFrame: shpファイルを変換したgdf

        """
        path_str = str(Path(path).resolve())
        return gpd.read_file("zip://" + path_str)

    def _file_to_gdf(self, path):
        """.shp及び.shpが格納されたzipファイルを読み込みGeoDataFrameを返す

        Args:
            path (str): .shp及び.shpが格納された.zipのパス文字列

        Returns:
            gpd.GeoDataFrame: shpファイルを変換したgdf

        Notes:
            .shpか.zip以外のファイルを指定した時には異常終了

        """
        print("読み込みファイル：", str(Path(path).resolve()))
        print(f"suffix={Path(path).suffix.lstrip('.')}")

        if self._is_shp_file(path) is True:
            print("shpファイルをgdfに変換します")
            return self._shp_to_gdf(path)

        if self._is_zip_file(path) is True:
            print(".zipファイル内のshpファイルをgdfに変換します")
            return self._zip_to_gdf(path)

        print("読み込み可能ファイルは.shpか.zipのみです。システムを終了します。")
        sys.exit(1)
