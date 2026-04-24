import unittest
import tkinter as tk

from simulator.graphics.gui import MainApplication
"""
Pruebas para el Debugger
"""
class TestDebugger(unittest.TestCase):

    def setUp(self):
        self.app = MainApplication()
       

    def tearDown(self):
        self.app.close()

    def test_flujo_debugger(self):

        #Paso 1: Escribir código en el editor
        code_test = '''
        int contador_global = 0;
        int limite = 5;

        void actualizarContador() {
            int paso = 1;
            contador_global = contador_global + paso;
        }

        void setup() {
            contador_global = 0;
        }

        void loop() {
            if (contador_global < limite) {
            actualizarContador();
        }
    }
    '''
        self.app.text_area.delete("1.0", tk.END)
        self.app.text_area.insert("1.0", code_test)
        
        #Paso 2: Abrir depurador
        self.app.button_bar.debug_button.invoke()
        self.app.update_idletasks()

        #Paso 3: Agregar los breakpoints
        self.app.update_tracepoints({"3.0"})

        #Paso 4: Comprobar si el panel de depuración es visible
        self.assertTrue(self.app.debug_panel_visible, "El panel de depuración debería ser visible.")

        #Paso 5: Se realiza un paso
        self.app.debug_panel.step_button.invoke()
        self.app.update_idletasks()

if __name__ == '__main__':
    unittest.main()

        



