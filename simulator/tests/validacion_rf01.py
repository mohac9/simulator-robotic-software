"""
Bateria de pruebas de validacion del requisito RF-01 (Procesamiento del
codigo fuente).

Cada caso de prueba es un sketch de Arduino que ejercita una
construccion del lenguaje. El caso se considera correcto si el pipeline
completo (lexer -> parser -> interprete) se ejecuta sin excepciones y
las variables observadas terminan con el valor esperado.

Uso (desde la carpeta simulator/):
    python tests/validacion_rf01.py
"""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from compiler_v2.interpreter import ArduinoInterpreter


# ---------------------------------------------------------------------------
# Definicion de los casos de prueba
# ---------------------------------------------------------------------------
# nombre:         identificador del caso
# codigo:          sketch de Arduino a ejecutar
# esperado:        valores finales que deben tener las variables globales
# iteraciones:     numero de veces que se ejecuta loop() (1 por defecto)
# error_esperado:  si esta presente, el caso es negativo: el sketch es
#                  incorrecto y la ejecucion debe lanzar ese tipo de error

CASOS = [
    {
        "nombre": "declaraciones_y_tipos",
        "codigo": """
            int a = 5;
            float b = 2.5;
            bool c = true;
            void setup() {
            }
            void loop() {
            }
        """,
        "esperado": {"a": 5, "b": 2.5, "c": True},
    },
    {
        "nombre": "operaciones_aritmeticas",
        "codigo": """
            int x = 7;
            int y = 3;
            int suma = 0;
            int resta = 0;
            int producto = 0;
            int resto = 0;
            void setup() {
                suma = x + y;
                resta = x - y;
                producto = x * y;
                resto = x % y;
            }
            void loop() {
            }
        """,
        "esperado": {"suma": 10, "resta": 4, "producto": 21, "resto": 1},
    },
    {
        "nombre": "condicional_if_else",
        "codigo": """
            int valor = 10;
            int rama_if = 0;
            int rama_else = 0;
            void setup() {
                if (valor > 5) {
                    rama_if = 1;
                } else {
                    rama_if = 2;
                }
                if (valor < 5) {
                    rama_else = 1;
                } else {
                    rama_else = 2;
                }
            }
            void loop() {
            }
        """,
        "esperado": {"rama_if": 1, "rama_else": 2},
    },
    {
        "nombre": "bucle_while",
        "codigo": """
            int contador = 0;
            void setup() {
                while (contador < 5) {
                    contador = contador + 1;
                }
            }
            void loop() {
            }
        """,
        "esperado": {"contador": 5},
    },
    {
        "nombre": "bucle_do_while",
        "codigo": """
            int valor = 0;
            void setup() {
                do {
                    valor = valor + 2;
                } while (valor < 10);
            }
            void loop() {
            }
        """,
        "esperado": {"valor": 10},
    },
    {
        "nombre": "bucle_for_y_break",
        "codigo": """
            int acumulado = 0;
            void setup() {
                for (int i = 0; i < 100; ) {
                    acumulado = acumulado + i;
                    i = i + 1;
                    if (i > 4) {
                        break;
                    }
                }
            }
            void loop() {
            }
        """,
        "esperado": {"acumulado": 10},
    },
    {
        "nombre": "switch_case_break",
        "codigo": """
            int opcion = 2;
            int salida = 0;
            void setup() {
                switch (opcion) {
                    case 1:
                        salida = 10;
                        break;
                    case 2:
                        salida = 20;
                        break;
                    default:
                        salida = 99;
                }
            }
            void loop() {
            }
        """,
        "esperado": {"salida": 20},
    },
    {
        "nombre": "funcion_con_retorno",
        "codigo": """
            int resultado = 0;
            int sumar(int a, int b) {
                return a + b;
            }
            void setup() {
                resultado = sumar(4, 6);
            }
            void loop() {
            }
        """,
        "esperado": {"resultado": 10},
    },
    {
        "nombre": "sobrecarga_de_funciones",
        "codigo": """
            int resultado_a = 0;
            int resultado_b = 0;
            int duplicar(int x) {
                return x + x;
            }
            int duplicar(int x, int y) {
                return x + y + x + y;
            }
            void setup() {
                resultado_a = duplicar(3);
                resultado_b = duplicar(3, 4);
            }
            void loop() {
            }
        """,
        "esperado": {"resultado_a": 6, "resultado_b": 14},
    },
    {
        "nombre": "funcion_recursiva",
        "codigo": """
            int resultado = 0;
            int factorial(int n) {
                if (n < 2) {
                    return 1;
                }
                return n * factorial(n - 1);
            }
            void setup() {
                resultado = factorial(5);
            }
            void loop() {
            }
        """,
        "esperado": {"resultado": 120},
    },
    {
        "nombre": "ambitos_y_variables_globales",
        "codigo": """
            int contador_global = 0;
            void incrementar() {
                contador_global = contador_global + 1;
            }
            void setup() {
            }
            void loop() {
                incrementar();
            }
        """,
        "esperado": {"contador_global": 3},
        "iteraciones": 3,
    },
    {
        "nombre": "operaciones_con_float",
        "codigo": """
            float precio = 2.5;
            float total = 0.0;
            void setup() {
                total = precio * 4.0;
            }
            void loop() {
            }
        """,
        "esperado": {"total": 10.0},
    },
    {
        "nombre": "integracion_programa_completo",
        "codigo": """
            int total = 0;
            int iteracion = 0;
            int modo = 0;
            int avisos = 0;

            int cuadrado(int n) {
                return n * n;
            }

            int clasificar(int n) {
                if (n > 50) {
                    return 2;
                }
                if (n > 10) {
                    return 1;
                }
                return 0;
            }

            void setup() {
                total = 0;
                iteracion = 0;
            }

            void loop() {
                iteracion = iteracion + 1;
                int aporte = cuadrado(iteracion);
                total = total + aporte;
                modo = clasificar(total);
                switch (modo) {
                    case 1:
                        avisos = avisos + 1;
                        break;
                    case 2:
                        avisos = avisos + 10;
                        break;
                    default:
                        break;
                }
            }
        """,
        "esperado": {"total": 30, "iteracion": 4, "modo": 1, "avisos": 2},
        "iteraciones": 4,
    },
    # ------------------------------------------------------------------
    # Casos negativos: el sistema debe rechazar codigo incorrecto
    # lanzando un error controlado, nunca ejecutarlo en silencio.
    # ------------------------------------------------------------------
    {
        "nombre": "negativo_variable_no_declarada",
        "codigo": """
            void setup() {
                y = 5;
            }
            void loop() {
            }
        """,
        "error_esperado": RuntimeError,
    },
    {
        "nombre": "negativo_funcion_no_declarada",
        "codigo": """
            void setup() {
                inexistente();
            }
            void loop() {
            }
        """,
        "error_esperado": KeyError,
    },
    {
        "nombre": "negativo_declaracion_duplicada",
        "codigo": """
            int a = 1;
            int a = 2;
            void setup() {
            }
            void loop() {
            }
        """,
        "error_esperado": RuntimeError,
    },
    {
        "nombre": "negativo_funcion_sin_retorno",
        "codigo": """
            int resultado = 0;
            int roto() {
                int x = 1;
            }
            void setup() {
                resultado = roto();
            }
            void loop() {
            }
        """,
        "error_esperado": RuntimeError,
    },
]


