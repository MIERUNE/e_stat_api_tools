# e_stat_api_sample

e-statのAPIを簡単に利用するためのCLIツール

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

### command

```shell script
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

% pipenv run python -m e_stat boundary --help
Usage: __main__.py boundary [OPTIONS]

  境界データを取得

Options:
  -p, --pref_name TEXT   取得するshpファイルの都道府県コードを入力  [required]
  -o, --output_dir TEXT  ダウンロードファイルを格納するディレクトリのパス文字列を入力  [required]
  --help                 Show this message and exit.

e% pipenv run python -m e_stat ids --help
Usage: __main__.py ids [OPTIONS]

  統計表ID一覧を取得

Options:
  -g, --gov_stats_code TEXT  取得したい統計表ID一覧の政府統計コードを入力  [required]
  -o, --output_dir TEXT      ダウンロードしたcsvを格納するディレクトリのパス文字列を入力  [required]
  --help                     Show this message and exit.

% pipenv run python -m e_stat meta --help
Usage: __main__.py meta [OPTIONS]

  統計表メタデータを取得

Options:
  -st, --stats_table_id TEXT  取得したい統計表メタデータの統計表IDを入力  [required]
  -o, --output_dir TEXT       ダウンロードしたcsvを格納するディレクトリのパス文字列を入力  [required]
  --help                      Show this message and exit.

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

e% pipenv run python -m e_stat merge-boundary --help
Usage: __main__.py merge-boundary [OPTIONS]

  統計データと境界データを取得してマージする

Options:
  -p, --pref_name TEXT        取得するshpファイルの都道府県コードを入力  [required]
  -d, --download_dir TEXT     ダウンロードするshpファイルを格納するディレクトリのパス文字列を入力  [required]
  -a, --area TEXT             取得する統計データの標準地域コードを入力  [required]
  -c, --class_code TEXT       取得する統計データの項目を入力  [required]
  -y, --year TEXT             取得する統計データの年度を入力  [required]
  -st, --stats_table_id TEXT  取得したい統計データの統計表IDを入力  [required]
  -o, --output_dir TEXT       ダウンロードしたcsvを格納するディレクトリのパス文字列を入力  [required]
  --help                      Show this message and exit.

```

### example

```shell script
pipenv run python -m e_stat merge-boundary \
  -p 北海道 \
  -d ./download_file \
  -a 01101 \
  -c A1101 \
  -y 2000 \
  -st 0000020101 \
  -o ./created_csv
```

or

```shell script
% bash merge_boundary.sh
```