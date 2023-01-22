# Faceit post game stats - Discord bot

## Config

Create a **.docker_env** file on the server.

Add the following variables into the file.

FACEIT_API_KEY=
FACEIT_PLAYER_ID=
NUMBERS_OF_MATCHES=
BOT_TOKEN=
BOT_CHANNEL_ID=

## Deploy with Docker

### Building image

* Build docker image: **`docker build -t faceit-bot:latest .`**
* Create the folder `dist/docker`
* Save the image to a file: `docker save -o dist/docker/faceit-bot.tar faceit-bot:latest`
* Remove the image from the local reg: `docker rmi faceit-bot:latest`

### Sending to server

Copy the file to the server `scp dist/docker/faceit-bot.tar root@<ip>:/root/docker/faceit-bot.tar`

Alternativly you can run `scp dist/docker/faceit-bot.tar <username>@<ip>:/home/<username>/docker/faceit-bot.tar` (This does require the user to be in the docker group or have sudo access.)

### Running container

Run the following commmands on the server. Can you ssh for this

Remember to configure the `.env_docker` file before running the docker container.

* Load the image from file: `docker load -i /root/docker/faceit-bot.tar`
* Run the container: `docker run --env-file=.env_docker -d -p 8080:8080 --restart unless-stopped faceit-bot:latest`
