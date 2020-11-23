from PIL import Image
import sys, os.path


# Función para codificar una imagen con un texto especificado
def Codificar(fileOpen, text, fileSave):
	image = Image.open(fileOpen)	# Abrimos la imagen

	mode = image.mode # Modo de imagen (RGB, RGBA, etc...)

	numChannels = 3 if (mode == "RGB") else 4 # Comprobamos el número de canales (red, green, blue, alpha)

	size = image.size # Tamaño de la imagen
	width = size[0]	  # Ancho
	height = size[1]  # Alto

	wholeImageBits = (width * height * numChannels) # Total de bits alterables

	print("Cantidad de caracteres cifrables: " + str(int(wholeImageBits/8) - 1)) # Cantidad de carácteres que puedo ingresar

	binaryList = CompleteBinaryList(text) # Lista del texto en binario

	finalString = ['1', '1', '1', '1', '1', '1', '1', '1'] # Carácter de finalización

	# Añadimos el carácter de finalización a la lista anteriormente creada
	for bit in finalString:
		binaryList.append(bit)

	listLength = len(binaryList) # Longitud de la lista

	contador = 0 # Inicializamos un contador para saber por cuál bit de la lista vamos

	exit = False # Para comprobar si hemos terminado de codificar para salir

	# Comprobamos si la cantidad de bits de nuestro texto es menor o igual que la cantidad de bits que se pueden escribir
	if(listLength <= wholeImageBits):
		# Bucle anidado
		for x in range(width):
			for y in range(height):
				# Comprobamos si hemos llegado al final de la lista
				if(contador < listLength):
					pixel = image.getpixel((x, y)) # Obtenemos el pixel en las coordenadas

					red = pixel[0]
					green = pixel[1]
					blue = pixel[2]
					if(numChannels == 4):
						alpha = pixel[3]

					red = ChangeColor(red, binaryList[contador]) # Cambiamos el ultimo bit de red al deseado
					contador += 1

					# Con cada color se vuelve a comprobar se se ha llenado y si es así se actualizan los colores
					if(contador < listLength):
						green = ChangeColor(green, binaryList[contador])
						contador += 1

						if(contador < listLength):
							blue = ChangeColor(blue, binaryList[contador])
							contador += 1

							if(numChannels == 4):
								if(contador < listLength):
									alpha = ChangeColor(alpha, binaryList[contador])
									contador += 1
					
					# Se asignan los colores en la imagen, comprobando antes sin son RGB o RGBA
					if(numChannels == 4):
						image.putpixel((x, y), (red, green, blue, alpha))
					else:
						image.putpixel((x, y), (red, green, blue))

				# Si se ha llegado al final de la lista salimos del bucle anidado
				else:
					exit = True
					break

			if(exit):
				break

		print("Guardando...")
		image.save(fileSave) # Guardamos la imagen
		print("Imagen codificada correctamente.")
		image.close()

	# Si queremos escribir más texto del que nos permite la imagen, nos avisará
	else:
		print("Mucho texto")



