sudo dhclient -r wlan0 
sudo wpa_cli scan
sudo dhclient -v wlan0
while ! ping -c 1 192.168.2.1
do echo Trying to connect ; sleep 1
done
echo "Connected"
node index.js
