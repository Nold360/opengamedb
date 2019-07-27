#!/usr/bin/env python3
####
# MongoDB Connection for Game API
#
from pymongo import MongoClient
from os import environ

class gameDB():
  host = None
  port = None
  user = None
  passwd = None
  client = None

  # Name of DB/collection in Mono
  database = None
  collection = None

  # MongoDB Objects
  db = None
  col = None
 
  ###
  # collection = console (ps2 default right now)
  def __init__(self, host='localhost', port=27017, user=None, passwd=None, database='games', collection='ps2'):
    try: self.host = str(environ['MONGO_DB'])
    except: self.host = host

    try: self.user = str(environ['MONGO_INITDB_ROOT_USERNAME'])
    except: self.user = user

    try: self.passwd = str(environ['MONGO_INITDB_ROOT_PASSWORD'])
    except: self.passwd = passwd

    try: self.database = str(environ['MONGO_DB_NAME'])
    except: self.database = database

    self.collection = collection
    self.connect()

  def connect(self):
    try:
      self.close()
    except: pass

    self.client = MongoClient(self.host, username=self.user, password=self.passwd, authSource='admin')
    self.db = self.client[self.database]
    self.col = self.db[self.collection]

  def close(self):
    return self.client.close()

  def get_title_by_id(self, serial):
    return self.col.find_one({"id": str(serial)})

  # insert json_data in collection
  def import_json(self, json_path, collection):
    from json import load
    self.connect()
    col = self.db[collection]
    with open(json_path) as f:
      file_data = load(f)
    assert file_data
    for title in file_data:
      for title_id in title:
        tid = title_id.replace('_', '-').replace('.', '')
        for field in title[title_id]:
          for fname in field:
            col.update_one({'id': tid}, { '$set': { "artwork."+fname: field[fname]}})
    return self.close()
