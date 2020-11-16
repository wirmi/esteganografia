from PIL import Image
import Conversiones as PasarTexto

nameOpen = "Pixeles.png" # Nombre de la imagen
image = Image.open(nameOpen) # Abrimos la imagen

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
			text += PasarTexto.BinaryToCharacter(byteString) # Añadimos al texto final la cadena analizada
			byteString = "" # Vaciamos el string para seguir añadiendo más bytes

		pixel = image.getpixel((x, y)) # Obtenemos los valores del pixel en las coordenadas

		red = pixel[0]
		green = pixel[1]
		blue = pixel[2]
		if(numChannels == 4):
			alpha = pixel[3]

		byteString += PasarTexto.IntToBinary(red)[-1:] # Le añadimos el último bit a la cadena para analizar

		if(len(byteString) % 8 == 0):
			if(byteString == finalString):
				exit = True
				break
			text += PasarTexto.BinaryToCharacter(byteString)
			byteString = ""
		byteString += PasarTexto.IntToBinary(green)[-1:]

		if(len(byteString) % 8 == 0):
			if(byteString == finalString):
				exit = True
				break
			text += PasarTexto.BinaryToCharacter(byteString)
			byteString = ""
		byteString += PasarTexto.IntToBinary(blue)[-1:]

		if(numChannels == 4):
			if(len(byteString) % 8 == 0):
				if(byteString == finalString):
					exit = True
					break
				text += PasarTexto.BinaryToCharacter(byteString)
				byteString = ""
			byteString += PasarTexto.IntToBinary(alpha)[-1:]
	if(exit):
		break

print("El texto decodificado es: \"" + text + "\"")

