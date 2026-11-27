# Custom Haar Cascade Classifier

This repository provides the tools, datasets, and instructions required to create your own custom Haar Cascade classifier using OpenCV.

It includes:

- **Positive images:** Samples containing the object of interest.
- **Negative images:** Background samples without the target object.
- **OpenCV tools:** Utilities required to generate samples and train the classifier.

### Scripts

| Script | Description |
|---|---|
| `1_capture.py` | Captures images of the object of interest. |
| `2_annotate.py` | Annotates positive images using bounding boxes. |
| `3_generateSamples.py` | Generates positive samples for training. |
| `4_train.py` | Trains the custom Haar Cascade classifier. |
| `5_detect.py` | Detects objects using the trained classifier. |

---

Este repositorio proporciona las herramientas, conjuntos de imágenes e instrucciones necesarias para crear tu propio clasificador Haar Cascade utilizando OpenCV.

Incluye:

- **Imágenes positivas:** Muestras que contienen el objeto de interés.
- **Imágenes negativas:** Muestras de fondos sin el objeto objetivo.
- **Herramientas OpenCV:** Utilidades necesarias para generar muestras y entrenar el clasificador.

### Scripts

| Script | Descripción |
|---|---|
| `1_capture.py` | Captura imágenes del objeto de interés. |
| `2_annotate.py` | Anota las imágenes positivas mediante cuadros delimitadores. |
| `3_generateSamples.py` | Genera muestras positivas para el entrenamiento. |
| `4_train.py` | Entrena el clasificador Haar Cascade personalizado. |
| `5_detect.py` | Detecta objetos utilizando el clasificador entrenado. |

---

**Requirements / Requisitos:** OpenCV 3.4.x