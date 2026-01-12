import json
import os


def load(file):
  try:
   with open(os.path.dirname(__file__)[:-6] + "\\" + file, "r", encoding='utf-8') as f:
     return json.load(f)
   
  except:
    return {"commands" : {}, "plugins" : {}, "cache": {"qm" : False, "nm" : False, "logs" : False, "last_hp" : False}}
  

def dump(file, data):
  with open(os.path.dirname(__file__)[:-6] + "\\" + file, "w", encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
