# e_stat_api_sample

e-statのAPIを簡単に利用するためのCLIツール
（パッケージとしても利用可能）

## usage

### install library

```shell script
% pwd
.../e_stat_api_sample
% pipenv install
```

### setup .env

```
touch /e_stat_api_sample/e_stat/.env
echo "app_id=<YOUR_APP_ID>" >> /e_stat_api_sample/e_stat/.env
```

#### what's app_id

[https://www.e-stat.go.jp/api/api-dev/how_to_use](https://www.e-stat.go.jp/api/api-dev/how_to_use)

### commands

#### e_stat

```
% pipenv run python -m e_stat --help
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

  e-statのAPIを簡単に利用するためのCLIツール

Options:
  --help  Show this message and exit.

Commands:
  boundary  境界データを取得
  ids       統計表ID一覧を取得
  merge-boundary  統計データと境界データを取得してマージする
  meta      統計表メタデータを取得
  stats     統計データを取得
```

#### boundary

```
% pipenv run python -m e_stat boundary --help
Usage: __main__.py boundary [OPTIONS]

  境界データを取得

Options:
  -p, --pref_name TEXT   取得するshpファイルの都道府県コードを入力  [required]
  -o, --output_dir TEXT  ダウンロードファイルを格納するディレクトリのパス文字列を入力  [required]
  --help                 Show this message and exit.
```

#### ids

```
% pipenv run python -m e_stat ids --help
Usage: __main__.py ids [OPTIONS]

  統計表ID一覧を取得

Options:
  -g, --gov_stats_code TEXT  取得したい統計表ID一覧の政府統計コードを入力  [required]
  -o, --output_dir TEXT      ダウンロードしたcsvを格納するディレクトリのパス文字列を入力  [required]
  --help                     Show this message and exit.
```

#### meta

```
% pipenv run python -m e_stat meta --help
Usage: __main__.py meta [OPTIONS]

  統計表メタデータを取得

Options:
  -st, --stats_table_id TEXT  取得したい統計表メタデータの統計表IDを入力  [required]
  -o, --output_dir TEXT       ダウンロードしたcsvを格納するディレクトリのパス文字列を入力  [required]
  --help                      Show this message and exit.
```

#### stats

```
% pipenv run python -m e_stat stats --help
Usage: __main__.py stats [OPTIONS]

  統計データを取得

Options:
  -a, --areas TEXT            取得する統計データの標準地域コードをカンマ区切り文字列で入力(例:01101,01103,01105)  [required]

  -c, --class_codes TEXT      取得する統計データの項目をカンマ区切り文字列で入力(例:A1101,A110101,A110101)  [required]

  -y, --years TEXT            取得する統計データの年度をカンマ区切り文字列で入力(例:2000,2005,2010)  [required]

  -st, --stats_table_id TEXT  取得したい統計データの統計表IDを入力  [required]
  -o, --output_dir TEXT       ダウンロードしたcsvを格納するディレクトリのパス文字列を入力  [required]
  --help                      Show this message and exit.
```

#### merge-boundary

```
% pipenv run python -m e_stat merge-boundary --help
Usage: __main__.py merge-boundary [OPTIONS]

  統計データと境界データを取得してマージする

Options:
  -p, --pref_name TEXT        取得するshpファイルの都道府県名を入力  [required]
  -d, --download_dir TEXT     ダウンロードするshpファイルを格納するディレクトリのパス文字列を入力  [required]
  -a, --area TEXT             取得する統計データの標準地域コードを入力  [required]
  -c, --class_code TEXT       取得する統計データの項目を入力  [required]
  -y, --year TEXT             取得する統計データの年度を入力  [required]
  -st, --stats_table_id TEXT  取得したい統計データの統計表IDを入力  [required]
  -o, --output_dir TEXT       ダウンロードしたcsvを格納するディレクトリのパス文字列を入力  [required]
  --help                      Show this message and exit.
```

### example

- 各種コマンドはサンプルとしてshell scriptを用意しているので、そちらも参照

```shell script
% pipenv run python -m e_stat merge-boundary \
  -p 北海道 \
  -d ./download_file \
  -a 01101 \
  -c A1101 \
  -y 2000 \
  -st 0000020101 \
  -o ./created
```

or

```shell script
% bash merge_boundary.sh
```

### work flow

#### get boundary data

- 取得したい境界データの都道府県とダウンロード先のディレクトリを指定しshpが格納されたzipファイルをダウンロードします。
    - 都道府県は`/e_stat_api_tools/e_stat/assets/pref_code.json`に記載されています。

```
% pipenv run python -m e_stat boundary \
  -p 北海道 \
  -d ./download_file
```

#### get raw data of stats

- `e_stat/assets/government_statistics_codes.tsv`または以下の公式ページから取得したい政府統計名の政府統計コードを確認します。
    - [政府統計コード一覧](https://www.e-stat.go.jp/help/stat-search-3-5)
    - [政府統計一覧](https://www.e-stat.go.jp/stat-search/database?page=1)
-  取得したい統計表ID一覧の政府統計コードとcsv書き出し先のディレクトリを指定して、`ids`コマンドを実行します。

```
% pipenv run python -m e_stat ids \
  -g 00200502 \
  -o ./created
```

- 書き出された`stats_ids.csv`から取得したい統計表のメタデータ（詳細項目）を確認して`meta`コマンドに統計表ID（`TABLE_INF`カラム）を指定して実行します。

```
% pipenv run python -m e_stat meta \
  -st 0000010101 \
  -o ./created
```

- 取得したい統計表の「標準地域コード、詳細項目、年度」をカンマ区切り文字列で指定、さらに統計表IDと書き出し先ディレクトリを指定し`stats`コマンドを実行します。
    - 標準地域コード：`/e_stat/assets/standard_area_codes.csv`または[市区町村を探す](https://www.e-stat.go.jp/municipalities/cities/areacode) から探せます。
    - 詳細項目：`meta`コマンドで取得した`meta_data.csv`に記載の`CLASS_CODE`カラムのデータです。
    - 年度：データによって異なりますが、多くは1975年頃からデータが存在します。

```
% pipenv run python -m e_stat stats \
  -a 01101,01105,01107,01203 \
  -c A1101,A110101,A110102,A1102,A110201,A110202 \
  -y 2000,2010 \
  -st 0000020101 \
  -o ./created
```

- 目的の`stats.csv`が書き出されます

#### create merged data from boundary and stats data

- 以下の項目を指定して`merge-boundary`コマンドを実行します。
    - 境界データの都道府県名を指定
    - shpが格納されたzipファイルのダウンロード先ディレクトリを指定
    - 取得したい統計データを指定
        - 標準地域コード
        - 統計表詳細項目
        - 取得年度
        - 統計表ID
    - ファイル書き出し先ディレクトリ
- 以下の点に注意してください。
    - APIの仕様上、統計データのレスポンスが10万件を超えるとデータが取得できないため、取得したい地域や項目は絞った方が良い。
    - 取得する境界データと、統計データの地域が異なる（北海道を指定したのに、標準地域コードは青森県の地域を指定した、等）場合はデータが生成されない。
    - 取得する境界データに市区町村よりも細かい境界（町丁目など）はdissolveされます。

```
% pipenv run python -m e_stat merge-boundary \
  -p 北海道 \
  -d ./download_file \
  -a 01101 \
  -c A1101 \
  -y 2000 \
  -st 0000020101 \
  -o ./created
```

- `-d`オプションで指定したディレクトリにzipファイルが格納されます。
- `-o`オプションで指定したディレクトリには以下のファイルが格納されます。
    - 境界データをそのまま変換したファイル
        - `boundary.geojson`
        - `boundary.csv`
    - 境界データと統計データを結合したファイル
        - `merge_boundary.geojson`
        - `merge_boundary.csv`
    
※ このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。