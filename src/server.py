#####
# Stupid Simple GameDB API using Flask, nginx & MongoDB
# Use by libopl to obtain metadata & artworks
# TODO: Insert links & stuff
#
from flask import Flask, abort, jsonify
from bson import ObjectId
from lib import db

import re
import os
import json

app = Flask(__name__)

# Override
class JSONEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, ObjectId):
      return str(o)
    return jsonify(json.JSONEncoder.default(self, o))

def __connect_db(col):
  return db.gameDB(collection=col)

# Search DB for title
def __get_title_by_id(col, media_id):
  dbc = __connect_db(col)

  # Try uniform media_id
  mid = media_id.replace('.', '').replace('_', '-')
  try: 
    if '-' not in mid[4]:
      mid = mid[:4]  + '-' + mid[4:]
    if len(mid) != 10:
      return None
  except Exception as e: 
    dbc.close()
    return None

  title = dbc.get_title_by_id(mid)
  dbc.close()
  return title

# Create OPL id from title_id
def __opl_id(title_id):
  oplid = title_id.replace('-', '_')
  oplid = oplid.replace('.', '')
  try: 
    oplid = oplid[:8] + "." + oplid[8:]
  except:
    oplid = None
  return oplid.upper()



# Check if media_id is valid
def __is_valid_title_id(media_id):
  r = re.compile(r'[a-zA-Z]{4}.?\d{3}\.?\d{2}')
  if not r.match(str(media_id).strip()):
    return False

  if len(media_id) > 11 or len(media_id) < 8:
    return False
  return True

# Nothing here
@app.route('/')
def index():
  return "Open Game Database API"

# Search for a media id for a console
@app.route('/v1/<console_name>/<media_id>', methods=['GET'])
def media(console_name, media_id):
  if not __is_valid_title_id(str(media_id)): return str(media_id)

  title = __get_title_by_id(console_name, media_id)
  if not title: abort(404)
    
  # Add OPL-ID Format:
  title.update({ "opl_id": __opl_id(title["id"])})

  #remove _id index from mongodb
  del title["_id"]
  
  return jsonify(title)

@app.errorhandler(404)
def not_found(e):
  return {"error": "title_not_found (%s)" % str(e)}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
