# survey
Aplicación para realizar consultas de forma que se mantenga el anonimato de los participantes, se controle los votos realizados y se provea de la trazabilidad necesaria para poder auditar todo el proceso.

# Features
- Autenticacion mediante ldap 
- Formulario de enquesta
- Anonimizado de votos
- Consulta de votos
- Descada de los datos

# Todo
- Interfaz para la creación de las encuestas.

# Instalación 
## Servidor físico 
Instalamos los requisitos de python. 
```bash 
pip install –r requirements.txt 
```
# Variables de entorno 


```text 
| Variable                                     | Descripción                                                 | 
|---------------------------------------------|̣̣̣--------------------------------------------------------------|
|FLASK_DATABASE_HOST= MYSQL HOST              | IP de la base de datos mysql.                                |
|FLASK_DATABASE_USER= MYSQL USER              | Usuario de la base de datos mysql.                           |
|FLASK_DATABASE_PASSWORD= MYSQL PASSWORD      | Contraseña de la base de datos mysql.                        |
|FLASK_DATABASE= DATABASE                     | Nombre de la base de datos mysql.                            |
|FLASK_SECRET_KEY=YOUERSECRET                 | Secreto para las sesiones http (valor aleatorio).            |
|FLASK_LDAP_SERVER="localhost"                | Ip del servidor ldap                                         |
|FLASK_LDAP_ROOT_DN="dc=example,dc=org"       | DN del grupo de ldap                                         |
|FLASK_LDAP_USER="cn=admin,dc=example,dc=org" | Usuario para leer el ldap                                    |
|FLASK_LDAP_PASSWORD=admin                    | Contraseña del usuario lpad                                  |
|FLASK_LDAP_ATTRIBUTE=sAMAccountName          | Atributo para identificar el usuario                         |
|----------------------------------------------------------------------------------------------------------
```


Iniciamos la base de datos con el comando: 

```bash 
flask init-db 
```
Este comando creara las tablas en la base de dados indicada en las variables de entorno y creará las credenciales por defecto (usuario: admin, contraseña: password) 
Se recomienda crear un nuevo usurio e eliminar el existente durante el primer acceso. 
Una vez inicializada la base de datos podemos iniciar el servidor:+ 
```bash 
gunicorn –w 4 –b 0.0.0.0:8000 app:create_app() 
```
Una vez iniciado podemos acceder a la url del servidor. 
http://localhost:8000 

## Docker 
La imagen para docker esta disponible en docker hub https://hub.docker.com/r/lliwi/survey.
En este repositorio se proporciona el fichero Dockerfile para poder generar la imagen en local y actualizar la visión de python. 
Se proporciona también el fichero docker-compose.yaml de ejemplo para poder iniciar el servicio mysql para pruebas, adminier, para la gestión de la mase de datos mysql (eliminarlo en servidores de producción) y el servicio web rvisitas. 
Para iniciarlo lo podemos realizar ejecutando: 
```bash 
docker-compose –f docker-compose.yaml up –d 
```
Crear la base de datos de adminier http://localhost:8080 
Ejecutaremos el siguiente comando para iniciar la base de datos: 
```bash 
docker exec -t CONTAINER_NAME flask init-db 
```
Una vez iniciado podemos acceder a la url del servidor. 
http://localhost:8000 
Iniciamos la base de datos con el comando: 
```bash 
flask init-db 
```
Este comando creara las tablas en la base de dados indicada en las variables de entorno. 

Una vez inicializada la base de datos podemos iniciar el servidor:
```bash 
gunicorn –w 4 –b 0.0.0.0:8000 app:create_app() 
```
Una vez iniciado podemos acceder a la url del servidor. 
http://localhost:8000 
