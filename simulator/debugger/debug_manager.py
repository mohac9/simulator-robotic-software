import threading
import time
from debugger.debugger import Debugger

class DebugManager:
    def __init__(self,application,callback_pause=None):
        self.application = application
        self.debugger = Debugger(pause_callback=callback_pause)
        self.execution_thread = None
        self.is_executing = False

    def start_execution(self,breakpoints):
        self.uptdate_breakpoints(breakpoints)

        self.application.controller.debug_manager = self
        self.is_executing = True

        self.execution_thread = threading.Thread(target=self._arduino_logic_thread, daemon=True)
        self.execution_thread.start()

        self._gui_drawing_loop()

    def _arduino_logic_thread(self):
        try:
            controller = self.application.controller

            if controller.compile_command.execute():
                if controller.setup_command.execute():
                    controller.executing = True
                    while self.is_executing and controller.executing:
                        if not self.application.keys_used:
                            controller.loop_command.execute()
                        time.sleep(0.01)  # Evitar un bucle de CPU alta
        except Exception as e:
            if str(e) == "Ejecución abortada por el usuario":
                print("Ejecución abortada por el usuario")
            else:
                print(f"[Depurador] Error en ejecución: {e}")
        finally:
            self.is_executing = False
            if hasattr(self.application, 'controller'):
                self.application.controller.executing = False

    def _gui_drawing_loop(self):
        if self.is_executing:
            import graphics.screen_updater as screen_updater
            screen_updater.refresh()
            # Tkinter vuelve a llamar a esta función en 16ms (~60FPS)
            self.application.identifier = self.application.after(16, self._gui_drawing_loop)

    def uptdate_breakpoints(self,tracepoints_set):
        lines = {int(str(tp).split(".")[0]) for tp in tracepoints_set}
        self.debugger.breakpoints = lines

    def continue_execution(self):
        self.debugger.cmd_process('continue')

    def step(self):
        self.debugger.cmd_process('step')

    def stop(self):
        self.debugger.stop()
        self.is_executing = False
        self.application.controller.stop()
