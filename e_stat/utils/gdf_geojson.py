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
    output_dit_obj = Path(output_dir)
    data_path = output_dit_obj / file_name
    if not output_dit_obj.exists():
        output_dit_obj.mkdir(parents=True, exist_ok=True)
    with data_path.open("w") as file:
        geojson.dump(geojson_obj, file, indent=2, ensure_ascii=False)
        print(f"{data_path.resolve()}を書き出しました。")
