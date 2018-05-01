
import json
import os
import os.path


def validarExistencia(path, name):
    list = os.listdir(path)
    valid = False 
    for elemento in list:
        if elemento == name:
            valid = True
    print valid
    return valid
    
def validarExistenciaTable(baseActual, tableName):
    valid = False
    with open("c:\\databases\\"+baseActual+'\metadataTabla.json', 'r') as file:
        data = json.load(file)
    for i in range(len(data['tables'])):
        if (data['tables'][i]['name'] == tableName):
            valid = False
        else:
            valid = True
    return valid
        