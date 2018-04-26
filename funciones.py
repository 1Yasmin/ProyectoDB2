
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