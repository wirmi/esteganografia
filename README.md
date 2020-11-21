Es necesaria la librería PIL:

		pip install pillow

Ayuda del programa:

		-c)     Para codificar texto en una imagen.

			Usage: Stenography.py -c ImageInput {-f TextInput | Text} [ImageOutput]

			ImageInput: Ruta de imagen a codificar.
			TextInput: Ruta de archivo de texto.
			Text: Texto para codificar. Si lleva espacios usen comillas.
			ImageOutput: Si se añade una ruta distinta a ImageInput no se sobreescribe.


		-d)     Para decodificar el texto de una imagen codificada anteriormente.

			Usage: Stenography.py -d EncodedImageInput [TextOutput]

			EncodedImageInput: Ruta de imagen ya codificada anteriormente.
			TextOutput: Ruta para guardar el texto decodificado. Si no se añade, se muestra por pantalla.
