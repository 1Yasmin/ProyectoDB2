# -*- coding: utf-8 -*-

import json
import os
import os.path
import funciones
import shutil
import pdb
import sys

class databaseManager:

    baseActual = None
    tablaActual = None

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
            print 'Estas usando la base de datos ' + db
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
                            if funciones.validarValor(const[a].expr()) != None:
                                nombre['constraints'].append(
                                {'type': 'CHECK', 
                                'name': funciones.validarValor(const[a].name()),
                                'column_name': funciones.columnName(const[a]),
                                'expr': funciones.condiciones(const[a].expr().getText())
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
            print "Borrar base de datos " + database_name
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
                with open("C:\\databases\\"+baseActual+'\Tabla'+tableName+'.json', 'r') as file:
                    tableData = json.load(file)
                #pdb.set_trace()
                tableColumName = []
                fila = []
                #Verificar que no ingrese mas valores que la cantidad de columnas
                if len(expr) <= len(tableData['columnas']) and len(columnName) <=len(tableData['columnas']):
                    
                    for i in range(len(tableData['columnas'])):
                        tableColumName.append(tableData['columnas'][i]['name'])
                        fila.append({tableData['columnas'][i]['name']: None})
                        
                    #verificar que la columna exista
                    for i in range(len(columnName)):
                        if columnName[i].getText() in tableColumName:
                            for a in range(len(tableData['columnas'])):
                                if tableData['columnas'][a]['name'] == columnName[i].getText():
                                    #Verifica tipo de dato y columna
                                    if tableData['columnas'][a]['type'] != 'INT':
                                        exptemp = funciones.queTipo(tableData['columnas'][a]['type'],expr[i].getText())
                                        print exptemp
                                        if exptemp != False:
                                            expr[i] = exptemp
                                            print "Se ha insertado el dato: "
                                            print expr[i]
                                            print "en la columna "+ columnName[i].getText()+" de la tabla "+tableName
                                        else:
                                            print "El tipo de dato por el que desea cambiar no corresponde"
                                            sys.exit()
                                    else:
                                        pass
                        else:
                            print "El nombre de la columna no esta definido"
                            sys.exit()
                else:
                    print 'El numero de valores no concuerda con el numero de columnas'
                    sys.exit()              
                                
                #Insertar los datos
                for i in range(len(columnName)):
                    for a in range(len(fila)):
                        if fila[a].keys()[0] == columnName[i].getText():
                            new = {fila[a].keys()[0]:expr[i]}
                            fila[a] = new 
                     
                tableData['registros'].append(fila)
                with open("C:\\databases\\"+baseActual+'\Tabla'+tableName+'.json', 'w') as file:
                    json.dump(tableData, file)
            
            else:
                print "La tabla no existe en la base de datos "+baseActual
               
                       
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

    def setCurrentTable(self, nombreTabla):
        global tablaActual
        tablaActual = nombreTabla

    def alterTable(self, tableName):
        os.chdir("C:\\databases")
        #global tabName = tableName.getText()

    ## Corregir numero de registros
    def alterRenameTo(self, newTableName): 
        

        tableName = tablaActual
        os.chdir("C:\\databases\\"+baseActual)
        if funciones.validarExistenciaTable(baseActual, tableName):

            print "Desea cambiar el nombre de la tabla " + tableName + " a " + newTableName
            deseaBorrar = raw_input("(si/no)\n")
            if deseaBorrar == "si":  
                print "cp"
                with open("C:\\databases\\"+baseActual+"\\metadataTabla.json", 'r') as file:
                    data = json.load(file)
                # Se cambia el objeto tabla del archivo json
                    print "aqui "
                    for i in range(len(data['tables'])):
                        if data['tables'][i]['name'] == tableName:
                            print data['tables'][i]['name']
                            del data['tables']
                        #     data[newTableName] = data[tableName]
                        #     del data[tableName]
                # Se cambia el archivo json de la tabla
                os.rename('Tabla'+tableName+'.json', 'Tabla'+newTableName+'.json')
                        
                with open("C:\\databases\\"+baseActual+"\\metadataTabla.json", 'w') as file:
                    json.dump(data, file)
                print 'Se cambio el nombre de la tabla ' + tableName + ' a ' + newTableName + ' con exito'
            elif deseaBorrar == "NO":
                print "No se cambio el nombre de la base de datos"
            else:
                print "Por favor, escriba si o no"
        else:
            print 'Esa tabla no existe'

    def alterAddColumn(self, columnDef):
        os.chdir("C:\\databases")
         #nombre['columnas'].append({'name': i.column_name().getText(), 'type': i.type_name().getText()})
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

    def updateTable(self, tableName, columnName, expr):
        if baseActual != None:
            #Verificar que la tabla exista
            exist = False
            with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'r') as file:
                data = json.load(file)
            for i in range(len(data['tables'])):
                if data['tables'][i]['name'] == tableName:
                    exist = True
            if exist:
                with open("C:\\databases\\"+baseActual+'\Tabla'+tableName+'.json', 'r') as file:
                        tableData = json.load(file)
                tableColumName = []
         
                #Verificar que no ingrese mas valores que la cantidad de columnas
                if len(expr) < 3 and len(columnName) < 2:
                    
                    for i in range(len(tableData['columnas'])):
                        tableColumName.append(tableData['columnas'][i]['name'])
      
                    #verificar que la columna exista
                    for i in range(len(columnName)):
                        if columnName[i].getText() in tableColumName:
                            for a in range(len(tableData['columnas'])):
                                if tableData['columnas'][a]['name'] == columnName[i].getText():
                                    pass
                                    #Verifica tipo de dato y columna
                                    # if funciones.queTipo(expr[1].getText(), tableData['columnas'][a]['type']):
                                        # pass
                                    # else:
                                        # print "El tipo de dato no corresponde"
                                        # sys.exit()
                                
                        else:
                            print "El nombre de la columna no esta definido"
                            sys.exit()
                else:
                    print 'El numero de valores no concuerda con el numero de columnas'
                    sys.exit()              
                
               
                #Actualizar datos
                for i in range(len(tableData['registros'])):
                    for f in range(len(tableData['registros'][i])):
                        if tableData['registros'][i][f].keys()[0] == columnName[0].getText():
                           # pdb.set_trace()
                            if tableData['registros'][i][f][columnName[0].getText()] == expr[1].getText()[(len(columnName[0].getText())+1):]:
                                tableData['registros'][i][f][columnName[0].getText()] = expr[0].getText()
                with open("C:\\databases\\"+baseActual+'\Tabla'+tableName+'.json', 'w') as file:
                    json.dump(tableData, file)
            
            else:
                print "La tabla no existe en la base de datos "+baseActual
        
        else:
            print "Seleccione la base de datos a utilizar \nUSE DATABASE nombre"
           
    def delete(self, tableName, condicion):
        if baseActual == None:
            print "Seleccione la base de datos a utilizar \nUSE DATABASE nombre"
            return

        # Verificar que la tabla exista
        exist = False

        with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'r') as file:
            data = json.load(file)

        for i in range(len(data['tables'])):
            if data['tables'][i]['name'] == tableName:
                exist = True

        if not exist:
            print "Seleccione la base de datos a utilizar \nUSE DATABASE nombre"
            return

        # Las condiciones se cumplen. Yey.
        with open("C:\\databases\\"+baseActual+'\Tabla'+tableName+'.json', 'r') as file:
            tableData = json.load(file)

        tableColumName = []

        for i in range(len(tableData['columnas'])):
            tableColumName.append(tableData['columnas'][i]['name'])

        #Borrar todas las filas si no hay condicion
        if condicion is None:
            delFilas = len(tableData['registros'])
            tableData['registros'] = []
            with open("C:\\databases\\"+baseActual+'\Tabla'+tableName+'.json', 'w') as file:
                json.dump(tableData, file)

            print 'Se eliminaron '+ str(delFilas)+' filas de la tabla '+tableName+' con exito'

        # Borra solo las filas que cumplan con la condicion
        else:
            condicion = condicion.getText()
            # Guardar el codicional

            # TODO: Temporalmente solo soportamos la condicion simple de igualdad
            lista = condicion.split("=")
            columnName = lista[0]
            cond = lista[1]

            # Verificar que la columna exista
            #pdb.set_trace()
            if not columnName in tableColumName:
                print "El nombre de la columna no esta definido"
                sys.exit()

            # Borrar datos
            delFilas = 0
            #posicionesAEliminar = []
            # paso = False

            # Iterar sobre las filas
            # print "Len: ", len(tableData['registros'])
            #   print "Pos 3: ", tableData['registros'][3]

            for i in xrange(len(tableData['registros']-1,-1,-1)): # PROBAR ESTO
                print "Actualmenbte la longitud de table data es: ", len(tableData['registros'])

                # Iterando las columnas
                for f in range(len(tableData['registros'][i])):
                    if tableData['registros'][i][f].keys()[0] == columnName:

                        #pdb.set_trace()
                        if str(tableData['registros'][i][f][columnName]) == cond:
                            print 'eliminar'
                            #pdb.set_trace()

                            # En lugar de eliminar eliminar, vamos a construir un array
                            # de las posiciones que deben ser eliminadas, de forma que luego
                            # hagamos la eliminacion atómicamente
                            # del tableData['registros'][i]
                            #posicionesAEliminar.append(i)
                            #paso = True

                            delFilas = delFilas +1

                            #tableData['registros'][i][f][columnName] = expr[0].getText()

            # Para evitar el problema de que eliminar una tupla 'corra' las demàs tuplas y por tanto
            # los offsets identificados para eliminación se vuelvan incorrectos, vamos a eliminar
            # las tuplas en sentido contrario, de forma que primer se elimine 3 y luego 1. Esto porque
            # eliminar la posición 3 no modifica la posición de 1.
            


                # TODO: Hacer hacer la eliminación
                # with open("C:\\databases\\"+baseActual+'\Tabla'+tableName+'.json', 'w') as file:
                    # json.dump(tableData, file)

    def selectCore(self, resultColumn, expr, tableOrSubquery,joinClause):
        os.chdir("C:\\databases\\")
        with open("C:\\databases\\"+baseActual+"\\Tabla"+tableName+".json", 'r') as file:
                data=json.load(file)
    
        #print "Las colunmas en "+tableName+" son: "
       # for i in range(len(data['columns'])):
            #print data['columns'][i]['name']
