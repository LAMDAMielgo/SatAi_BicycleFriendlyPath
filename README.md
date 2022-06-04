# SatAi_BicycleFriendlyPath
repository for saturdays.ai project about evaluation of bicycle-friendly paths in Madrid

---
### NOTES (w3)

Etapas de desarrollo del proyecto:

1. Tratamiento de datos (IMGS):

* Generación de DATASET:
    - Extraer más imagnes:
    - DATA AUGMENTATION: generación de imagenes a partir de subsets

* Armonización de imaǵenes:
    * (a) Sin ningún tipo de tratamiento:
        
        - Comprobar shape de las imágenes: FOVinicial == FOVfinal (F of View)
        - Histograma de contrast: Ecualización con CLAHE

    * (b) Imágenes en BW:
        
        Una vez que tenemos las imágenes en numpy array, triplicamos la tercera dimensión (1,1,3) con CLAHE


2. MODELO:

    - 2.1. Clasificación con modelos de Machine Learning:
        
        Inicialmente, se intentó aplicar Pycaret, para tener una idea sobre qué modelos predecía mejor si una imagen era ciclable o no. Dado que no se obtenían                 resultados para más de una feature, se optó por aplicar los siguientes modelos de clasificación:
        
        
            - Random Forest: es un algoritmo de aprendizaje automático supervisado basado en un conjunto de árboles de decisión.
            - LDA (Lineal Discriminant Analysis): es un método de clasificación supervisado de variables cualitativas en el que dos o más grupos son conocidos a priori
              y nuevas observaciones se clasifican en uno de ellos en función de sus características.
            - KNN: es un algoritmo de aprendizaje supervisado, es decir, que a partir de un juego de datos inicial su objetivo será el de clasificar correctamente                   todas las instancias nuevas
            - QDA (Quadratic Discriminant Analysis): es un método de clasificación supervisado que se encuentra en un punto medio entre el método no paramétrico KNN y               los métodos lineales LDA y regresión logística.
            - DBSCAN: es un algoritmo de clúster o agrupamiento, no supervisado, basado en la densidad que puede ser utilizado para identificar clústeres de cualquier               forma en un conjunto de datos que contiene ruido y valores atípicos.


        Para poder ver qué tipo de modelo de clasificación se ajusta mejor a nuestro problema, se ha analizado el score y f1-score de cada uno de los modelos.
    Con pycaret, ML y RNN, de forma que podamos comparar y hacer visualización.

        - 2.1.1 BINARIA: Empezamos con dos labels y si da tiempo
        
        - 2.1.2. MULTICLASIFICACIÓN
    
    Necesitamos hacer:
    * CUantificación de % pixel / total img (VALOR DE LA SEGMENTACIÓN CUANTIFICADO)

    - 2.2 FEATURE EXTRACTION: 
    A partir de las máscaras obtenidas, convertimos la información de la segmentación en vectores caracterizadores.
        * Sin feature selection
        * COn feature selection (UMBRAL)

    2.3 SEGMENTACION -> Filtrado -> Eliminamos personas de lasi imgs

3. RESULTADOS

HACER VISUALIZACIONSE
    
---

## ESTRUCTURA DEL PROYECTO


```
<nombre del proyecto> 
|
| geodata/
|    | #todo
|    | #todo 


```
