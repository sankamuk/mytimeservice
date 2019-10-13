from flask import Flask, jsonify
from datetime import date

app = Flask(__name__)

@app.route('/time')
def mytime():
  return jsonify({'now': str(date.today())})

if __name__ == '__main__' :
  app.run(debug=True, host='0.0.0.0', port=8080)

