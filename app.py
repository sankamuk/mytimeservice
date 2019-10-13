from flask import Flask, request, jsonify, abort
from datetime import datetime
import configparser
import pytz
import os


app = Flask(__name__)

# Calculate Total Hits
def hitrecorder():
  val = 1
  if 'TEST_ENV' in os.environ.keys() and os.environ['TEST_ENV'] == 'True' :
    perm_store = 'storage/hitcount.txt'
  else :
    perm_store = '/storage/hitcount.txt'
  with open(perm_store, 'a') as f:
    f.write(str(datetime.now())+"\n")
  with open(perm_store, 'r') as f:
    val = len(f.read().split("\n"))
  return ( val - 1)

# Handles Authentication & Authorization
def authmod(usernm, passwd):
  authcfg = configparser.ConfigParser()
  if 'TEST_ENV' in os.environ.keys() and os.environ['TEST_ENV'] == 'True' :
    authcfg.read('config/auth.property')
  else :
    authcfg.read('/config/auth.property')
  try :
    return ( authcfg['USER'][usernm] == passwd )
  except KeyError :
    return False

# Time Service
@app.route('/time')
def mytime():
  hits = hitrecorder()
  if "HTTP_AUTHORIZATION" not in request.environ.keys() or 'Basic' not in request.environ["HTTP_AUTHORIZATION"] :
    abort(403)
  reqauth = request.authorization
  if (authmod(reqauth['username'], reqauth['password'])) :
    datetmwithzn = pytz.timezone(os.environ['MY_TIMEZONE'])
    return jsonify({'now': str(datetmwithzn.localize(datetime.now())), 'hits': str(hits)})
  else :
    abort(403)

if __name__ == '__main__' :
  app.run(debug=True, host='0.0.0.0', port=8080)

