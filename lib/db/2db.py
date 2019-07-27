import json

with open('artdb.json', 'r') as f:
  json_data = json.load(f)

for title in json_data:
  for sid in title:
    print(sid)
    for e in title[sid]:
      try: print(e['BG']) 
      except: pass
