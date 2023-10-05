# Proyecto Fundamentos de Testing y aseguramiento de calidad
grupo 4

### Requisitos previos:
Se debe tener instalado o instalar postgresql.

Se recomienda crear y ejecutar todo el código en un ambiente virtual, este se puede crear con:
<br>
```python venv .venv```
<br>
Luego se activa el ambiente virtual con el comando:
<br>
```.\.venv\Scrips\activate```

### Instalación de dependencias
Para instalar las dependencias se utiliza el comando:
<br>
```pip install -r requirements.txt```

### Ejecutar el software
Con los requisitos anteriores, ahora solo basta con ejecutar el siguiente comando:
<br>
```python manage.py runserver```
<br>
Esto iniciará el servidor y en la consola de comandos se mostrará la URL de donde está el servidor.

### Ejecutar los tests
Basta con ejecutar el comando:
```python manage.py test```
<br>
Notar que no es necesario tener el servidor funcionando para realizar los tests, tampoco tener datos en la base de datos ya que estos se crean y borran al hacer los tests.
