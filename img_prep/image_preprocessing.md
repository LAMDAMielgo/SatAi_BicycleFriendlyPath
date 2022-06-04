## PREPROCESAMIENTO DE iMÁGENES

----

Una vez que tenemos las imágenes obtenidas de Google Street Maps API hemos aplicados las 
siguientes técnicas de preprocesamiento del dataset de imágenes:

* Filtrado de imágenes no válidas
* [Data augmentation](!https://en.wikipedia.org/wiki/Data_augmentation)
* Normalización de imágenes
* Transformación del [colorspace](!https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html) de las imágenes, para evaluar el comportamiento del modelo ante diferentes tipos de imágenes.

---

### FILTRADO DE IMÁGENES

Las llamadas a la API de GSM devuelven imágenes tanto tomadas por google como por usuarios.

Esto baja la calidad del dataset con el que entrenamos la clasificación, porque la segmentación sólo ha sido entrenada con imágenes diurnas y bajo la perspectiva o PoV de un coche / ciclista.

Por lo tanto, hemos tenido que hacer dos filtrados:

1. Sólo imágenes de google: se ha conseguido con los metadatos de la API, que almacenan el autor al que pertenece la captura de la imagen bajo el campo `copyright`.

2. Sólo imágenes diurnas: se ha realizado un análisis de la distribución de los diferentes canales de los colorspaces en RGB y LAB.

    > **¿Qué son los diferentes colorspaces de una imagen?**
    Son sistemas de interpretación del color, que permite organizar los colores de una imagen como modelos matemáticos abstractos, formados por tuplas o números.
    > 
    > En el caso de los archivos JPG, se trabaja en el espacio [RGB](!https://es.wikipedia.org/wiki/RGB) (Red-Green-Blue) usado en medios digitales, pues representa los colores como una muestra aditiva de colores de luz.
    >
    > Es espacio [LAB](!https://en.wikipedia.org/wiki/CIELAB_color_space) es empleado en extensiones TIFF y PDF, y se trata de un espacio tridimensional formado por los canales de:
    > * Luminosidad (de negro a blanco)
    > * A (de rojo a verde)
    > * B (de azul a amarillo) 

   
   Estos dos canales han resultado ser muy útiles para clasificar las imágenes por la distribución de:
   * Red Channel (RGB): Las imágenes nocturanas tienen una distribución muy diferente del rojo debido a la presencia de amarillos y naranjas muy intensos por la forma en que se captura la iluminación artificial.
   * Blue Channel (RGB): Debido a lo anterior, pasa justo lo contrario con los azules, que suelen estar menos presentes o casi ausentes en las fotografías de túneles.
   * Canal B (LAB): Este canal expresa lo anterior en otro espacio de color, pues representa la distrubición de colores de azul a amarillo.

   Curiosamente, el canal de brillo (lightness) no fue muy determinante, pues aunque las imágenes diurnas tienen colores en el centro de los valores mientras que las nocturnas muestras distribuciones muy asimétricas, si la imagen capta el foco de luz artificial, suelen ser imagenes con manchas blancas que distorsionan el brillo medio de las fotos y hace que sea más complicado establecer un valor para poder filtrarlas.


---

### DATA AUGMENTATION

Hemos aplicado esta técnica para incrementar la cantidad de datos disponibles y limitar el coste de las llamadas a la API de Google.Inicialmente tenemos **268 imágenes** que a través de esta técnica de Deep Learning hemos conseguido multiplicar por 5 hasta los 1608.

Debido a que necesitamos mantener la integridad del PoV de éstas, las transformaciones que hemos podido implementar son: 

* [Zoom](!https://keras.io/api/layers/preprocessing_layers/image_preprocessing/random_zoom/): Con esto hemos simulado que la salida de la API devuelve imágenes de todos los tamaños y necesitamos unificarlas.
* [Contrate](!https://keras.io/api/layers/preprocessing_layers/image_augmentation/random_contrast/): Una de las categorías que más le cuesta al modelo es diferenciar edificios del cielo cuando estos tienen colores similares. El aumento de contraste nos permite incrementar el pool de imágenes y ver cómo responde el modelo.
* [Flip (Simetría por eje)](!https://keras.io/api/layers/preprocessing_layers/image_augmentation/random_flip/): Hemos realizado una simetría horizontal (eje vertical) par obtener nuevas imágenes aparentando el punto de vista contrario.
* [Brillo](!https://keras.io/api/layers/preprocessing_layers/image_augmentation/random_brightness/): Esto incrementa el blanco en la imagen, y al igual que el contraste, nos permite ver qué tipo de imágenes son las que mejor segmenta el modelo.


Las imágenes sintéticas heredan de sus reales su clasificación y su geometría, de forma que podemos seguir clasificándolas y podríamos rellenar el resto de la información que hemos extraído.

---

### NORMALIZACIÓN DE LOS COLORES

Se ha realizado dos preprocesamientos de las imágenes:
1. Normalización de todas las imágenes: al estar guardadas como un array, se ha cogido el primer valor de cada tupla de colores y normalizado para todas las imágenes a la vez. Esto permite que se pierda pequeñas diferencias que pueda haber entre los rangos de colores debido a limitaciones o características de las cámaras con las que se obtuvieron.


2. [CLAHE](!https://en.wikipedia.org/wiki/Adaptive_histogram_equalization) imagen a imagen. 
Hemos aplicado esta técnica de ecualización adaptativa del histograma de valores para **mejorar el contraste**. Difiere de una ecualización habitual de histogramas en que en vez de actual sobre toda la imagen a la vez, este método computa diferentes histogramas a diferentes secciones de la imagen y los emplea para redistribuir el brillo. Es adecuado para mejorar el contraste local y aumentar la definición de los bordes entre figuras, lo cual pensamos que sería interesante hacer para ver cómo el modelo se comporta.

Este método tiene la limitación de sólo poder usarse sobre imágenes monocromáticas, o de un sólo canal, pues como se ha dicho, actúa sobre el brillo. En este caso, hemos cambiado las imágenes al espacio de color LAB y hemos aplicado CLAHE sobre el canal del brillo (blanco a negro) para despues volver al canal RGB.


---

### OUTPUT 

Tras este proceso, obtenemos arrays vinculados a través de su índice con la siguiente información:
* La clase de vía ciclista
* Si es real o sintética
* Su geometría, representada como string WKT
* Los diferentes arrays de imágenes que han surgido tras estre proceso:
    - Las imágenes originales
    - Las imágenes en RGB normalizadas
    - Las imágenes en Greyscale normalizadas

---

