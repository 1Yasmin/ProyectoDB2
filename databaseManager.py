
import os
class databaseManager:

	def __init__(self):
		# Verificar que exista la carpeta 'databases' que es donde se crearan las bases de datos
		pass
		# Si no existe, crearla
		
		# Verificar que exista el archivo de metadata databases/metadata.json
		
		# Si no existe, crearlo

		# self.currentDatabase = null
		
	def createDatabase(self, name):
		# Crear carpeta con el nombre name
		#os.makedirs("C:\Users\Samantha Duarte\Documents\5TO SEMESTRE\Proyecto2BD\proyecto2-dbms\sql-python2")

		os.mkdir(name)
		
		# Modificar archivo de metadata para agregar un nuevo database
	
	def setCurrentDatabase(self, databaseName):
		# Verificar que databaseName sea una base de datos existent
		pass
		# Setear la currentDatabase a databaseName
	def createTable(self, tableName, columnas):
	
		# Verificar que la tabla no exista ya en la base de datos
		pass
		# Crear el archivo para la tabla
