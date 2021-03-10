@echo off

SET PATH=%PATH%;c:\RepastSimphony-2.7\eclipse\jdk11\bin
::segundos entre creacion de instancias
SET /A delay = 10
::numero de instancias por defecto
SET /A inst = 4
::lee el parametro numero de instancias
IF NOT [%1]==[] (SET /A inst = %1)
::echo %inst%

CD complete_model
:: crea las instancias, separadas por un delay
FOR /L %%i IN (1, 1, %inst%) DO (
  echo Iniciando instancia numero %%i
  START "Instancia %%i" /MIN java -Xmn512m -cp "./lib/*" repast.simphony.batch.InstanceRunner -pxml ./scenario.rs/batch_params.xml -scenario ./scenario.rs -id $instance -pinput unrolledParamFile.txt
  TIMEOUT %delay% >nul
)
