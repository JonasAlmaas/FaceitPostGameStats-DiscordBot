@ECHO OFF

CD ..\

SET SERVER_IP=
SET SERVER_USER=
SET FILE_SRC=
SET FILE_DEST=

SCP %FILE_SRC% %SERVER_USER%@%SERVER_IP%:%FILE_DEST%

SET CMD_LOAD=docker load -i %FILE_DEST%
SET CMD_RUN=docker run --env-file=.env_docker -d -p 8080:8080 --restart unless-stopped faceit-bot:latest

ssh -t %SERVER_USER%@%SERVER_IP% "%CMD_LOAD% && %CMD_RUN%"

PAUSE
