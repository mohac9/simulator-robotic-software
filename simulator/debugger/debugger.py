import threading
import queue
import time
from enum import StrEnum

#Modos de ejecución del debugger
class DebugCommand(StrEnum):
    CONTINUE = 'continue'
    STEP_INTO = 'step_into'
    STEP_OVER = 'step_over'
    STEP_OUT = 'step_out'
    PAUSE = 'pause' #Uso interno


class Debugger:
    def __init__(self,pause_callback=None,controller=None):
        self.breakpoints = set()
        self.is_executing = False
        self.pause_callback = pause_callback
        self.controller = controller  
        self.iteration = 0
        self.debugger_mode = DebugCommand.CONTINUE #Se cambia en cmd_processor 
        self.pause_event = threading.Event()
        self.abort = False
        self.current_env = None


        
        
             

        
        
  

    #Procesador de comandos del debugger
    def cmd_processor(self,cmd):
        dic = {'continue': DebugCommand.CONTINUE,
               'step_into': DebugCommand.STEP_INTO,
               'step_into': DebugCommand.STEP_OVER,
               'step_out': DebugCommand.STEP_OUT
               }
 
        self.debugger_mode = dic.get(cmd, None)
        if self.debugger_mode is None:
            print(f"Comando desconocido: {cmd}")
            return
        
        self.pause_event.set()
        


            
    def execute_arduino_code(self,init_pause=False): 
        #Pausa inicial, espera al primer comando de ejecución para empezar a ejecutar el código
        init_pause.wait()  
        try:
            self.is_executing = True
            #Cargar includes y variables globales
            if self.controller.compile_command.execute():
                print("Se ejecuto correctamente el comando de compilación")
                if self.controller.setup_command.execute():
                    print("Se ejecuto correctamente el comando de setup")
                    for i in range(60*1000):#Iteraciones del bucle loop
                        self.controller.loop_command.execute()
                        print(f"Iteración {i} del loop")
                        time.sleep(0.01)
        except Exception as e:
            print(f'Error en ejecución: {e}')

                    
              




    def add_breakpoint(self, line):
        self.breakpoints.add(line)

    def remove_breakpoint(self, line):
        self.breakpoints.discard(line)
    
    #Recibe un comando del intérprete, lo procesa y decide si se debe pausar la ejecución o no


    def stop(self):
        self.abort = True
        self.pause_event.set()

    def pause(self,current_line, env):
        self.debugger_mode = DebugCommand.PAUSE
        self.pause_event.clear()
        self.pause_callback(current_line, env)
        self.pause_event.wait()


    def check_pause(self, current_line, env):
        print(f"Check pause: línea {current_line}, entorno {env}, modo {self.debugger_mode}")
        print(f"Modo de depuración: {self.debugger_mode}, breakpoints: {self.breakpoints}")
        print(f"debugger_mode: {self.debugger_mode}, step_into: {DebugCommand.STEP_INTO}, step_over: {DebugCommand.STEP_OVER}, step_out: {DebugCommand.STEP_OUT}")
        x = self.debugger_mode
        y = DebugCommand.STEP_INTO

        
        if x == y:
            print("Los valores son iguales")

        if self.abort:
            raise Exception("Ejecución abortada por el usuario")
        # Casos en los que no se hace nada:
        if current_line == -1:
            return
        if current_line not in self.breakpoints and self.debugger_mode == DebugCommand.CONTINUE:
            return
        # Logica de ejecución :
        if current_line == -1:
            return
        elif self.debugger_mode == DebugCommand.CONTINUE:
            if current_line in self.breakpoints:
                self.pause(current_line, env)
        elif self.debugger_mode == DebugCommand.STEP_INTO:
            self.pause(current_line, env)
        elif self.debugger_mode == DebugCommand.STEP_OVER:
            if env == self.current_env or current_line in self.breakpoints:
                self.pause(current_line, env)
            self.current_env = env
        elif self.debugger_mode == DebugCommand.STEP_OUT:
            if env != self.current_env or env.parent is None or current_line in self.breakpoints:
                self.pause(current_line, env)

        if self.abort:
            raise Exception("Ejecución abortada por el usuario")
        
