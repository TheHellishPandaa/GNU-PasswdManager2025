## GNU-PasswdManager in Spannish Languaje

Este código implementa un administrador de contraseñas gráfico utilizando Python con Tkinter y la librería cryptography para el cifrado. El programa permite a los usuarios realizar operaciones básicas de gestión de contraseñas, como:

  - Registrar Usuarios: Los usuarios pueden registrarse con un nombre de usuario y contraseña.
  - Iniciar Sesión: Solo los usuarios registrados pueden acceder al sistema.
  - Añadir Contraseñas: Permite añadir contraseñas asociadas a diferentes servicios.
  - Generar Contraseñas: Genera contraseñas seguras automáticamente.
  - Mostrar Contraseñas: Muestra una lista de contraseñas cifradas que se desencriptan temporalmente para la visualización.
  - Copiar Contraseñas al Portapapeles: Copia contraseñas seleccionadas en la lista.
  - Guardar Datos: Los datos de usuarios y contraseñas se almacenan en archivos JSON.

Características destacadas:

- Cifrado seguro: Las contraseñas se cifran con la biblioteca cryptography usando una clave generada automáticamente y almacenada localmente.
- Interfaz gráfica (GUI): Una interfaz intuitiva para gestionar las contraseñas.
-  JSON para persistencia: Los datos de usuarios y contraseñas se guardan en archivos .json, facilitando su manejo.
