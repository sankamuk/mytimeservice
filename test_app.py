import pytest
import app
import os.path

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
