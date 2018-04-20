import json
with open('data.json') as json_file:  
  data = json.load(json_file)
nuevoDato = "La nueva tabla"
data['bases'].append({"data": nuevoDato})
data['bases'].append({"data": "Lesly"})
data['bases'].append({"data": "El club del arbol"})
print data

