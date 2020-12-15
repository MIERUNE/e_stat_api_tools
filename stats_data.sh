#!/bin/bash

pipenv run python -m e_stat stats \
  -a 01101,01105,01107,01203 \
  -c A1101,A110101,A110102,A1102,A110201,A110202 \
  -y 2000,2010 \
  -st 0000020101 \
  -o ./created_csv
