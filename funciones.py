
import json
import os
import os.path
import pdb


def validarExistencia(path, name):
    list = os.listdir(path)
    valid = False 
    for elemento in list:
        if elemento == name:
            valid = True
    return valid
    
def validarExistenciaTable(baseActual, tableName):
    valid = False
    with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'r') as file:
        data = json.load(file)
    for i in range(len(data['tables'])):
        if (data['tables'][i]['name'] == tableName):
            valid = True
    return valid

def tipoConstraint(const):
    if const.K_PRIMARY() != None:
        return 'PRIMARY'
    elif const.K_UNIQUE() != None:
        return 'UNIQUE'
    elif const.K_FOREIGN() != None:
        return 'FOREIGN'
    elif const.K_CHECK() != None:
        return 'CHECK'
    
    
def validarValor(value):
    if value is None:
        return ''
    else:
        return value.getText()
        
def columnName(arr):
    arrCol = []
    if arr.column_name() != []:
        arrC = 0
        for c in arr.column_name():
            arrCol.append(validarValor(arr.column_name()[arrC]))
            arrC = arrC +1
    return arrCol










        