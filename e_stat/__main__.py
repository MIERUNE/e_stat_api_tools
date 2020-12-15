from pathlib import Path

import click

from .env_settings import app_id
from .lib import AreaCode, GdfDissolve, PrefCode, ShapeToGeoPandas, StatsData, StatsIds, StatsMetaData, MergeBoundaryStats
from .utils import df_to_geojson, geojson_str_to_obj, output_csv_from_df, write_geojson


@click.group()
def main():
    """e-statのAPIを簡単に利用するためのCLIツール"""


@main.command()
@click.option('-p', '--pref_name', required=True,
              type=str, help="取得するshpファイルの都道府県コードを入力")
@click.option('-d', '--download_dir', required=True,
              type=str, help="ダウンロードするshpファイルを格納するディレクトリのパス文字列を入力")
def boundary(pref_name, download_dir):
    """境界データを取得"""
    pref = PrefCode()
    pref_code = str(pref.name_to_code(pref_name)).zfill(2)

    area_code = AreaCode()
    output_dir = Path(download_dir).resolve()
    area_code.download_polygon_of_shp(pref_code, str(output_dir), False)
    download_path = area_code.download_file_path

    s2g = ShapeToGeoPandas(download_path)
    gdf = s2g.gdf

    necessary_columns = [
        "KEY_CODE",
        "PREF",
        "CITY",
        "PREF_NAME",
        "CITY_NAME",
        "geometry"]
    geo_d = GdfDissolve(gdf, necessary_columns)
    geo_d.join_columns("AREA_CODE", "PREF", "CITY")
    geo_d.dissolve_poly("AREA_CODE")
    boundary_gdf = geo_d.new_gdf

    geojson_obj = geojson_str_to_obj(df_to_geojson(boundary_gdf))
    write_geojson(geojson_obj, "./created/", "boundary.geojson")

    output_csv_from_df(boundary_gdf, "./created/", "boundary.csv")
    return boundary_gdf


@main.command()
@click.option("-g", "--gov_stats_code", required=True,
              type=str, help="取得したい統計表ID一覧の政府統計コードを入力")
@click.option('-o', '--output_dir', required=True,
              type=str, help="ダウンロードしたcsvを格納するディレクトリのパス文字列を入力")
def ids(gov_stats_code, output_dir):
    """統計表ID一覧を取得"""
    si = StatsIds(app_id, gov_stats_code)
    si_df = si.stats_table_ids_df
    si.stats_table_ids_to_csv(output_dir, "stats_ids.csv")
    return si_df


@main.command()
@click.option("-st", "--stats_table_id", required=True,
              type=str, help="取得したい統計表メタデータの統計表IDを入力")
@click.option('-o', '--output_dir', required=True,
              type=str, help="ダウンロードしたcsvを格納するディレクトリのパス文字列を入力")
def meta(stats_table_id, output_dir):
    """統計表メタデータを取得"""
    smt = StatsMetaData(app_id, stats_table_id)
    smt_df = smt.stats_meta_data_df
    smt.to_csv(output_dir, "meta_data.csv")
    return smt_df


@main.command()
@click.option('-a', '--areas', required=True, type=str,
              help="取得する統計データの標準地域コードをカンマ区切り文字列で入力(例:01101,01103,01105)")
@click.option('-c', '--class_codes', required=True, type=str,
              help="取得する統計データの項目をカンマ区切り文字列で入力(例:A1101,A110101,A110101)")
@click.option('-y', '--years', required=True,
              type=str, help="取得する統計データの年度をカンマ区切り文字列で入力(例:2000,2005,2010)")
@click.option("-st", "--stats_table_id", required=True,
              type=str, help="取得したい統計データの統計表IDを入力")
@click.option('-o', '--output_dir', required=True,
              type=str, help="ダウンロードしたcsvを格納するディレクトリのパス文字列を入力")
def stats(areas, class_codes, years, stats_table_id, output_dir):
    """統計データを取得"""
    sd = StatsData(
        app_id,
        stats_table_id,
        output_dir,
        areas.split(","),
        class_codes.split(","),
        years.split(","))
    stats_df = sd.stats_df
    sd.to_csv(output_dir, "stats.csv")
    return stats_df


@main.command()
@click.option('-p', '--pref_name', required=True,
              type=str, help="取得するshpファイルの都道府県コードを入力")
@click.option('-d', '--download_dir', required=True,
              type=str, help="ダウンロードするshpファイルを格納するディレクトリのパス文字列を入力")
@click.option('-a', '--area', required=True, type=str,
              help="取得する統計データの標準地域コードを入力")
@click.option('-c', '--class_code', required=True, type=str,
              help="取得する統計データの項目を入力")
@click.option('-y', '--year', required=True,
              type=str, help="取得する統計データの年度を入力")
@click.option("-st", "--stats_table_id", required=True,
              type=str, help="取得したい統計データの統計表IDを入力")
@click.option('-o', '--output_dir', required=True,
              type=str, help="ダウンロードしたcsvを格納するディレクトリのパス文字列を入力")
def merge_boundary(
        pref_name,
        download_dir,
        area,
        class_code,
        year,
        stats_table_id,
        output_dir):
    """統計データと境界データを取得してマージする"""
    pref = PrefCode()
    pref_code = str(pref.name_to_code(pref_name)).zfill(2)

    area_code = AreaCode()
    output_shp_dir = Path(download_dir).resolve()
    area_code.download_polygon_of_shp(pref_code, str(output_shp_dir), False)
    download_path = area_code.download_file_path

    s2g = ShapeToGeoPandas(download_path)
    gdf = s2g.gdf

    necessary_columns = [
        "KEY_CODE",
        "PREF",
        "CITY",
        "PREF_NAME",
        "CITY_NAME",
        "geometry"]
    geo_d = GdfDissolve(gdf, necessary_columns)
    geo_d.join_columns("AREA_CODE", "PREF", "CITY")
    geo_d.dissolve_poly("AREA_CODE")
    boundary_gdf = geo_d.new_gdf

    geojson_obj = geojson_str_to_obj(df_to_geojson(boundary_gdf))
    write_geojson(geojson_obj, "./created/", "boundary.geojson")

    output_csv_from_df(boundary_gdf, "./created/", "boundary.csv")

    mbs = MergeBoundaryStats(app_id,
                             stats_table_id,
                             boundary_gdf,
                             area,
                             class_code,
                             year)
    merge_boundary_df = mbs.merged_df

    geojson_obj = geojson_str_to_obj(df_to_geojson(merge_boundary_df))
    write_geojson(geojson_obj, "./created/", "merge_boundary.geojson")

    output_csv_from_df(merge_boundary_df, output_dir, "merge_boundary.csv")


if __name__ == '__main__':
    main()