# ---------------------------------------------------------------------------
# Ejecucion de un sketch a traves del pipeline completo del interprete
# ---------------------------------------------------------------------------

def ejecutar_sketch(codigo, iteraciones_loop=1):
    """Ejecuta un sketch (init + setup + N iteraciones de loop) y
    devuelve el entorno global resultante."""
    salida_interna = io.StringIO()
    with redirect_stdout(salida_interna):
        interprete = ArduinoInterpreter(codigo)
        if interprete.parser_object is None:
            raise SyntaxError("El parser no ha podido generar el AST")
        interprete.run_init()
        if interprete.had_runtime_error:
            raise RuntimeError("Error en tiempo de ejecucion durante la inicializacion")
        interprete.run_setup()
        for _ in range(iteraciones_loop):
            interprete.run_loop_once()
    return interprete.env


# ---------------------------------------------------------------------------
# Generacion dinamica de los tests (un metodo unittest por caso)
# ---------------------------------------------------------------------------

class TestRF01(unittest.TestCase):
    """Validacion del RF-01: procesamiento y ejecucion del codigo fuente."""
    pass


def _crear_test(caso):
    def test(self):
        if "error_esperado" in caso:
            with self.assertRaises(caso["error_esperado"]):
                ejecutar_sketch(caso["codigo"], caso.get("iteraciones", 1))
            return
        env = ejecutar_sketch(caso["codigo"], caso.get("iteraciones", 1))
        for nombre_var, valor_esperado in caso["esperado"].items():
            contenido = env.get_variable_contents(nombre_var)
            self.assertIsNotNone(
                contenido,
                f"La variable '{nombre_var}' no tiene contenido")
            valor_real = getattr(contenido, "value", contenido)
            self.assertEqual(
                valor_real, valor_esperado,
                f"'{nombre_var}' vale {valor_real}, se esperaba {valor_esperado}")
    return test


for _caso in CASOS:
    setattr(TestRF01, f"test_{_caso['nombre']}", _crear_test(_caso))


# ---------------------------------------------------------------------------
# Ejecucion con resumen por consola
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Validacion RF-01: procesamiento del codigo fuente")
    print("=" * 60)

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestRF01)
    exitos = 0
    fallos = []

    for test in suite:
        resultado = unittest.TestResult()
        test.run(resultado)
        nombre = test._testMethodName.replace("test_", "")
        if resultado.wasSuccessful():
            print(f"[OK]    {nombre}")
            exitos += 1
        else:
            problemas = resultado.failures + resultado.errors
            traza = problemas[0][1].strip().splitlines()
            motivo = traza[-1] if traza else "error desconocido"
            print(f"[FALLO] {nombre}")
            print(f"        -> {motivo}")
            fallos.append(nombre)

    total = exitos + len(fallos)
    print("-" * 60)
    print(f"Resultado: {exitos}/{total} casos correctos")
    if fallos:
        print(f"Casos fallidos: {', '.join(fallos)}")
        sys.exit(1)
