import json
n = 0

while n != 10000:
	with open('data.json', 'r') as file:
		data = json.load(file)
	print n
	data['bases'].append({"data": "hola"})
	with open('data.json', 'w') as file:
		json.dump(data, file)
	n = n+1


