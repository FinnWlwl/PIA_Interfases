# ============================================================================================================ #
# =                                       PIA - INTERFACES GRÁFICAS                                          = #
# =                                                                                                          = #
# =  Equipo 5                                                                                                = #
# =  Jesús Alberto Soto Juárez       Matrícula: 2020228     Carrera: IMTC                                    = #
# =  Laura Ivonne López Rodríguez    Matrícula: 2128053     Carrera: IMTC                                    = #
# =  Diego Andrés Martínez Chávez    Matrícula: 2026516     Carrera: IMTC                                    = #
# =  Miguel Gerardo Castillo Ruiz    Matrícula: 1928841     Carrera: IMTC                                    = #
# ============================================================================================================ #
# ------------------------------------------------------------------------------------------------------------ #
#                                           REQUERIMIENTOS DEL SISTEMA                                         #
# ------------------------------------------------------------------------------------------------------------ #
# pip install pillow
# pip install matplotlib
# pip install numpy
# pip install sqlalchemy
# pip install cryptography
# pip install pyserial
# pip install pandas openpyxl

# NOTA: Tkinter ya viene incluido por defecto en Python
# NOTA: Para los íconos se usa Font Awesome (solid), descargar la tipografía de https://fontawesome.com/download
# descomprimes el archivo y abres "otfs" e instalas: Font Awesome 6 Free-Solid-900.
# NOTA: Si se descarga de Github, se debe copiar y pegar la carpeta "Programa" fuera de la carpeta "PIA_Interfases",
# para que funcione correctamente el programa.

# ------------------------------------------------------------------------------------------------------------ #
#                                          DESCRIPCIÓN DE LOS ARCHIVOS                                         #
# ------------------------------------------------------------------------------------------------------------ #
# El programa se inicia desde el archivo de "main".
# "config" se usa para guardar todas las paletas de colores del diseño del programa.
# "build_db" crea la base de datos.
# En la carpeta "util" se encuentras scripts útiles para el programa.
# En la carpeta "pruebas" se encuentran varios archivos de medidas hechas que se pueden abrir en la interfaz.
# En la carpeta "persistence" se guardan los repositorios de las bases de datos.
# En la carpeta "images" se guardan imágenes que se usan en la interfaz.
# En la carpeta "forms" se guardan todos los paneles y ventanas de la interfaz.
  # Dentro de "forms" hay otras 3 carpetas, "login", "register" y "main", las primeras 2 son autoexplicativas,
  # en "main" se encuentran la pantalla de carga (loading) y "master", que contiene la mayor parte del código
  # de la interfaz, además se encuentra la carpeta "panels", que contiene las ventanas que se abren a partir
  # de "master".
# En la carpeta "db" se guarda la base de datos.
 

