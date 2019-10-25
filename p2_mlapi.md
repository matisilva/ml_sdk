# Despliegue de sistemas predictivos - Práctico 2
> Diplodatos 2019

En esta segunda iteración, vamos a continuar trabajando en nuestra API para predicción de sentimientos en oraciones, profundizando e implementando lo siguiente:

1. Testing de stress con *Locust*
2. Monitoreo con *EKL*
3. Scaling de servicios
4. Obtener y almacenar feedback de usuarios

## 1. Testing de stress con *Locust*

Para esta tarea deberá crear una nueva carpeta en el proyecto, llamada `stress_test`, en la cual colocará los archivos `.py` de Locust.

- Cree al menos un test de uso del endpoint `predict` de nuestra API para evaluar su comportamiento frente a un gran número de usuarios.

- Detalle en un reporte las especificaciones de hardware del servidor donde está desplegado su servicio y compare los resultados obtenidos para diferentes números de usuarios. Algunos puntos que puede tener en cuenta son:

## 2. Monitoreo con *EKL*

TODO

## 3. Scaling de servicios

TODO - supongo que hay que cambiar algo en docker-compose.yml

## 4. Obtener y almacenar feedback de usuarios

(Puede ser ejercicio opcional, será muy difícil de hacer? Mi idea es poner dos botones onda pulgar para arriba o abajo, que vos puedas clickear si te pareció bien o mal la predicción. Esto habría que almacenarlo en un csv ponele para luego tener una lista de las oraciones en la cual la api falló.)
