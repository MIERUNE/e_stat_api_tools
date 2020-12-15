#!/bin/bash

pipenv run python -m e_stat merge-boundary \
  -p 北海道 \
  -d ./download_file \
  -a 01101 \
  -c A1101 \
  -y 2000 \
  -st 0000020101 \
  -o ./created