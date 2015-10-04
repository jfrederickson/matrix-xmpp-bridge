#!/usr/bin/env python

import sys
import logging
import getpass
from optparse import OptionParser
import requests
import json
import ConfigParser

import sleekxmpp

config = ConfigParser.ConfigParser()
config.read('/etc/mxbridge.conf')
MXAPI = config.get("Matrix", "as_api_url")
MXROOM = config.get("Matrix", "room_id")

class BridgeBot(sleekxmpp.ClientXMPP):
  def __init__(self, jid, password, room, nick):
    sleekxmpp.ClientXMPP.__init__(self, jid, password)
    self.room = room
    self.nick = nick
    
    self.add_event_handler("session_start", self.start)
    self.add_event_handler("groupchat_message", self.muc_message)
    
  def start(self, event):
    self.get_roster()
    self.send_presence()
    self.plugin['xep_0045'].joinMUC(self.room,
                                    self.nick,
                                    wait=True)
    
  def muc_message(self, msg):
    if(msg['mucnick'] != self.nick):
      data = {"from": "test", "to": MXROOM, "body": msg['mucnick'] + ": " + msg['body']}
      requests.post(MXAPI + "/mxbridge/send", data=json.dumps(data), headers={"Content-Type": "application/json"})

#if sys.version_info < (3, 0):
  #reload(sys)
  #sys.setdefaultencoding('utf8')



if(__name__ == '__main__'):
  jid = config.get("XMPP", "username")
  room = config.get("XMPP", "muc_room")
  nick = config.get("XMPP", "nick")
  
  try:
    password = config.get("XMPP", "password")
  except ConfigParser.NoOptionError:
    password = getpass.getpass("Password: ")
  
  xmpp = BridgeBot(jid, password, room, nick)
  xmpp.register_plugin('xep_0045')
  
  if xmpp.connect():
    try:
      xmpp.process(block=True)
    except TypeError:
      xmpp.process(threaded=False) # Used for older versions of SleekXMPP
    print("Done")
  else:
    print("Unable to connect.")