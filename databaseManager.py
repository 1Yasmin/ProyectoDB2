import json
import os
import os.path
import funciones
import shutil

class databaseManager:

    baseActual = ""

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
        global baseActual
        # Verificar que databaseName sea una base de datos existent
        os.chdir("C:\\databases")
        if funciones.validarExistencia(".", db):
            print 'estas usando la base d datos ' + db
            baseActual = db
            os.chdir(db)
        else:
            print 'La base de datos no existe'
                
                
    def createDatabase(self, name):
        os.chdir("C:\\databases")
        #validar que ninguna carpeta tenga ese nombre
        if funciones.validarExistencia(".", name):
            print "Ya existe la base de datos, cambie el nombre"
        else:
        # Crear carpeta con el nombre name
            os.mkdir(name)
            # Modificar archivo de metadata para agregar un nuevo database
            with open('metadata.json', 'r') as file:
                data = json.load(file)
                print data
            data['bases'].append({"data": name, 'tables': 0})
            with open('metadata.json', 'w') as file:
                json.dump(data, file)
            #Crear archivo de metadata de las tablas
            metadataTabla = {}
            metadataTabla['tables'] = [] 
            with open("C:\\databases\\"+name+"\metadataTabla.json", 'w') as outfile:
                json.dump(metadataTabla, outfile)

    def showDatabase(self):
        list = os.listdir(".")
        print 'Las bases de datos disponibles:'
        for elemento in list:
            if elemento != "metadata.json":
                print elemento
        
    def createTable(self, tableName, columnas):
        # Verificar que la tabla no exista ya en la base de datos
        if funciones.validarExistencia("c:\\databases\\"+baseActual, tableName):
            print 'La tabla ya existe, cambie el nombre'
        else:
            # Modificar la metadata de las tablas
            with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'r') as file:
                data = json.load(file)
                print data
            data['tables'].append({'name':tableName, 'cantRegistros': 0, 'cantRestricciones': 0})
            with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'w') as file:
                json.dump(data, file)
            # Modificar archivo de metadata para agregar una nueva tabla a la base de datos actual
            n = 0

            with open('C:\\databases\metadata.json', 'r') as file:
                data = json.load(file)
                print n
                print len(data['bases'])
                while n < len(data['bases']):
                    print n
                    if data['bases'][n]['data'] == baseActual:
                        tableNum = data['bases'][n]['tables']
                        tableNum = tableNum + 1
                        print tableNum
                        data['bases'][n] = {"data": baseActual, "tables": tableNum}
                        #data['bases'].append({"data": name})
                        with open('C:\\databases\metadata.json', 'w') as file:
                            json.dump(data, file)
                    n = n + 1

            # Crear el archivo para la tabla
            nombre = "Tabla"+tableName
            nombre = {}
            nombre['columnas'] = [] 
            nombre['constraints'] = [] 
            nombre['registros'] = [] 
            
            list = columnas
            for i in list:
                nombre['columnas'].append({'name': i.column_name().getText(), 'type': i.type_name().getText()})

            with open("c:\\databases\\"+baseActual+'\\'+"Tabla"+tableName+'.json', 'w') as outfile:
                json.dump(nombre, outfile)


    # TODO: Pendiente de completar
    def tableConstraint(self, name, columnName, expr, foreignKey):
        with open('data.json', 'r') as file:
            data = json.load(file)

        print n

        data['constraints'].append({"tipo": "hola"})

        with open('data.json', 'w') as file:
            json.dump(data, file)

        
    def insertStmt(self, tableName, expr, columnName):
        pass
        
    def dropDatabase(self, database_name):
        os.chdir("C:\\databases")
        if funciones.validarExistencia(".", database_name):
            shutil.rmtree("c:\\databases\\"+database_name)
            print "La base de datos " + database_name + " fue eliminada"
        else:
            print "La base de datos no existe"
        
    # def alterTable(self, tableName, newTableName, columnDef, tableConstraint, columnName, name):
        # os.chdir("C:\\databases\\"+baseActual)

        # with open('C:\\databases\metadata.json', 'r') as file:
                # data = json.load(file)
        
        
    def alterDatabase(self, databaseName, newDatabaseName):
        #8os.chdir("C:\\databases\\"+baseActual)
        # os.chdir("C:\\databases")
        # print baseActual + newDatabaseName
        # os.rename(baseActual, newDatabaseName)
        # print "La base de datos " + databaseName + " fue renombrada como " + newDatabaseName
        #else:
        #print "La base de datos no existe"
        
        #Verificar que databaseName sea una base de datos existent
        os.chdir("C:\\databases")
        if funciones.validarExistencia(".", databaseName):
            os.rename(databaseName, newDatabaseName)
            print "La base de datos " + databaseName + " fue renombrada como " + newDatabaseName
            baseActual = databaseName
            os.chdir(newDatabaseName)
        else:
            print 'La base de datos no existe'
            


            
