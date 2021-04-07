# gecoshc-client
Help Channel client for GECOS workstations.

This Help Channel client validates the workstation against the GECOS CC and then connects to the appropiate Help Channel Server (basically a UVNC Repeater) by using x11vnc.

# Relathionship with other projects
This project includes:
* websocket-client 0.58.0 (https://pypi.python.org/pypi/websocket-client/)

This project is part of the GECOS environment.

# Building
To build this project in a Debian system execute:
``
dpkg-buildpackage -us -uc
``

# Installing
To install this project use the DEB package by:
``
sudo dpkg -i gecosws-hc-client_<version>_all.deb 
sudo apt-get -f install
``

# Configuring
After installing is important to configure the client by editing /etc/helpchannel.conf file.
The most important thing to configure is the Help Channel server URL (tunnel_url):
```
[TunnelConfig]
command_full_path: /usr/bin/hctunnel.py
tunnel_url: wss://helpchannel.yourdomain.com/wsServer
local_port=6000
ssl_verify=False
```

If your SSL certificates are valid (not self-signed certificates) you may set "ssl_verify=True".
