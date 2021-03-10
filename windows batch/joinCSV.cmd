@echo off

SETLOCAL
SET /A header = 1
SET fname=Full.csv
DEL *batch_param_map.csv
>new.csv.tmp (
  FOR %%F IN (*.csv) DO (
    IF DEFINED header (
      TYPE "%%F"
      SET "header="
      SET fname=Full%%F
    ) ELSE MORE +1 "%%F"
  )
)
DEL Reporte*.csv
REN new.csv.tmp "%fname%"
