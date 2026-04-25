import threading
from debugger.debugger import Debugger
import queue



#Fachada, se emplea para ocultar la complejidad del debugger y su integración con el resto de la aplicación.
class DebugManager:
    def __init__(self,application,callback_pause=None):
        self.application = application
        self.debugger = Debugger(pause_callback=callback_pause,controller=self.application.controller)
        self.is_executing = False
        self.debugger_thread = None
        #Comunicación al thread de depuración
        self.init_pause = threading.Event()


        
        

    def start_execution(self,breakpoints):
        self.update_breakpoints(breakpoints)

        self.application.controller.debug_manager = self
        self.is_executing = True

        self.command_queue = queue.Queue()
        self.env_queue = queue.Queue()

        #Crea el thread de ejecucion del debugger
        self.debugger_thread = threading.Thread(target=self.debugger.execute_arduino_code, daemon=True, args=(self.init_pause,))
        self.debugger_thread.start()
        
        self._gui_drawing_loop()

    def _gui_drawing_loop(self):
        if self.is_executing:
            if hasattr(self.application, 'controller') and self.application.controller.executing:
                import graphics.screen_updater as screen_updater
                try:
                    screen_updater.refresh()
                except Exception as e:
                    pass
            # Tkinter vuelve a llamar a esta función en 16ms (~60FPS)
            self.application.identifier = self.application.after(16, self._gui_drawing_loop)

    def update_breakpoints(self,tracepoints_set):
        lines = {int(str(tp).split(".")[0]) for tp in tracepoints_set}
        self.debugger.breakpoints = lines

    #Botones del thread de depuración

    def send_command(self, command):
        self.debugger.cmd_processor(command)
        self.init_pause.set()  # Desbloquea la ejecución del código
        

        


    def stop(self):
        self.debugger.stop()
        self.is_executing = False
        self.application.controller.stop()
