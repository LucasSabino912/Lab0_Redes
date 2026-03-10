Claro, aquí tienes un resumen de los archivos en el directorio Lab0_Redes, qué necesitas instalar y cómo puedes ejecutar el proyecto.

hget.py: Es la implementación de un cliente HTTP simple, similar a wget o curl. Su función es realizar peticiones a servidores web. Basado en el requirements.txt, este script solo utiliza la librería estándar de Python.

servidor_lab0.py: Es un servidor web de prueba diseñado específicamente para este laboratorio. hget.py se conectará a este servidor para realizar las pruebas.

hget-test.py: Contiene los tests que verifican si tu implementación de hget.py funciona correctamente.
test_metrics.py: Este archivo prueba la calidad de tu código, verificando métricas como la complejidad ciclomática y la cobertura de los tests.

grade.py: Es un script de autoevaluación. Ejecuta todos los tests (hget-test.py y test_metrics.py), realiza un análisis estático del código y te da una nota final para el laboratorio. Es la forma principal de verificar si tu trabajo está correcto.
requirements.txt: Este archivo lista las librerías de Python que son necesarias para ejecutar los tests y el script de evaluación.

pyproject.toml: Es un archivo de configuración para las herramientas de desarrollo de Python que se usan en el proyecto, como pytest (para los tests) y ruff (para el análisis estático de código).

Necesitas instalar las dependencias listadas en requirements.txt. Puedes hacerlo ejecutando el siguiente comando en tu terminal, dentro del directorio Lab0_Redes: