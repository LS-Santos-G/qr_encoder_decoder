# Codificador y Decodificador de Códigos QR

**Asignatura:** Teoría de Códigos

**Institución:** Universidad del Norte

**Integrantes:** Kevin Cardona, Luna Santos, David Alvarez, Maria Camila Tamara

## Descripción del Proyecto

Aplicativo desarrollado en python que codifica y decodifica códigos qr version 1 para niveles L, M, Q y H de corrección,
aplicando conceptos de teoría de códigos y mecanismos de corrección de errores.

## Funcionalidades

- Codificación de mensajes Qr
- Selección de nivel de corrección (L, M, Q, H)
- Visualización de la matriz Qr generada
- Decodificación de códigos Qr aun con error en el canal

## Instrucciones de Ejecución

**Requisitos:** python 3 y las dependencias indicadas en *requirements.txt*
Luego desde la carpeta del aplicativo, ejecutar:

```terminal
python -m pip install -r requirements.txt

python main.py
```

## Resultados Principales

El aplicativo es capaz de generar qrs y decodificar qrs con error de canal

## Herramientas Utilizadas

**Python:** Lenguaje de programacion
**CustomTkinter:** Principal libreria para la interfaz grafica
**NumPy:** Manejo de matrices
**Matplotlib:** Graficas de los Qr


