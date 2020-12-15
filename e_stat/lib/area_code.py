import os
import re
import sys
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm


class AreaCode:
    """標準地域コードクラス"""

    def __init__(
            self,
            path="./e_stat/assets/standard_area_codes.csv",
            encoding="shift-jis",
            dtype="str"):
        """イニシャライザ

        Args:
            path (str): 標準地域コードが格納されたcsvのパス文字列
            encoding (str): csv読み込み時のエンコーディング
            dtype (dict): カラムのdtype

        """
        self.path = Path(path)
        self.df = self._read_csv(self.path, encoding, dtype)
        # download_polygon_of_shpが実行されるまでNone
        self.download_file_path = None

    def _read_csv(self, path, encoding, dtype):
        """指定csvを読み込みDataFrameに変換する

        Args:
            path (Path): 標準地域コードが格納されたcsvのpath
            encoding (str): csv読み込み時のエンコーディング
            dtype (dict): カラムのdtype

        Returns:
            pd.DataFrame: csvのDataFrame

        """
        self.df = pd.read_csv(path, encoding=encoding, dtype=dtype)
        return self.df

    def _get_row(self, start, stop):
        """スライスで行番号を指定して列を取得

        Args:
            start (int): スライスの開始行を指定
            stop (int): スライスの終了行を指定

        Returns:
            pd.DataFrame: 対象の行のみ抽出したDataFrame

        Notes:
            先頭は0行目なので番号指定に注意

        """
        return self.df[start:stop]

    def _get_one_row(self, index):
        """行番号を指定して1列を取得

        Args:
            index (int): 行番号を指定

        Returns:
            pd.DataFrame: 対象の行のみ抽出したDataFrame

        Notes:
            先頭は0行目なので番号指定に注意

        """
        return self._get_row(index, index + 1)

    def _get_columns(self, column_name="標準地域コード"):
        """DataFrameから標準地域コードを取得（取得するカラムは上書き可能）

        Args:
            column_name (str): 取得するカラムの名称

        Returns:
            list: 取得したカラムのリスト

        """
        return list(self.df[column_name])

    def _text_search(self, column_name, search_word):
        """指定カラムから指定ワードで検索する

        Args:
            column_name (str): 検索対象のカラム名を指定
            search_word (str): 検索ワードを指定

        Returns:
            pd.DataFrame: 対象の行のみ抽出したDataFrame

        """
        return self.df[self.df[column_name].str.contains(search_word)]

    def _check_suffix(self, file_path, suffix):
        """ファイルの拡張子が指定のものかどうかチェック

        Args:
            file_path (Path): ファイルのパス
            suffix (str): 対象の拡張子

        """
        if file_path.suffix == suffix:
            return True
        return False

    def _make_download_path(self, dir_path):
        """パス文字列からディレクトリを作成し、Pathオブジェクトを返す

        Args:
            dir_path (str): ディレクトリのパス文字列

        Returns:
            Path: 作成されたディレクトリのPathオブジェクト

        """
        parent_dir = Path(dir_path)

        if not parent_dir.exists():
            parent_dir.mkdir(parents=True, exist_ok=True)

        return parent_dir

    def _get_file_name_from_response(self, url, response):
        """responseのContent-Dispositionからファイル名を取得、できなければURLの末尾をファイル名として返す

        Args:
            url (str): リクエストのURL
            response (Response): responseオブジェクト

        Returns:
            str: ファイル名を返す

        """
        disposition = response.headers["Content-Disposition"]
        try:
            file_name = re.findall(r"filename.+''(.+)", disposition)[0]
        except IndexError:
            print("ファイル名が取得できませんでした")
            file_name = os.path.basename(url)
        return file_name

    def _file_download(self, url, dir_path, overwrite=True):
        """URLと保存先ディレクトリを指定してファイルをダウンロード

        Args:
            url (str): ダウンロードリンク
            dir_path (str): 保存するディレクトリのパス文字列
            overwrite (bool): ファイル上書きオプション。Trueなら上書き

        Returns:
            Path: ダウンロードファイルのパスオブジェクト

        Notes:
            すでにファイルが存在していて、overwrite=Falseなら何もせず
            ファイルパスを返す

        """
        res = requests.get(url, stream=True)

        parent_dir = self._make_download_path(dir_path)
        file_name = self._get_file_name_from_response(url, res)
        download_path = parent_dir / file_name

        if download_path.exists() and not overwrite:
            print("ファイルがすでに存在し、overwrite=Falseなのでダウンロードを中止します。")
            return download_path

        # content-lengthは必ず存在するわけでは無いためチェック
        try:
            file_size = int(res.headers['content-length'])
        except KeyError:
            file_size = None
        progress_bar = tqdm(total=file_size, unit="B", unit_scale=True)

        if res.status_code == 200:
            print(f"{url=}, {res.status_code=}")
            print(f"{file_name}のダウンロードを開始します")
            with download_path.open('wb') as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)
                    progress_bar.update(len(chunk))
                progress_bar.close()
            return download_path
        else:
            print(f"{url=}, {res.status_code=}")
            print("正常にリクエストできませんでした。システムを終了します。")
            sys.exit(1)

    def download_polygon_of_shp(self, area_code, dir_path, overwrite=True):
        """指定された標準地域コードのshpを格納したzipファイルをダウンロード

        Args:
            area_code (str): ダウンロード対象の標準地域コード
            dir_path (str): ファイルを格納するディレクトリ
            overwrite (bool): ファイル上書きオプション。Trueなら上書き

        Notes:
            すでにファイルが存在していて、overwrite=Falseなら何もせず
            self.download_file_pathにファイルパスを保存する

        """
        area_code_to_int = area_code
        base_url = f"https://www.e-stat.go.jp/gis/statmap-search/data?"
        query_params = f"dlserveyId=A002005212015&code={area_code_to_int}&coordSys=1&format=shape&downloadType=5"
        request_url = base_url + query_params
        self.download_file_path = self._file_download(
            request_url, dir_path, overwrite)
