import threading
import queue
import time


class Debugger:
    def __init__(self,pause_callback=None,controller=None):
        self.breakpoints = set()
        self.is_executing = False
        self.controller = controller  
        self.iteration = 0
             

        
        
  

    #Loop del depurador
    def debugger_loop(self,command_queue, env_queue):
        debug_mode = True
        while debug_mode:
            #Leer cmd
            cmd = command_queue.get()
            if cmd == 'stop':
                debug_mode = False
                continue
            else:
                self.execute_arduino_code(cmd)
                
            
    def execute_arduino_code(self,cmd): 
        try:
            self.is_executing = True
            #Cargar includes y variables globales
            if self.controller.compile_command.execute():
                if self.controller.setup_command.execute():
                    for i in range(60*1000):#Iteraciones del bucle loop
                        self.controller.loop_command.execute()
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

    def check_pause(self, current_line, env):
        print("Llega aqui al check_pause", current_line, env)
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
