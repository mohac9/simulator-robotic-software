import threading

class Debugger:
    def __init__(self,pause_callback=None):
        self.breakpoints = set()
        self.step_mode = False
        self.abort = False

        # Dormir el hilo del depurador hasta que se le indique que continúe
        self.pause_event = threading.Event()
        self.pause_callback = pause_callback

        self.current_command = None

    def add_breakpoint(self, line):
        self.breakpoints.add(line)

    def remove_breakpoint(self, line):
        self.breakpoints.discard(line)
    
    #Recibe un comando del intérprete, lo procesa y decide si se debe pausar la ejecución o no
    def cmd_process(self, cmd):
        self.current_comand = cmd
        self.pause_event.set()

    def stop(self):
        self.abort = True
        self.pause_event.set()

    def check_pause(self, current_line, env):
        if self.abort:
            raise Exception("Ejecución abortada por el usuario")

        # Casos en los que no se hace nada:
        if current_line == -1:
            return
        if current_line not in self.breakpoints and not self.step_mode:
            return
        # En este punto, se ha alcanzado un breakpoint o se ha activado el modo paso a paso, por lo que se pausa la ejecución
        self.step_mode = False
        self.pause_event.clear()
        # Llamar al callback para que la interfaz gráfica se actualice con la información del estado actual del programa
        if self.pause_callback:
            self.pause_callback(current_line, env)

        self.pause_event.wait()

        if self.abort:
            raise Exception("Ejecución abortada por el usuario")
        
        if self.current_comand in ['step','next']:
            self.step_mode = True