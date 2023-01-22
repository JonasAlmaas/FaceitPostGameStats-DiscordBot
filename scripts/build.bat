@ECHO OFF

CD ..\

docker build -t faceit-bot:latest .

SET DIST_PATH="%cd%\dist\docker"

IF NOT EXIST %DIST_PATH% MKDIR %DIST_PATH%
IF EXIST %DIST_PATH%\faceit-bot.tar DEL /F %DIST_PATH%\faceit-bot.tar

docker save -o %DIST_PATH%\faceit-bot.tar faceit-bot:latest

docker rmi faceit-bot:latest

PAUSE
