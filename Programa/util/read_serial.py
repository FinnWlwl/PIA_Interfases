#============================================================================================================#
#                                         LECTURA DEL PUERTO SERIAL                                          #
#============================================================================================================#
"""
Descripción:
Este módulo se encarga de leer datos desde un puerto serial utilizando la librería pyserial, también permite
detectar si el Arduino se encuentra conectado, hasta que este se conecte, sin embargo, si se
conecta y desconecta el Arduino es incapaz de reconectar la lectura sin reiniciar el programa.
"""

#============================================================================================================#
#                                      IMPORTACIÓN DE LIBRERÍAS                                              #
#============================================================================================================#
import serial
import time

#============================================================================================================#
#                                           INICIO DEL SCRIPT                                                #
#============================================================================================================#
'''
MOTOR_PORT  = 'COM9'
SENSOR_PORT = 'COM4'
BAUDRATE    = 9600
STEP_MM     = 0.5
TOTAL_MM    = 160
N_STEPS     = int(TOTAL_MM / STEP_MM) + 1
OFFSET      = 34

class ReadSerial:
    def __init__(self):
        self.motor_ser = serial.Serial(MOTOR_PORT, BAUDRATE, timeout=1)
        self.sensor_ser = serial.Serial(SENSOR_PORT, BAUDRATE, timeout=1)
        time.sleep(2)
        self.cancelar_escaneo_externo = False

    def motor_home(self):
        self.motor_ser.reset_input_buffer()
        self.motor_ser.write(b'HOME\n')
        start = time.time()
        while True:
            line = self.motor_ser.readline().decode().strip()
            if line == "OK HOME":
                return
            if "ERROR" in line or "EMERGENCY" in line:
                raise RuntimeError(f"Error en HOME: {line}")
            if time.time() - start > 37:
                raise TimeoutError("motor_home: Timeout")
            time.sleep(0.1)

    def motor_move(self, x_mm):
        self.motor_ser.reset_input_buffer()
        cmd = f"MOVE {x_mm:.2f}\n".encode()
        self.motor_ser.write(cmd)
        start = time.time()
        while True:
            line = self.motor_ser.readline().decode().strip()
            if line.startswith("OK POS"):
                return
            if "ERROR" in line or "EMERGENCY" in line:
                raise RuntimeError(f"Error en MOVE: {line}")
            if time.time() - start > 40:
                raise TimeoutError("motor_move: Timeout")
            time.sleep(0.1)

    def sensor_read(self):
        self.sensor_ser.reset_input_buffer()
        self.sensor_ser.write(b'MEASURE\n')
        start = time.time()
        while True:
            line = self.sensor_ser.readline().decode().strip()
            if line.startswith("DIST"):
                try:
                    return int(line.split()[1])
                except:
                    raise RuntimeError(f"Formato DIST incorrecto: {line}")
            if time.time() - start > 5:
                raise TimeoutError("sensor_read: Timeout")
            time.sleep(0.1)
'''
#============================================================================================================#
MOTOR_PORT = 'COM9'
SENSOR_PORT = 'COM4'
BAUDRATE = 9600
STEP_MM = 0.5
TOTAL_MM = 160
N_STEPS = int(TOTAL_MM / STEP_MM) + 1
OFFSET = 34


