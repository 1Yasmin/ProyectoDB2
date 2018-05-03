


def queTipo (tipo, valor):
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
        return int(valor)
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

