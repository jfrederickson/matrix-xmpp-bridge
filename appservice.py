# app_service.py:

import json, requests
from flask import Flask, jsonify, request
import xmpp_component as xmpp
import ConfigParser
app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('/etc/mxbridge.conf')
TOKEN = config.get("Matrix", "token")
APIURL = config.get("Matrix", "api_url")

# Observe all the things forever
# TODO: Send these to XMPP
@app.route("/transactions/<transaction>", methods=["PUT"])
def on_receive_events(transaction):
    events = request.get_json()["events"]
    #if(event['type'] == 'm.room.message'):
      #xmpp.sendMessage(event['user_id'] + ': ' + event['content']['body'])
    for event in events:
        print "User: %s Room: %s" % (event["user_id"], event["room_id"])
        print "Event Type: %s" % event["type"]
        print "Content: %s" % event["content"]
    return jsonify({})
  
# Create this room if it doesn't exist
@app.route("/rooms/<alias>")
def query_alias(alias):
  alias_localpart = alias.split(":")[0][1:]
  createRoom(TOKEN, alias_localpart)
  print('Room alias: ' + alias)
  return jsonify({})

def createRoom(as_token, alias_localpart):
  roomCreateURL = APIURL + "/createRoom?access_token=" + as_token
  data = json.dumps({
    "room_alias_name": alias_localpart
  })
  resp = requests.post(roomCreateURL, data=data, headers={"Content-Type": "application/json"})
  print('Room creation URL: ' + roomCreateURL)
  print('Data: ' + data)
  print(resp.text)
  
@app.route("/mxbridge/send", methods=["POST"])
def sendMessage():
  print(request.data)
  req = request.get_json()
  
  sender = req["from"]
  #sender = request.args.get('from')
  xmppRecipient = req["to"]
  #xmppRecipient = request.args.get('to')
  message = req["body"]
  #message = request.args.get('body')
  print('Sending to room: ' + str(xmppRecipient))
  
  #recipient = xmppMap(xmppRecipient)
  
  joinRoom(token=TOKEN, roomid=xmppRecipient)
  sendMessageURL = APIURL + "/rooms/" + xmppRecipient + '/send/m.room.message?access_token=' + TOKEN
  body = json.dumps({
    "msgtype": "m.text",
    "body": message
  })
  requests.post(sendMessageURL, data=body, headers={"Content-Type": "application/json"})
  
  return jsonify({})


def joinRoom(token, roomid):
  if(token != None and roomid != None):
    requests.post(APIURL + '/' + roomid + '/join?access_token=' + token)
  elif(token == None):
    print("Must include access token!")
  elif(roomid == None):
    print("Must include roomid!")
    

if __name__ == "__main__":
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