class ReadSerial:
    def __init__(self):
        self.motor_ser = serial.Serial(MOTOR_PORT, BAUDRATE, timeout=1)
        self.sensor_ser = serial.Serial(SENSOR_PORT, BAUDRATE, timeout=1)
        time.sleep(2)
        self.cancelar_escaneo_externo = False

    def motor_home(self):
        self.motor_ser.reset_input_buffer()
        self.motor_ser.write(b'HOME\n')
        start = time.time()
        while True:
            line = self.motor_ser.readline().decode().strip()
            if line == "OK HOME":
                return
            if "ERROR" in line or "EMERGENCY" in line:
                raise RuntimeError(f"Error en HOME: {line}")
            if time.time() - start > 37:
                raise TimeoutError("motor_home: Timeout")
            time.sleep(0.1)

    def motor_move(self, x_mm):
        self.motor_ser.reset_input_buffer()
        cmd = f"MOVE {x_mm:.2f}\n".encode()
        self.motor_ser.write(cmd)
        start = time.time()
        while True:
            line = self.motor_ser.readline().decode().strip()
            if line.startswith("OK POS"):
                return
            if "ERROR" in line or "EMERGENCY" in line:
                raise RuntimeError(f"Error en MOVE: {line}")
            if time.time() - start > 40:
                raise TimeoutError("motor_move: Timeout")
            time.sleep(0.1)

    def sensor_read(self):
        self.sensor_ser.reset_input_buffer()
        self.sensor_ser.write(b'MEASURE\n')
        start = time.time()
        while True:
            line = self.sensor_ser.readline().decode().strip()
            if line.startswith("DIST"):
                try:
                    return int(line.split()[1])
                except:
                    raise RuntimeError(f"Formato DIST incorrecto: {line}")
            if time.time() - start > 5:
                raise TimeoutError("sensor_read: Timeout")
            time.sleep(0.1)

    def run_scan_filtrado(self):
        THRESHOLD = 4
        MIN_RUN = 20

        vertices = []
        last_plateau_y = None
        run_length = 0
        run_start_x = None
        prev_x = None

        for i in range(N_STEPS):
            if self.cancelar_escaneo_externo:
                break

            x = i * STEP_MM
            self.motor_move(x)
            y = self.sensor_read()

            if last_plateau_y is None:
                last_plateau_y = y
                run_length = 15
                run_start_x = x
            else:
                if abs(y - last_plateau_y) <= THRESHOLD:
                    run_length += 1
                else:
                    if run_length >= MIN_RUN:
                        if -6 <= (last_plateau_y - OFFSET) <= 6:
                            last_plateau_y = 0
                        else:
                            last_plateau_y -= OFFSET

                        new_plane = (run_start_x, prev_x, last_plateau_y)
                        if vertices:
                            x0_prev, x1_prev, y_prev = vertices[-1]
                            y_new = new_plane[2]
                            if (y_prev > 0 and y_new > 0 and abs(y_new - y_prev) <= THRESHOLD + 2 and
                                    abs(run_start_x - x1_prev) <= STEP_MM * 2):
                                vertices[-1] = (x0_prev, prev_x, (y_prev + 2 * y_new) / 3)
                            else:
                                vertices.append(new_plane)
                        else:
                            vertices.append(new_plane)
                    last_plateau_y = y
                    run_length = 1
                    run_start_x = x
            prev_x = x

        # Último tramo
        if run_length >= MIN_RUN:
            last_plateau_y = 0
            vertices.append((run_start_x, prev_x, last_plateau_y))

        if self.cancelar_escaneo_externo:
            return  # Terminó antes de completar, no procesa planos

        if len(vertices) != 5:
            raise ValueError(f"[ERROR] Se esperaban 5 planos, se detectaron {len(vertices)}")

        # Generar los 8 vértices compensados
        raw_x = [
            vertices[0][1],
            vertices[1][0] + 5,
            vertices[1][1] - 5,
            vertices[2][0],
            vertices[2][1],
            vertices[3][0],
            vertices[3][1] - 5,
            vertices[4][0],
        ]
        raw_y = [
            vertices[0][2],
            vertices[1][2],
            vertices[1][2],
            vertices[2][2],
            vertices[2][2],
            vertices[3][2] - 5,
            vertices[3][2] - 5,
            vertices[4][2],
        ]

        for x, y in zip(raw_x, raw_y):
            yield x, y

        self.motor_home()

    def escaneo_crudo(self):
        for i in range(N_STEPS):
            if self.cancelar_escaneo_externo:
                break
            x = i * STEP_MM
            self.motor_move(x)
            y = self.sensor_read()
            yield x, y

    def filtrar_puntos_crudos(self, puntos_crudos):
        THRESHOLD = 4
        MIN_RUN = 20
        OFFSET = 34

        vertices = []
        last_plateau_y = None
        run_length = 0
        run_start_x = None
        prev_x = None

        for x, y in puntos_crudos:
            if last_plateau_y is None:
                last_plateau_y = y
                run_length = 15
                run_start_x = x
            else:
                if abs(y - last_plateau_y) <= THRESHOLD:
                    run_length += 1
                else:
                    if run_length >= MIN_RUN:
                        if -6 <= (last_plateau_y - OFFSET) <= 6:
                            last_plateau_y = 0
                        else:
                            last_plateau_y -= OFFSET

                        new_plane = (run_start_x, prev_x, last_plateau_y)
                        if vertices:
                            x0_prev, x1_prev, y_prev = vertices[-1]
                            y_new = new_plane[2]
                            if (y_prev > 0 and y_new > 0 and abs(y_new - y_prev) <= THRESHOLD + 2 and
                                    abs(run_start_x - x1_prev) <= STEP_MM * 2):
                                vertices[-1] = (x0_prev, prev_x, (y_prev + 2 * y_new) / 3)
                            else:
                                vertices.append(new_plane)
                        else:
                            vertices.append(new_plane)
                    last_plateau_y = y
                    run_length = 1
                    run_start_x = x
            prev_x = x

        if run_length >= MIN_RUN:
            last_plateau_y = 0
            vertices.append((run_start_x, prev_x, last_plateau_y))

        if len(vertices) != 5:
            raise ValueError(f"[ERROR] Se esperaban 5 planos, se detectaron {len(vertices)}")

        raw_x = [
            vertices[0][1],
            vertices[1][0] + 5,
            vertices[1][1] - 5,
            vertices[2][0],
            vertices[2][1],
            vertices[3][0],
            vertices[3][1] - 5,
            vertices[4][0],
        ]
        raw_y = [
            vertices[0][2],
            vertices[1][2],
            vertices[1][2],
            vertices[2][2],
            vertices[2][2],
            vertices[3][2] - 5,
            vertices[3][2] - 5,
            vertices[4][2],
        ]

        return list(zip(raw_x, raw_y))
