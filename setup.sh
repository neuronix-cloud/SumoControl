#!/bin/bash
IP="${1:?local ip}"
SSID="${2:?drone SSID}"

# configure wifi connection to the drone
sudo wpa_cli <<EOF
remove_network 0
add_network 
set_network 0 $SSID
set_network 0 key_mgmt NONE 
enable_network 0
list_networks
EOF

sed -e "s|/video|http://$IP:3000/video|" <public/index.html.dist >public/index.html
sed -e "s|http://localhost:3000|http://$IP:3000|" <public/js/script.js.dist >public/js/script.js

npm install