# Función para decodificar una imagen codificada
def Decodificar(fileOpen, textSave):
	image = Image.open(fileOpen) # Abrimos la imagen

	mode = image.mode # Modo de imagen (RGB, RGBA, etc...)

	numChannels = 3 if (mode == "RGB") else 4 # Comprobamos el número de canales (red, green, blue, alpha)

	size = image.size # Tamaño de la imagen
	width = size[0]	  # Ancho
	height = size[1]  # Alto

	exit = False # Para comprobar si hemos terminado de codificar para salir

	text = "" # Texto final

	byteString = "" # Se utiliza para comprobar por bytes si es igual al finalString

	finalString = "11111111" # Byte de finalización para comprobar que se ha extraido todo el texto

	for x in range(width):
		for y in range(height):
			# Se comprueba si byteString tiene 8 carácteres
			if(len(byteString) % 8 == 0):
				# Se comprueba si el byte que estamos examinando es igual que el de finalización
				if(byteString == finalString):
					exit = True
					break
				text += BinaryToCharacter(byteString) # Añadimos al texto final la cadena analizada
				byteString = "" # Vaciamos el string para seguir añadiendo más bytes

			pixel = image.getpixel((x, y)) # Obtenemos los valores del pixel en las coordenadas

			red = pixel[0]
			green = pixel[1]
			blue = pixel[2]
			if(numChannels == 4):
				alpha = pixel[3]

			byteString += IntToBinary(red)[-1:] # Le añadimos el último bit a la cadena para analizar

			if(len(byteString) % 8 == 0):
				if(byteString == finalString):
					exit = True
					break
				text += BinaryToCharacter(byteString)
				byteString = ""
			byteString += IntToBinary(green)[-1:]

			if(len(byteString) % 8 == 0):
				if(byteString == finalString):
					exit = True
					break
				text += BinaryToCharacter(byteString)
				byteString = ""
			byteString += IntToBinary(blue)[-1:]

			if(numChannels == 4):
				if(len(byteString) % 8 == 0):
					if(byteString == finalString):
						exit = True
						break
					text += BinaryToCharacter(byteString)
					byteString = ""
				byteString += IntToBinary(alpha)[-1:]
		if(exit):
			break

	if(textSave != None):
		file = open(textSave, "w")
		file.write(text)
		file.close()
	else:
		print("El texto decodificado es: \"" + text + "\"")




# --------------------- FUNCIONES USADAS -------------------------

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

# Convierte un texto en una lista transformada en bits
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

def Help():
	print("\n"
"Usage:\n"
"\n"
"-c)     Para codificar texto en una imagen.\n"
"\n"
"\tUsage: Stenography.py -c ImageInput {-f TextInput | Text} [ImageOutput]\n"
"\n"
"\tImageInput: Ruta de imagen a codificar.\n"
"\tTextInput: Ruta de archivo de texto.\n"
"\tText: Texto para codificar. Si lleva espacios usen comillas.\n"
"\tImageOutput: Si se añade una ruta distinta a ImageInput no se sobreescribe.\n"
"\n"
"\n"
"-d)     Para decodificar el texto de una imagen codificada anteriormente.\n"
"\n"
"\tUsage: Stenography.py -d EncodedImageInput [TextOutput]\n"
"\n"
"\tEncodedImageInput: Ruta de imagen ya codificada anteriormente.\n"
"\tTextOutput: Ruta para guardar el texto decodificado. Si no se añade, se muestra por pantalla.")

# INICIO DEL PROGRAMA
argumentos = sys.argv # Recoge los argumentos que le pasamos por la consola
error = False # Para comprobar si ha fallado algo y no ejecutar nada

if(len(argumentos) > 2):
	if(argumentos[1].lower() == '-c'):
		if(os.path.isfile(argumentos[2])):
			fileOpen = argumentos[2]
			if(len(argumentos) >= 4):
				if(argumentos[3].lower() == '-f'):
					if(len(argumentos) >= 5):
						if(os.path.isfile(argumentos[4])):
							fileText = open(argumentos[4])
							text = fileText.read()							
							if(len(argumentos) >= 6):
								fileSave = argumentos[5]
							else:
								fileSave = fileOpen
						else:
							error = True
							print("Dirección de archivo de texto inaccesible.")
							Help()
					else:
						error = True
						print("Archivo de texto no indicado.")
						Help()
				else:
					text = argumentos[3]
					if(len(argumentos) >= 5):
						fileSave = argumentos[4]
					else:
						fileSave = fileOpen
			else:
				error = True
				print("Texto no indicado.")
				Help()
		else:
			error = True
			print("Imagen para abrir innacesible.")
			Help()
		if(not error):
			Codificar(fileOpen, text, fileSave)

	elif(argumentos[1].lower() == '-d'):
		if(os.path.isfile(argumentos[2])):
			fileOpen = argumentos[2]
			if(len(argumentos) >= 4):
				textSave = argumentos[3]
			else:
				textSave = None
		else:
			error = True
			print("Imagen para abrir innacesible.")
			Help()
		if(not error):
			Decodificar(fileOpen, textSave)

	else:
		error = True
		print("Argumentos inválidos.")
		Help()

else:
	error = True
	print("Pocos argumentos.")
	Help()