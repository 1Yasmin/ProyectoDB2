
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

def tipoValido(tipo):
    if tipo == "INT" or tipo == "CHAR" or tipo == "FLOAT" or tipo == "DATE":
        return True
    else:
        return False


def queTipo(tipo, valor):
    valid = None

    if tipo.upper() == "INT" and isinstance(valor, int) == True:
        return valor
    elif tipo.upper() == "FLOAT" and isinstance(valor, float) == True:
        return valor
    elif tipo.upper() == "CHAR" and isinstance(valor, str) == True:
        return valor
    elif tipo.upper() == "DATE" and validarFecha(valor) == True:
        return valor

    elif tipo.upper() == "INT" and isinstance(valor, int) == False:
        #print int(valor)
        return valor
    elif tipo.upper() == "FLOAT" and isinstance(valor, float) == False:
        return float(valor)
    elif tipo.upper() == "CHAR" and isinstance(valor, str) == False:
        return str(valor)
    elif tipo.upper() == "DATE" and validarFecha(valor) == False:
        valid = False
        return valid
    else:
        valid = False
        return valid


def validarFecha(valor):

    lista = valor.split("-")
    anio = lista[0]
    mes = lista[1]
    dia = lista[2]
   # print anio,mes,dia
    if len(anio) == 4 and len(mes) == 2 and len(dia) == 2:
        if int(mes) < 13 and int(dia) < 32:
            return True
        else:
            return False
    else:
        return False

          
def identificarCondicion(expr):
    if '>' in expr and '>=' not in expr and '<>' not in expr:
        signo = '>'
        lista = expr.split(signo)
        columnName = lista[0]
        cond = lista[1]
        return [columnName, signo, cond]
    elif '>=' in expr:
        signo = '>='
        lista = expr.split(signo)
        columnName = lista[0]
        cond = lista[1]
        return [columnName, signo, cond]
    elif '<' in expr and '<=' not in expr and '<>' not in expr:
        signo = '<'
        lista = expr.split(signo)
        columnName = lista[0]
        cond = lista[1]
        return [columnName, signo, cond]
    elif '<=' in expr:
        signo = '<='
        lista = expr.split(signo)
        columnName = lista[0]
        cond = lista[1]
        return [columnName, signo, cond]
    elif '<>' in expr:
        signo = '<>'
        lista = expr.split(signo)
        columnName = lista[0]
        cond = lista[1]
        return [columnName, signo, cond]
    elif '=' in expr and '>' not in expr and '<' not in expr:
        signo = '='
        lista = expr.split(signo)
        columnName = lista[0]
        cond = lista[1]
        return [columnName, signo, cond]
    else:
        return False
        
def condiciones(expr):
    cond =[]
    if 'AND' in expr:
        #pdb.set_trace()
        lista = expr.split('AND')
        for i in range(len(lista)):
            if 'OR' in expr:
                ex = lista[i].split('OR')
                for x in range(len(ex)):
                    a = identificarCondicion(ex[x])
                    if i%2 == False:
                        a.insert(3, 'OR')
                    cond.append(a)
            else:
                a = identificarCondicion(lista[i])
                if i%2 == False:
                    a.insert(3, 'AND')
                cond.append(a)
        return cond
    else:
        cond.append(identificarCondicion(expr))
        return cond
 

