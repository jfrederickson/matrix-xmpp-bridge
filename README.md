NOTE: This project is no longer maintained (and never really made it past an experimental stage anyway)

# Matrix-XMPP Bridge
This project creates a bridge between a Matrix room and an XMPP MUC. It is currently very early in development and only relays messages one way (from XMPP to Matrix). Use it if you wish, but don't blame me if it blows up in your face.

## Using
- Add an AS and HS token to registration.yaml and reference it in your homeserver config as described [here](http://matrix.org/blog/2015/03/02/introduction-to-application-services/)
- Edit mxbridge.conf.example with user and room details for the Matrix/XMPP rooms you would like to bridge and save as /etc/mxbridge.conf
- Start appservice.py and xmpp_component.py in a screen session

## Dependencies
- sleekxmpp
- configparser
- requests
- flask
