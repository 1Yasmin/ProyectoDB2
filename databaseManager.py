import json
import os
import os.path
class databaseManager:

	def __init__(self):
		# Verificar que exista la carpeta 'databases' que es donde se crearan las bases de datos
		os.chdir("C:\\")
		if os.path.exists("C:\\databases") == False:
			os.mkdir("databases")
		os.chdir("C:\\databases")
		# Verificar que exista el archivo de metadata databases/metadata.json
		if os.path.exists("C:\\databases\metadata.json") == False:
			print 'no existe, se creo'
			metadata = {}
			metadata['bases'] = [] 
			#os.mkdir("databases/metadata.json")
			with open('metadata.json', 'w') as outfile:
				json.dump(metadata, outfile)
			print metadata
		else:
			print 'Si'
		
		# Si no existe, crearlo

        def useDatabase(self, db):
		# Verificar que databaseName sea una base de datos existent
				os.chdir("C:\\databases")
				list = os.listdir(".")
				valid = True
				for elemento in list:
					if elemento == db:
						print 'estas usando la base d datos ' + db
						os.chdir(db)
					else:
						valid = False
				if valid == False:
					print 'La base de datos no existe'
                
				
	def createDatabase(self, name):
		#validar que ninguna carpeta tenga ese nombre
		list = os.listdir(".")
		valid = True
		for elemento in list:
			if elemento == name:
				print 'La base de datos ya existe, cambie el nombre'
			else:
				valid = False
		if valid == False:
			# Crear carpeta con el nombre name
			os.mkdir(name)
			# Modificar archivo de metadata para agregar un nuevo database
			with open('metadata.json', 'r') as file:
				data = json.load(file)
				print data
			data['bases'].append({"data": name})
			with open('metadata.json', 'w') as file:
				json.dump(data, file)

	def showDatabase(self):
		list = os.listdir(".")
		print 'Las bases de datos disponibles:'
		for elemento in list:
			if elemento != "metadata.json":
				print elemento
		
	def setCurrentDatabase(self, databaseName):
		# Verificar que databaseName sea una base de datos existent
		pass
		# Setear la currentDatabase a databaseName
	def createTable(self, tableName, columnas):
	
		# Verificar que la tabla no exista ya en la base de datos
		pass
		# Crear el archivo para la tabla
