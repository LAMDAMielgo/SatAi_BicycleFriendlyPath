## CAPTURA Y LIMPIEZA DE DATOS GEOESPACIALES
-----
### ABOUT

En esta carpeta está el código producido para la limpieza de los datos que fueron el punto de partida del proyecto.

Parte de los datos fueron mergeados entre ellos con qGIS; para obtener el conjunto de datos con el que se obtuvo los puntos se hizo:

* Un primer set de datos _rápido_ fue hecho obteniendo los puntos de control de las líneas de los ejes (geometría del geopackage)
* Un segundo set de datos más homogéneamente producido, fue hecho mediante los siguientes pasos en qGIS:    
    * Densificar los ejes de puntos de control (dado un angulo)
    * Obtener los puntos de control de los ejes
    * Simplificar para quitar duplicados y puntos demasiados juntos en rotondas y cruces.

El segundo método es consigue un reparto más uniforme de los puntos sobre el viario; pero dado la cantidad de puntos puede ser dificil de hacer.

-----

### FUENTES DE DATOS

Aquí se limpian los datos del Banco de datos de Madrid (BDM) y, los ejes de viario del IGN y el los geopackage obtenidos del archivo KML de enbicipormadrid.org

Según cada archivo:

* cleaning_viario_polygons: aquí se limpian:
    * viario de polígonos del BDM
    * ejes de viario del IGN
    * infraestructura ciclista
    
    También se hace el pegado de todos los elementos y se hace un check de duplicados.

* cleaning_viario_ciclista: aqui se limpia los archivos gpkg resultantes del KML anteriormente mencionado. Cada archivo contiene una única multigeometría, que al pegar espacialmente con el resultado anterior da lugar a la feature 'cyclist_type' que se usa a lo largo del proyecto. Se
usa esta clasificación en vez de la de la BDM porque contiene más casos y es más extensa.

* cleaning_bicicleaccdnts: limpiado e intento de pegado de la capa de accidentes ciclistas de Madrid;
el código aquí está modulado y en vez de tirar de un archivo descargado en local, apunta directamente a la URL de descarga, guardando el constructor y pasándole unos argumentos según el indicador a descargar. 

    Este dataset tenía bastantes complicaciones:
    * Antes de 2021 no hay puntos geográficos en los que localizar los accdientes; sólo había direcciones. Se hizo un intento de pegado por callejero pero las cadenas de texto entre el dataset que se tiene y el dataset varían en la forma que en formatean los nombres de los textos; y sólo se pegaba un porcentaje un pequeño.

    * También hay un cambio en la clasificación de los accidentes: a partir de 2021 la clasificación está simplificada.

    El proceso hace una simplificación para obtener un dataset en el que dado un lugar (punto o direccion) en un distrito, hay un accidente (tipo_accidente) en una franja horaria (hour_range).

    Hay unas 8k filas, de las cuales 2k tienen geometría; se consiguió pegar por nombre otras 2k pero viendo el head() final de la comparación, era bastante dudoso. Se hizo por distancia de Levenstein, que compara la similaridad entre cadenas de carácteres.


---
REQUIREMENTS

Para poder usar el codigo se necesita: geopandas, numpy, pandas, requests, seaborn y StringIO.

Tira de una carpeta en local para los datos en ```../data.```

-----


