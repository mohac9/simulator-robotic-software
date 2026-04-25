import traceback
import importlib.util
import sys
import time
import libraries.standard as standard
import libraries.serial as serial
import robot_components.robot_state as state

from .interpreter import ArduinoInterpreter
import output.console as console


module = None

class Command:
    def __init__(self, controller):
        self.controller = controller
        self.ready = False

    def execute(self):
        """
        Executes a command object
        """
        pass

    def reboot(self):
        self.ready = False

    def prepare_exec(self):
        standard.board = self.controller.robot_layer.robot.board
        standard.state = state.State()
        serial.cons = self.controller.console
        self.ready = True


class Compile(Command):
    def __init__(self, controller):
        super().__init__(controller)
        self.interpreter = None

    def execute(self):
        try:
            code = self.controller.get_code()
            self.interpreter = ArduinoInterpreter(code)

            self.interpreter.run(self.interpreter.parser_object)

            self.interpreter.register_libraries(
            self.controller.robot_layer.robot.board,
            self.controller.console
            )
            #Si se esta en modo debug
            if hasattr(self.controller, 'debug_manager') and self.controller.debug_manager:
                self.interpreter.env.debugger = self.controller.debug_manager.debugger
            
            if self.interpreter.had_runtime_error:
                self.controller.console.print_error(
                    console.Error("Error de compilación", 0, 0, "El sketch no se ha podido compilar correctamente")
                )
                return False
            return True

        except Exception as e:
                print(f'la excepción es {e}')
                traceback.print_exc()
                self.controller.console.write_error(
                console.Error("Error de compilación", 0, 0, "El sketch no se ha podido compilar correctamente"))
                return False
        
        
    def compile(self,code):
        try:
            interpreter = ArduinoInterpreter(code)
            if hasattr(self.controller, 'debug_manager') and self.controller.debug_manager:
                interpreter.env.debugger = self.controller.debug_manager.debugger
            if interpreter.had_runtime_error:
                return None
            return interpreter
        except Exception as e:
            print(f'la excepción es {e}')
            traceback.print_exc()
            self.controller.console.write_error(
                console.Error("Error de compilación", 0, 0, "El sketch no se ha podido compilar correctamente"))
            return None


class Setup(Command):
    def __init__(self, controller):
        super().__init__(controller)

    def execute(self):
        if not self.ready:
            self.prepare_exec()

        interpreter = self.controller.compile_command.interpreter
        if not interpreter:
            self.controller.console.write_error(
                console.Error("Error de ejecución", 0, 0, "No se ha compilado ningún sketch")
            )
            return False
        
        

        #board = self.controller.robot_layer.robot.board
        #console_obj = self.controller.console
        #interpreter.register_libraries(board, console_obj)


        
        curr_time_ns = time.time_ns()
        if (
            not standard.state.exec_time_us > curr_time_ns / 1000
            and not standard.state.exec_time_ms > curr_time_ns / 1000000
        ):
            try:
                setup_func = None
                for func in interpreter.env.get_all_functions():
                    if func['signature'].startswith('setup'):
                        setup_func = func['function_object']
                        break
                if setup_func:
                    print("Ejecutando setup()")
                    setup_func.body_execution(interpreter.env)
                    print("Se ha ejecutado setup() correctamente")
                else:
                    self.controller.console.write_warning(
                    console.Warning("Aviso", 0, 0, "No se ha encontrado la función setup()")
                )
                return True
            
            except Exception as e:
                print(f'Error ejecutando setup(): {e}')
                traceback.print_exc()
                self.controller.console.write_error(
                    console.Error("Error de ejecución", 0, 0, "No se ha podido ejecutar la función setup()")
                )
                return False
        return True
    
    
class Loop(Command):
    def __init__(self, controller):
        super().__init__(controller)

    def execute(self):
        print("Entrando en execute loop()")
        if not self.ready:
            self.prepare_exec()

        interpreter = self.controller.compile_command.interpreter
        if not interpreter:
            self.controller.console.write_error(
                console.Error("Error de ejecución", 0, 0, "No se ha compilado ningún sketch")
            )
            self.controller.executing = False
            return False
        
        curr_time_ns = time.time_ns()
        if (
            not standard.state.exec_time_us > curr_time_ns / 1000
            and not standard.state.exec_time_ms > curr_time_ns / 1000000
            #and not standard.state.exited and self.controller.executing
        ):
            try:
                loop_func = None
                for func in interpreter.env.get_all_functions():
                    if func['signature'].startswith('loop'):
                        loop_func = func['function_object']
                        break
                        
                if loop_func:
                    print("Ejecutando loop()")
                    loop_func.body_execution(interpreter.env)
                    print("Se ha ejecutado loop() correctamente")
                else:
                    self.controller.console.write_warning(
                        console.Warning("Aviso", 0, 0, "No se ha encontrado la función loop()")
                    )
                    self.controller.executing = False
                    return False
                    
                return True
                
            except Exception as e:
                print(f'Error ejecutando loop(): {e}')
                traceback.print_exc()
                self.controller.console.write_error(
                    console.Error("Error de ejecución", 0, 0, "No se ha podido ejecutar la función loop()")
                )
                self.controller.executing = False
                return False
                
        return True