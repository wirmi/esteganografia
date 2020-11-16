from PIL import Image
import Conversiones as PasarTexto

text = "Lorem ipsum dolor sit amet, consectetur adipiscii" # Texto a codificar

nameOpen = "Images/Pixeles.png" # Nombre de la imagen
nameSave = "Pixeles.png"		# Nombre para guardar la imagen
image = Image.open(nameOpen)	# Abrimos la imagen

mode = image.mode # Modo de imagen (RGB, RGBA, etc...)

numChannels = 3 if (mode == "RGB") else 4 # Comprobamos el número de canales (red, green, blue, alpha)

size = image.size # Tamaño de la imagen
width = size[0]	  # Ancho
height = size[1]  # Alto

wholeImageBits = (width * height * numChannels) # Total de bits alterables

print("Cantidad de caracteres cifrables: " + str(int(wholeImageBits/8) - 1)) # Cantidad de carácteres que puedo ingresar

binaryList = PasarTexto.CompleteBinaryList(text) # Lista del texto en binario

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

				red = PasarTexto.ChangeColor(red, binaryList[contador]) # Cambiamos el ultimo bit de red al deseado
				contador += 1

				# Con cada color se vuelve a comprobar se se ha llenado y si es así se actualizan los colores
				if(contador < listLength):
					green = PasarTexto.ChangeColor(green, binaryList[contador])
					contador += 1

					if(contador < listLength):
						blue = PasarTexto.ChangeColor(blue, binaryList[contador])
						contador += 1

						if(numChannels == 4):
							if(contador < listLength):
								alpha = PasarTexto.ChangeColor(alpha, binaryList[contador])
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
	image.save(nameSave) # Guardamos la imagen
	print("Imagen codificada correctamente.")

# Si queremos escribir más texto del que nos permite la imagen, nos avisará
else:
	print("Mucho texto")