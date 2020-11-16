# Función para convertir un caracter en un numero de la tabla ASCII
def CharacterToInt(character):
	return ord(character)

# Función para convertir un entero en un binario de 8 bits
def IntToBinary(integer):
	return bin(integer)[2:].zfill(8)

# Función para convertir un entero a carácter ASCII
def IntToCharacter(integer):
	return chr(integer)

# Cambiamos el ultimo bit de un byte
def ChangeLastBit(binaryText, bit):
	return binaryText[:-1]+bit

# Convertimos un string en binario a entero
def BinaryToInteger(binaryText):
	return int(binaryText, 2)

# 
def CompleteBinaryList(text):
	lista = []

	for letter in text:
		byte = IntToBinary(CharacterToInt(letter))
		for bit in byte:
			lista.append(bit)

	return lista

# Devuelve el color en número (0-255) con el bit cambiado
def ChangeColor(color, bit):
	return int(BinaryToInteger(ChangeLastBit(IntToBinary(color), bit)))

# Pasa bytes a texto
def BinaryToCharacter(binaryText):
	if(binaryText != ""):
		integer = BinaryToInteger(binaryText)
		return IntToCharacter(integer)
	else:
		return ""