from flask import Flask, request, jsonify, abort
from datetime import datetime
import configparser
import pytz
import os


app = Flask(__name__)

def authmod(usernm, passwd):
  authcfg = configparser.ConfigParser()
  authcfg.read('/config/auth.property')
  try :
    return ( authcfg['USER'][usernm] == passwd )
  except KeyError :
    return False

@app.route('/time')
def mytime():
  if "HTTP_AUTHORIZATION" not in request.environ.keys() or 'Basic' not in request.environ["HTTP_AUTHORIZATION"] :
    abort(403)
  reqauth = request.authorization
  if (authmod(reqauth['username'], reqauth['password'])) :
    datetmwithzn = pytz.timezone(os.environ['MY_TIMEZONE'])
    return jsonify({'now': str(datetmwithzn.localize(datetime.now()))})
  else :
    abort(403)

if __name__ == '__main__' :
  app.run(debug=True, host='0.0.0.0', port=8080)

