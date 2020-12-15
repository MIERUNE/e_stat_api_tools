from pathlib import Path

import geojson
import geopandas as gpd


def df_to_geojson(gdf):
    """gdfから指定されたディレクトリに指定名でGeoJSONを作成する

    Args:
        gdf (gpd.GeoDataFrame): 書き出し元のgdf

    Returns:
        str: geojson形式の文字列

    """
    print("gdfをgeojsonに変換します。")
    return gdf.to_json()


def geojson_str_to_obj(geojson_str):
    """

    Args:
        geojson_str (str): geojson形式の文字列

    Returns:
        geojson.feature.FeatureCollection: geojsonオブジェクト

    """
    return geojson.loads(geojson_str)


def write_geojson(geojson_obj, output_dir, file_name):
    """geojsonオブジェクトをファイル出力する

    Args:
        geojson_obj (geojson): GeoJSONオブジェクト
        output_dir (str): 書き出し先ディレクトリのパス文字列
        file_name (str): 作成するファイルの名称

    """
    data_path = Path(output_dir) / file_name
    with data_path.open("w") as file:
        print(f"{data_path}を書き出します。")
        geojson.dump(geojson_obj, file, indent=2, ensure_ascii=False)
