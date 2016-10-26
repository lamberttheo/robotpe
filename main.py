#!/usr/bin/python -O

import redis, random, threading, time
import globalConfig, robotControl, sendMail, videoProcessing
from bottle import route, run, request, response, redirect, template, static_file

db = redis.Redis('localhost')

@route('/assets/<filepath:path>')
def assets(filepath):
  return static_file(filepath, root='assets/')

@route('/')
def index():
  user = "nobody"
  if request.get_cookie("session") and db.get("session") == request.get_cookie("session"):
    user = "the one"
  elif db.exists("session"):
    user = "a guest"
  return template('index', serverIP = sendMail.get_ip_address("wlan0"), user = user)

@route('/controls/<stick1x>/<stick1y>/<stick2x>/<stick2y>')
def controls(stick1x, stick1y, stick2x, stick2y):
  if request.get_cookie("session") and db.get("session") == request.get_cookie("session"):
    globalConfig.leftJoystickX = int(stick1x)
    globalConfig.leftJoystickY = int(stick1y)
    globalConfig.rightJoystickX = int(stick2x)
    globalConfig.rightJoystickY = int(stick2y)
    globalConfig.lastHTTPrequest = time.time()
    # Session lifetime, resetted once every 10s
    if db.ttl("session") < 50:
      db.expire("session", 60)
  return 'stick1x = ' + stick1x + " stick1y = " + stick1y + " stick2x = " + stick2x + " stick2y = " + stick2y

@route('/login')
def login():
  if not db.exists("session"):
    random_value = str(random.getrandbits(128))
    db.set("session", random_value)
    db.expire("session", 60)
    db.bgsave()
    response.set_cookie("session", random_value)

    ledThread = threading.Thread(None, robotControl.toggleLED)
    ledThread.start()
    ledThread._Thread__stop()
    return 'connected'
  elif request.get_cookie("session") and db.get("session") == request.get_cookie("session"):
    return 'connected'
  else:
    return 'waiting'

@route('/logout')
def logout():
  if request.get_cookie("session") and db.get("session") == request.get_cookie("session"):
    db.delete("session")
    db.bgsave()
    response.set_cookie("session", "")
  return 'offline'

@route('/status')
def status():
  if not db.exists("session"):
    return 'offline'
  elif request.get_cookie("session") and db.get("session") == request.get_cookie("session"):
    return 'connected'
  else:
    return 'waiting'

run(host='0.0.0.0', port=globalConfig.webserverPort, debug=True)
