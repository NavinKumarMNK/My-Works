#!/bin/sh
# author: @NavinKumarMNK
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install curl vim build-essential ca-certificates git wget htop

# microsoft edge browser installation
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list'
sudo rm microsoft.gpg 
sudo apt-get update
sudo apt-get install microsoft-edge-stable

# update the nvidia-driver if its needed
# manually install tor-browser. [optional] and extract to the folder ~/apps/tor-browser
# start the browser with the command  ./apps/tor-browser/Browser/start-tor-browser

# Docker Enginer Install
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# install the docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# set docker to user permission
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
sudo chown $USER:$USER /var/run/docker.sock


# install nvidia-docker
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# change the docker storage path
NEW_DOCKER_DIR="$HOME/docker"
echo "{
  \"data-root\": \"$NEW_DOCKER_DIR\"
}" | sudo tee /etc/docker/daemon.json
sudo systemctl restart docker

# Install Tabby -> terminal
URL="https://github.com/Eugeny/tabby/releases/download/v1.0.207/tabby-1.0.207-linux-x64.deb"
TARGET_DIR="$HOME/Downloads"
wget -P "$TARGET_DIR" "$URL"
FILE_NAME=$(basename "$URL")
sudo dpkg -i "$TARGET_DIR/$FILE_NAME"
rm "$TARGET_DIR/$FILE_NAME"

# install vscode 
wget -qO - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /usr/share/keyrings/microsoft.gpg > /dev/null
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
sudo apt update
sudo apt install code
# sync with the github account.

# install jetbrains mono & firacode fonts.
sudo apt install fonts-firacode
wget https://download.jetbrains.com/fonts/JetBrainsMono-1.0.0.zip
unzip JetBrainsMono-1.0.0.zip
sudo mv JetBrainsMono-*.ttf /usr/share/fonts/
fc-cache -f -v

# ollama install
curl -fsSL https://ollama.com/install.sh | sh

# Run the customized docker container pulls

