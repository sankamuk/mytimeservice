import pytest
import app
import base64
import os

def test_auth():
  assert app.authmod('sankar', 'Password123') == True
  assert app.authmod('sankar', 'Password') == False

def test_hitrecorder():
  hits = app.hitrecorder()
  if 'TEST_ENV' in os.environ.keys() and os.environ['TEST_ENV'] == 'True' :
    perm_store = 'storage/hitcount.txt'
  else :
    perm_store = '/storage/hitcount.txt'
  with open(perm_store, 'r') as f:
    assert (len(f.read().split("\n")) - 1) == hits

def test_app():
  response = app.app.test_client().get('/time')
  assert response.status_code == 403
  valid_credentials = base64.b64encode(b'sankar:Password123').decode('utf-8')
  response = app.app.test_client().get('/time', headers={'Authorization': 'Basic ' + valid_credentials})
  assert response.status_code == 200
