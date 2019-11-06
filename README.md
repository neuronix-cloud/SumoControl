# SumoControl

Simple node app to control the Jumping Sumo from Parrot.

To install, first find the the IP of your machine with:

```
sudo ifconfig eth0 | grep inet
```

and the Wifi name (ESSID) of your Drone with:

```
sudo iwlist wlan0 scan  | grep ESSID
```

Then run `./setup.sh <local-ip> <drone-ssid>`.

You can now connect to the drone launching the application with: `./run.sh`

You can open the browser and display the following URL `http://<ip-address>:3000`.

Use the arrow keys to move your drone, space for high jump, shift for tap and the top buttons on the page for other moves.
