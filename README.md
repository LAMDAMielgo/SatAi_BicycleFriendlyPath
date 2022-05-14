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

    - 2.1. Clasificación:

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