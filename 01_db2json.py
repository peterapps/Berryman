import xmltodict
import json

f = open('hsdb.xml','r')
db = xmltodict.parse(f.read())
f.close()

f = open('hsdb.json','w')
json.dump(db, f)
f.close()
