#!/bin/bash
# Remove old config
rm -rf ~/.vnc/xstartup
rm -rf ~/.vnc/ip-*
export HOME=/root/
export USER=root
cat ~/.vnc/xstartup
cat <<EOT >> ~/.vnc/xstartup
#!/bin/sh

export XKL_XMODMAP_DISABLE=1
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS

[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r /root/.Xresources ] && xrdb /root/.Xresources
xsetroot -solid grey
vncconfig -iconic &

gnome-panel &
gnome-settings-daemon &
metacity &
nautilus &
gnome-terminal &
EOT
chmod +x ~/.vnc/xstartup
killall screen
vncserver -kill :1
vncserver -geometry 1280x720
screen -d -m -S novnc /home/ubuntu/noVNC-1.2.0/utils/launch.sh --vnc localhost:5901
export DISPLAY=:1

rm -rf /home/ubuntu/fb-zoo/app.log
sudo apt install -y xvfb
cd /home/ubuntu/fb-zoo/ && pip3 install -r requirements.txt
cd /home/ubuntu/fb-zoo/ && python3 -m app.main
host=`hostname -I | awk '{print $1}'`
DESCRIBE_COMMAND=$(aws ec2 describe-instances \
                   --filters Name=network-interface.addresses.private-ip-address,Values=$host \
                   --query 'Reservations[*].Instances[*].{Instance:InstanceId}' \
                   --output text)
echo $DESCRIBE_COMMAND
#aws ec2 terminate-instances --instance-ids $DESCRIBE_COMMAND