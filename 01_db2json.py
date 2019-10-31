import xmltodict
import json

f = open('./data/hsdb.xml','r')
db = xmltodict.parse(f.read())
f.close()

f = open('./data/hsdb.json','w')
json.dump(db, f)
f.close()
