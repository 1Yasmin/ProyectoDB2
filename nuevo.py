import json
n = 0

while n != 3:
	with open('data.json', 'r') as file:
		data = json.load(file)
		print data
	print('Data:')
	nuevoDato = raw_input()
	print nuevoDato
	data['bases'].append({"data": nuevoDato})
	with open('data.json', 'w') as file:
		json.dump(data, file)
	n = n+1


