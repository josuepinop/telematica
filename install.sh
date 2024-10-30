#!/bin/sh
sudo apt update
sudo apt install docker-compose -y
sudo apt install git
#git clone https://github.com/josuepinop/telematica.git
#cd proyecto
sudo docker-compose up -d
