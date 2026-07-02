import traceback
import importlib.util
import sys
import time
import libraries.standard as standard
import libraries.serial as serial
import robot_components.robot_state as state

import graphics.layers as la

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
    def __init__(self, controller,debug_manager=None):
        super().__init__(controller)
        self.interpreter = None
        self.debug_manager = debug_manager

    def execute(self):
        try:
            code = self.controller.get_code()
            self.interpreter = ArduinoInterpreter(code)
            self.interpreter.env.add_board(self.controller.robot_layer.robot.board)
            #Añadir en el entorno de forma forzada los servos ya construidos
            self.link_elements_to_env()
            #Debugger gets injected into the environment before the first AST node is even executed
            if self.debug_manager:
                print(f"INYECCION EXITOSA DEL MANEJADOR DEL DEPURADOR:{self.debug_manager} *** CON DEPURADOR: {self.debug_manager.debugger}")
                self.interpreter.env.activate_debug_mode(self.debug_manager.debugger) 
            print(f"El objeto board que se le da al interprete es el siguiente: {self.controller.robot_layer.robot.board}")
            self.interpreter.run_init()

            self.interpreter.register_libraries(
            self.controller.robot_layer.robot.board,
            self.controller.console

            )
          
            
            
            
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

    #This method adds the objects that were already created in robot
    def link_elements_to_env(self):
        #Add servos depending of the type of robot that is given
        if isinstance(self.controller.robot_layer,la.MobileRobotLayer):
            #The names used are the only possibilities to init them, I know is a bit rough but this should work. If you need more elements add them here 
            self.interpreter.env.add_hw_element("servoIzq",self.controller.robot_layer.robot.servo_left)
            self.interpreter.env.add_hw_element("servoDer",self.controller.robot_layer.robot.servo_right)
        if isinstance(self.controller.robot_layer,la.LinearActuatorLayer):
            self.self.interpreter.env.add_hw_element("servo",self.controller.robot_layer.robot.servo)
          
        
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
                interpreter.run_setup()
                print("Se ha ejecutado setup() correctamente")

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
                interpreter.run_loop_once()  
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