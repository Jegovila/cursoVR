# OpenCV 3.4.10 – Required Files / Archivos Necesarios

The executables `opencv_createsamples.exe` and `opencv_traincascade.exe` are no longer included in OpenCV versions 4.0 and later. Therefore, **OpenCV 3.4.10** is required to use these tools.

The following files are provided in this folder:
- `opencv_createsamples.exe`
- `opencv_traincascade.exe`

However, the required DLL (`opencv_world3410.dll`) is not included because of GitHub's file upload size restrictions.

**Download and install the missing DLL:**

1. Download OpenCV 3.4.10 from the following link:

   [Download OpenCV 3.4.10 (SourceForge)](https://sourceforge.net/projects/opencvlibrary/files/3.4.10/opencv-3.4.10-vc14_vc15.exe/download)

2. Run the downloaded executable to extract the OpenCV files. You can choose any extraction directory.

3. Locate the following file inside the extracted folder:

   `opencv\build\x64\vc15\bin\opencv_world3410.dll`

4. Copy `opencv_world3410.dll` into this folder, alongside the two `.exe` files.

The tools should now be ready to use.

---


Los ejecutables `opencv_createsamples.exe` y `opencv_traincascade.exe` dejaron de incluirse en las versiones 4.0 y posteriores de OpenCV. Por lo tanto, es necesario utilizar **OpenCV 3.4.10** para trabajar con estas herramientas.

Los siguientes archivos se incluyen en esta carpeta:
- `opencv_createsamples.exe`
- `opencv_traincascade.exe`

Sin embargo, la DLL requerida (`opencv_world3410.dll`) no está incluida debido a las restricciones de tamaño de archivos de GitHub.

**Descarga e instalación de la DLL faltante:**

1. Descarga OpenCV 3.4.10 desde el siguiente enlace:

   [Descargar OpenCV 3.4.10 (SourceForge)](https://sourceforge.net/projects/opencvlibrary/files/3.4.10/opencv-3.4.10-vc14_vc15.exe/download)

2. Ejecuta el archivo descargado para extraer los archivos de OpenCV. Puedes elegir cualquier directorio de destino.

3. Localiza el siguiente archivo dentro de la carpeta extraída:

   `opencv\build\x64\vc15\bin\opencv_world3410.dll`

4. Copia `opencv_world3410.dll` en esta carpeta, junto a los dos archivos `.exe`.

¡Las herramientas estarán listas para utilizarse!