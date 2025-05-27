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
#                                           DESCRIPCIÓN DEL PROGRAMA                                           #
# ------------------------------------------------------------------------------------------------------------ #
"""
Este archivo inicializa el programa y llama a la ventana de login o carga. Además,
muestra las librerías y requerimientos necesarios para el funcionamiento del sistema.
"""

# ------------------------------------------------------------------------------------------------------------ #
#                                          IMPORTACIÓN DE LIBRERÍAS                                            #
# ------------------------------------------------------------------------------------------------------------ #
import forms.login.login_design as login_design  # Diseño de la ventana de login
import forms.main.loading as master              # Ventana de carga

# ------------------------------------------------------------------------------------------------------------ #
#                                            INICIALIZACIÓN DEL SISTEMA                                        #
# ------------------------------------------------------------------------------------------------------------ #
login_design.LoginDesigner()  # Llama a la ventana de login
#master.MasterPanel()        # Llama a la ventana de carga (descomentar para pruebas más eficientes)