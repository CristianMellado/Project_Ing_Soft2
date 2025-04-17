#  Proyecto Final de Ing. Software II

## Profesor
- Guillermo Enrique Calderon Ruiz

## Alumnos

- Briceño Quiroz Anthony Angel
- Carpio Mamani Alexander
- Cruz Laura Eduardo Jacob
- Mellado Baca Cristian
- Torres Acuña Marcelo


# Sistema de Portal de Descarga de Contenidos

Este proyecto consiste en un sistema asociado a un portal de descarga de contenidos en formato de imágenes (PNG, JPG, etc.), sonidos (MP3, MID, etc.) y videos (MPG, MOV, etc.). El sistema maneja cuentas de usuario y administrador, historial de descargas, promociones, regalos de contenidos entre usuarios, notas de contenidos, y gestión de categorías.

## Descripción General

El portal permite a los usuarios comprar, regalar y calificar contenidos, mientras que el administrador puede gestionar contenidos, usuarios, categorías y promociones. Además, el sistema realiza descuentos automáticos dependiendo del historial de descargas del usuario y permite la creación de promociones para aumentar las ventas.

### Funcionalidades Principales

1. **Registro de Clientes**: Las personas se registran como nuevos clientes.
2. **Cierre de Cuenta**: Los clientes pueden cerrar su cuenta (requiere saldo en cero).
3. **Descarga de Contenidos**: Los clientes pueden descargar contenidos y aplicar descuentos si tienen un historial de compras significativo.
4. **Regalo de Contenidos**: Los clientes pueden regalar contenidos a otros usuarios.
5. **Calificación de Contenidos**: Los usuarios pueden poner una nota de 1 a 10 a los contenidos descargados.
6. **Gestión de Contenidos**: El administrador puede agregar o eliminar contenidos.
7. **Gestión de Categorías**: El administrador puede crear categorías y asignarlas a los contenidos.
8. **Promociones**: El administrador puede crear promociones de descuento para varios contenidos.

### Consultas y Reportes

1. **Consultar Información del Cliente**: Mostrar datos del cliente (nombre, saldo, últimos 10 contenidos descargados).
2. **Consultar Información del Contenido**: Mostrar detalles de un contenido (nombre, autor, descripción, precio, etc.).
3. **Búsqueda por Autor**: Mostrar contenidos de un autor en específico.
4. **Listado de Notas de un Usuario**: Mostrar las notas que un usuario ha dado a los contenidos.
5. **Consulta de Categorías**: Ver todos los contenidos en una categoría específica.
6. **Ranking de Contenidos Más Descargados**: Mostrar los 10 contenidos más descargados.
7. **Ranking de Contenidos con Mejor Nota**: Mostrar los 10 contenidos mejor calificados.
8. **Listado de Clientes por Descargas**: Listar los clientes ordenados por número de descargas en los últimos 6 meses.

## Requerimientos del Sistema

### Funcionalidades de Usuario

- **Clientes**:
  - Registro de nuevos clientes con nombre completo, login, contraseña y saldo.
  - Consultar los últimos contenidos descargados, con posibilidad de hacer descargas con descuentos.
  - Regalar contenidos a otros usuarios.
  - Calificar contenidos descargados.
  
- **Administrador**:
  - Cargar y eliminar contenidos del portal.
  - Gestionar categorías (crear y asignar).
  - Crear promociones para contenidos.
  - Cargar dinero a las cuentas de los usuarios.

### Datos del Contenido

Cada contenido tiene los siguientes atributos:
- **Nombre**: Nombre del contenido.
- **Autor**: Nombre del autor.
- **Descripción**: Descripción del contenido.
- **Precio**: Precio del contenido.
- **Tipo de Archivo**: Formato (JPG, MP3, AVI, etc.).
- **Tamaño**: Tamaño del archivo en bytes.
- **Archivo**: Secuencia de bytes que contiene el archivo.

### Categorías

Las categorías son jerárquicas, lo que significa que pueden tener subcategorías, formando un árbol sin límite de profundidad.

### Promociones

Las promociones ofrecen un descuento en ciertos contenidos, y están asociadas con un porcentaje de descuento y un periodo de inicio y fin.

---

## Requerimientos Mínimos

El sistema debe soportar las siguientes operaciones:

- **Cliente**:
  - Registro y cierre de cuenta.
  - Descargar contenido (verificando si aplica descuento).
  - Regalar contenido a otro cliente.
  - Poner nota a un contenido descargado.
  
- **Administrador**:
  - Agregar y eliminar contenidos.
  - Crear categorías y asignarlas a contenidos.
  - Crear promociones de descuento.
  - Cargar dinero en la cuenta de un usuario.

### Consultas y Reportes:

- Consultar datos de clientes (nombre, saldo, últimos contenidos descargados).
- Consultar información de un contenido (autor, precio, etc.).
- Consultar todos los contenidos de un autor.
- Ver el ranking de los contenidos más descargados.
- Ver los clientes con más descargas en los últimos 6 meses.

---

## Suposiciones Adicionales

- El sistema no tiene limitaciones de usuarios o contenidos.
- Las promociones solo pueden ser aplicadas a contenidos específicos, y un contenido solo puede tener una promoción activa a la vez.
- Las categorías son jerárquicas, pero no hay un límite de profundidad.
- Los usuarios no pueden cambiar sus notas una vez que las han puesto.