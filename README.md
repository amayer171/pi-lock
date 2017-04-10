# pi-lock
code for controller raspberry pi webserver and door lock mechanism
To startup as a background process:
nohup sudo python3 ./server.py &
See /etc/init.d/pythonDoorOpener for current startup script
sudo update-rc.d pythonDoorOpener defaults
was used in order to register the script for startup
