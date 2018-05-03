import json
import os
import os.path
import funciones
import shutil
import pdb
import sys

class databaseManager:

    baseActual = None
    tablaActual = ""

    def __init__(self):
    
        # Verificar que exista la carpeta 'databases' que es donde se crearan las bases de datos
        os.chdir("C:\\")
        if os.path.exists("C:\\databases") == False:
            os.mkdir("databases")
        os.chdir("C:\\databases")
        
        
        # Verificar que exista el archivo de metadata databases/metadata.json
        if os.path.exists("C:\\databases\metadata.json") == False:
            metadata = {}
            metadata['bases'] = [] 
            #os.mkdir("databases/metadata.json")
            with open('metadata.json', 'w') as outfile:
                json.dump(metadata, outfile)   
        print "Bienvenido al DBM de Yasmin y Samantha"

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
            print "Ya existe la base de datos, cambie el nombre por favor"
        else:
        # Crear carpeta con el nombre name
            os.mkdir(name)
            # Modificar archivo de metadata para agregar un nuevo database
            with open('metadata.json', 'r') as file:
                data = json.load(file)
                print data
            data['bases'].append({"name": name, 'tables': 0})
            with open('metadata.json', 'w') as file:
                json.dump(data, file)
            #Crear archivo de metadata de las tablas
            metadataTabla = {}
            metadataTabla['tables'] = [] 
            with open("C:\\databases\\"+name+"\metadataTabla.json", 'w') as outfile:
                json.dump(metadataTabla, outfile)

    def showDatabase(self):
        list = os.listdir("C:\\databases")
        print 'Las bases de datos disponibles:'
        for elemento in list:
            if elemento != "metadata.json":
                print elemento
        
    def createTable(self, tableName, columnas, constraint):
        #Verificar que la base de datos actual exista   
        if baseActual != None:
            # Verificar que la tabla no exista ya en la base de datos
            if funciones.validarExistenciaTable(baseActual, tableName):
                print 'La tabla ya existe, cambie el nombre'
            else:
                # Crear el archivo para la tabla
                nombre = "Tabla"+tableName
                nombre = {}
                nombre['columnas'] = [] 
                nombre['constraints'] = [] 
                nombre['registros'] = [] 
                
                list = columnas
                for i in list:
                    if funciones.tipoValido(i.type_name().getText().upper()):
                       
                        nombre['columnas'].append({'name': i.column_name().getText(), 'type': i.type_name().getText()})
                    else:
                        print "Uno de los tipos de datos no es valido \nLos tipos validos son: INT, FLOAT, CHAR y DATE"
                        sys.exit()
                const = constraint 
               # pdb.set_trace()
                if (const != []) == True:
                    a = 0
                    while a < len(const):
                        if funciones.tipoConstraint(const[a]) == 'PRIMARY':
                            nombre['constraints'].append(
                            {'type': 'PRIMARY', 
                            'name': funciones.validarValor(const[a].name()),
                            'column_name': funciones.columnName(const[a])
                            })
                            a = a+1
                        if funciones.tipoConstraint(const[a]) == 'FOREIGN':
                            nombre['constraints'].append(
                            {'type': 'FOREING', 
                            'name': funciones.validarValor(const[a].name()),
                            'column_name': funciones.columnName(const[a]),
                            'ref': funciones.validarValor(const[a].foreign_key_clause())
                            })
                            a = a+1
                        if funciones.tipoConstraint(const[a]) == 'CHECK':
                            nombre['constraints'].append(
                            {'type': 'CHECK', 
                            'name': funciones.validarValor(const[a].name()),
                            'column_name': funciones.columnName(const[a]),
                            'expr': funciones.validarValor(const[a].expr())
                            })
                            a = a+1
                        if funciones.tipoConstraint(const[a]) == 'UNIQUE':
                            nombre['constraints'].append(
                            {'type': 'UNIQUE', 
                            'name': funciones.validarValor(const[a].name()),
                            'column_name': funciones.columnName(const[a])
                            })
                            a = a+1
                with open("c:\\databases\\"+baseActual+'\\'+"Tabla"+tableName+'.json', 'w') as outfile:
                    json.dump(nombre, outfile) 
            # Modificar la metadata de las tablas
                with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'r') as file:
                    data = json.load(file)
                data['tables'].append({'name':tableName, 'cantRegistros': 0, 'cantRestricciones': len(const)})
                with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'w') as file:
                    json.dump(data, file)
            #Modificar archivo de metadata para agregar una nueva tabla a la base de datos actual

                with open('C:\\databases\metadata.json', 'r') as file:
                    data = json.load(file)
                    for n in range(len(data['bases'])):
                        if data['bases'][n]['name'] == baseActual:
                            tableNum = data['bases'][n]['tables']
                            tableNum = tableNum + 1
                            data['bases'][n] = {"name": baseActual, "tables": tableNum}
                            with open('C:\\databases\metadata.json', 'w') as file:
                                json.dump(data, file) 
        
        else:
            print "Seleccione la base de datos a utilizar \nUSE DATABASE nombre"

    def dropDatabase(self, database_name):
        global baseActual
        os.chdir("C:\\databases")
        if funciones.validarExistencia(".", database_name):
            print "Borrar base de datos " + database_name + " con 5 registros "
            deseaBorrar = raw_input("(si/no)")
            if deseaBorrar.upper() == "SI":
                shutil.rmtree("c:\\databases\\"+database_name)
                with open('C:\\databases\metadata.json', 'r') as file:
                    data = json.load(file)
                    #del data['bases'][1][database_name]  
                n = 0
                while n < (len(data['bases'])):
                    if data['bases'][n]['name'] == database_name:
                        del data['bases'][n]
                    n = n+1
                with open('C:\\databases\metadata.json', 'w') as file:
                    json.dump(data, file)
                baseActual = None
                print "La base de datos " + database_name + " fue eliminada"
            elif deseaBorrar.upper() == "NO":
                print "No se borro la base de datos"
            else:
                print "Por favor, escriba si o no"
        else:
            print "La base de datos no existe"
        
    def alterDatabase(self, databaseName, newDatabaseName):
        os.chdir("C:\\databases")
        if funciones.validarExistencia(".", databaseName):
            os.rename(databaseName, newDatabaseName)
            print "La base de datos " + databaseName + " fue renombrada como " + newDatabaseName
            baseActual = databaseName
            os.chdir(newDatabaseName)
        else:
            print 'La base de datos no existe'

    def showColumnsFrom(self,tableName):
        os.chdir("C:\\databases")
        with open("c:\\databases\\"+baseActual+'\Tabla'+tableName+'.json', 'r') as file:
                data = json.load(file)
        for i in range(len(data['columnas'])):
            print data['columnas'][i]['name']
            
    # columnName
    #CREATE TABLE Orders(OrderID int, OrderNumber int, PersonID int, CONSTRAINT pk PRIMARY KEY (OrderID,PersonID), CONSTRAINT pf FOREIGN KEY (PersonID,OrderID) REFERENCES Persons(PersonID,OrderNumber), CONSTRAINT limite CHECK (OrderNumber > 12), CONSTRAINT unico UNIQUE (OrderID, PersonID))
    def insertInto(self,tableName,expr,columnName):
        if baseActual != None:
            #Verificar que la tabla exista
            exist = False
            with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'r') as file:
                data = json.load(file)
            for i in range(len(data['tables'])):
                if data['tables'][i]['name'] == tableName:
                    exist = True
            if exist:
                #if len(expr) == len()
                pass
                
                #concordancia de datos a insertar  
                
                #Verificar columnas e insertar datos
                
            else:
                print "La tabla no existe en la base de datos "+baseActual
        # print "tableName "
        # print tableName
        # print "expr "
        # print expr[0]
        # print "columnNAme "
        # print columnName
        
    def dropTable(self,tableName): # Borrar el 1 de la metadata.json
        os.chdir("C:\\databases\\"+baseActual)
        if funciones.validarExistenciaTable(baseActual, tableName):
            
            print "Borrar tabla " + tableName + " con 5 registros "
            deseaBorrar = raw_input("(si/no)\n")
            if deseaBorrar == "si":
                # Se borra el archivo json de la tabla
                os.remove('Tabla'+tableName+'.json')
                with open("C:\\databases\\"+baseActual+"\\metadataTabla.json", 'r') as file:
                    data = json.load(file)
                # Se borra el objeto tabla del archivo json
                    n = 0
                    while n < (len(data['tables'])):
                        #print data['bases'][n]['name']
                        if data['tables'][n]['name'] == tableName:
                            del data['tables'][n]
                        n = n+1
                with open("C:\\databases\\"+baseActual+"\\metadataTabla.json", 'w') as file:
                    json.dump(data,file)
                # print data['tables']
                # del data['tables']
                print 'Se elimino la tabla '+tableName+' con exito'
            elif deseaBorrar == "NO":
                print "No se borro la base de datos"
            else:
                print "Por favor, escriba si o no"
        else:
            print 'Esa tabla no existe'

    def showTables(self,):
        os.chdir("C:\\databases\\")
        #os.chdir("C:\\databases\\" +baseActual+ "\\metadataTabla.json")
        with open("C:\\databases\\"+baseActual+"\\metadataTabla.json", 'r') as file:
                data = json.load(file)
        print "Las tablas en "+baseActual+" son: "
        for i in range(len(data['tables'])):
            print data['tables'][i]['name']

    def setCurrentDatabase(self, nombreTabla):
        tablaActual = nombreTabla

    def alterTable(self, tableName):
        os.chdir("C:\\databases")
        #global tabName = tableName.getText()
        

    def alterRenameTo(self, newTableName):
        print "holiwe"
        print tablaActual
        print newTableName

        # os.chdir("C:\\databases\\"+baseActual)
        # if funciones.validarExistenciaTable(baseActual, tableName):

        #     print "Desea cambiar el nombre de la tabla " + tableName + " a " 
        #     deseaBorrar = raw_input("(si/no)\n")
        #     if deseaBorrar == "si":
        #         # Se cambia el archivo json de la tabla
        #         os.rename('Tabla'+tableName+'.json', 'Tabla'+newTableName+'.json')
        #         with open("C:\\databases\\"+baseActual+"\\metadataTabla.json", 'r') as file:
        #             data = json.load(file)
        #         # Se cambia el objeto tabla del archivo json
        #             n = 0
        #             while n < (len(data['tables'])):
        #                 #print data['bases'][n]['name']
        #                 if data['tables'][n]['name'] == tableName:
        #                #    del data['tables'][n]
        #                     data[newTableName] = data[tableName]
        #                     del data[tableName]
        #                 n = n+1
        #         with open("C:\\databases\\"+baseActual+"\\metadataTabla.json", 'w') as file:
        #             json.dump(data, file)
        #         print 'Se cambio el nombre de la tabla '+tableName+ 'a'+ newTableName +' con exito'
        #     elif deseaBorrar == "NO":
        #         print "No se cambio el nombre de la base de datos"
        #     else:
        #         print "Por favor, escriba si o no"
        # else:
        #     print 'Esa tabla no existe'

    def alterAddColumn(self, columnDef):
        os.chdir("C:\\databases")
        ###
        print columnDef

    def alterAddConstraint(self, tableConstraint):
        os.chdir("C:\\databases")
        print tableConstraint

    def alterDropColumn(self, columnName):
        os.chdir("C:\\databases")
        print columnName
        #

    def alterDropConstraint(self, constraintName):
        os.chdir("C:\\databases")
        print constraintName
