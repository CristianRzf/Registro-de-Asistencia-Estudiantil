Sistema de Registro de Asistencia Estudiantil:
Sistema de gestión de asistencia estudiantil desarrollado en Python con interfaz gráfica Tkinter que permite registrar, consultar y generar reportes de asistencia de estudiantes de manera eficiente.

Objetivo General
Diseñar e implementar una aplicación de escritorio en Python que permita registrar, consultar 
y generar reportes de asistencia estudiantil, garantizando la persistencia de datos y la facilidad 
de uso mediante una interfaz gráfica. 

Objetivos Específicos
 Implementar una interfaz gráfica intuitiva con Tkinter, que permita un manejo 
sencillo y claro del registro y consulta de asistencias. 
• Desarrollar un módulo de persistencia en archivos CSV, garantizando el 
almacenamiento seguro y la recuperación de la información. 
• Incorporar la exportación de reportes en formatos CSV y PDF, facilitando el 
análisis y la presentación de resultados. 
• Aplicar una arquitectura modular con programación orientada a objetos, separando 
interfaz, lógica de negocio y persistencia para mejorar la organización y el 
mantenimiento del sistema. 
• Asegurar el cumplimiento de los requerimientos funcionales y buenas prácticas de 
calidad de software, para lograr un sistema confiable y eficiente. 

Características
Funcionalidades Principales
- Registro de Asistencia: Marcar estudiantes como Presente, Ausente o Tarde

- Gestión de Estudiantes: Carga masiva desde archivos CSV

- Consultas Flexibles: Búsqueda por fecha o por estudiante específico

- Reportes Automáticos: Generación de porcentajes de asistencia

- Alertas Inteligentes: Notificaciones para estudiantes con baja asistencia

- Exportación de Datos: Reportes exportables en formato CSV

- Respaldo de BD: Funcionalidad de backup de la base de datos

Características Técnicas
Interfaz: Tkinter con estilos personalizados

Base de Datos: SQLite 

Estructura: Programación Orientada a Objetos (POO)

Módulos: Separación clara de responsabilidades

Validaciones: Manejo robusto de errores y excepciones

🛠️ Instalación y Configuración
Prerrequisitos
Python 3.8 o superior

Módulos estándar de Python (tkinter, sqlite3, csv, datetime)

Instalación
Clonar el repositorio:

bash
git clone [url-del-repositorio]
cd asistencia-estudiantil
Ejecutar la aplicación:

bash
python main.py
Estructura del Proyecto
text
asistencia-estudiantil/
│
├── main.py                 
├── asistencia.db           
│
├── modelos/               
│   ├── __init__.py
│   ├── estudiante.py      
│   └── asistencia.py       
│
├── servicios/              
│   ├── __init__.py
│   ├── database.py         
│   └── reporters.py        
│
├── ui/                    
│   ├── __init__.py
│   └── main_window.py      
│
├── data/                   
│   ├── estudiantes.csv     
│   └── asistencias.json

    
Uso de la Aplicación
1. Carga Inicial de Estudiantes
Navegar a la pestaña "Cargar Base de Datos"

Seleccionar archivo CSV con formato: id_estudiante,nombre,apellido

Ver vista previa y confirmar carga

2. Registro Diario de Asistencia
En pestaña "Registrar Asistencia"

Seleccionar fecha (o usar "Hoy" para fecha actual)

Marcar estados (Presente/Ausente/Tarde) para cada estudiante

Aplicar en lote o individualmente

Guardar cambios en base de datos

3. Consulta de Asistencias
En pestaña "Consultar Asistencia"

Filtrar por fecha específica o por estudiante

Visualizar historial completo

4. Generación de Reportes
En pestaña "Reportes y Estadísticas"

Generar reporte general de asistencia

Ver alertas de baja asistencia (<70%)

Exportar reportes a CSV

Formatos de Archivo
Estructura CSV para Estudiantes
csv
id_estudiante,nombre,apellido
E001,Juan,Pérez
E002,María,García
E003,Carlos,López
Base de Datos
Tabla estudiantes: id_estudiante(PK), nombre, apellido

Tabla asistencias: id(PK), id_estudiante(FK), fecha, estado

Interfaz de Usuario
La interfaz cuenta con:

Diseño moderno con paleta de colores profesional

Pestañas organizadas para diferentes funcionalidades

Iconos intuitivos para mejor experiencia de usuario

Vistas previas antes de acciones críticas

Confirmaciones para operaciones importantes

Desarrollo
Tecnologías Utilizadas
Lenguaje: Python 3.x

GUI: Tkinter con ttk widgets

Base de Datos: SQLite3

Persistencia: Archivos CSV y JSON

Patrones de Diseño
MVC (Modelo-Vista-Controlador)

DAO (Data Access Object)

Separación de responsabilidades

Estado del Proyecto
COMPLETADO - Todas las funcionalidades requeridas implementadas

Requerimientos Cumplidos
Interfaz gráfica con Tkinter

Persistencia en base de datos SQLite

Carga de estudiantes desde CSV

Registro de asistencia por fecha

Consultas por estudiante y fecha

Generación de reportes con porcentajes

Exportación a CSV

Alertas de baja asistencia

Contribución:
Equipo de Desarrollo
Carlos Andres Cordoba Araujo
Cristian Felipe Ruiz Arias
María del Mar Luna Castañeda
Julián Alejandro Agudelo Bedoya

Proceso de Contribución
Fork del proyecto

Crear rama de feature (git checkout -b feature/nuevaFuncionalidad)

Commit de cambios (git commit -m 'Agregar nueva funcionalidad')

Push a la rama (git push origin feature/nuevaFuncionalidad)

Crear Pull Request
Contactar al equipo de desarrollo

Desarrollado como parte del Curso de Lenguajes de Programación 🎓
