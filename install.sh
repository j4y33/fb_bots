#!/bin/bash

apt install ubuntu-desktop gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal xfce4
apt install tightvncserver
mkdir ~/.vnc/
sudo tee -a ~/.vnc/xstartup > /dev/null <<EOT
#!/bin/bash
xrdb $HOME/.Xresources
EOT
chmod +x ~/.vnc/xstartup
startxfce4 &
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
apt update
apt install google-chrome-stable
apt install unzip
wget https://chromedriver.storage.googleapis.com/87.0.4280.88/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
python get-pip.py
pip install numpy
wget https://github.com/novnc/noVNC/archive/v1.2.0.tar.gz
tar -xvf v1.2.0.tar.gz

apt install python3-pip
pip3 install awscli
apt install openvpn
update-rc.d -f openvpn remove


