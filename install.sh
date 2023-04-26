#!/bin/bash
sudo apt-get update -y 
sudo apt update -y
sudo apt-get install -y git net-tools 
sudo apt install python3-pip -y
pip install docker -y

sudo ufw allow 2222/tcp

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

cd $HOME
git clone https://github.com/BenRedic-FyFazan/ctfkom-distributor.git

cd ./ctfkom-distributor
sudo docker build -t "ctf_test" .
