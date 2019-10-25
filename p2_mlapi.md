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

Si bien la propuesta es ElasticSearch Kibana y Logstash para mejor entendimiento usaremos tecnologías similares. En este punto se debera instanciar un stack compuesto de los siguientes servicios:
  - *mongodb*: Para dar soporte de base de datos a graylog en la gestion de usuarios y configuraciones
  - *elasticsearch*: Para el almacenamiento persistente de los datos a ser procesados. En este caso serán logs de salida de los contenedores.
  - *graylog*: Reponsable de la gestión de elasticsearch. Creará nuestros indices rotativos con persistencia configurable y ademas nos permitirá hacer preproceso en la ingestión de datos. Su driver de ingestión de datos nos permitirá conectar la salida de los contenedores de manera nativa. 
  - *grafana*: Herramienta que utilizaremos para la creación de dashboards para visualización. Elegida por su versatilidad y facil entendimiento.

Una vez realizadas las configuraciones iniciales para completar la tarea será necesario enviar los logs al stack instanciado y visualizar dashboards de actividad donde se pueda ver en tiempo real las siguientes estadisticas.

- *req/min* que esta recibiendo nuestra API
- *histograma de actividad* diferenciando cuales dieron respuesta positiva y cuales negativa.
- *alerta de errores* al recibir mas de 10 request con codigo de error (>=400) en un minuto

## 3. Scaling de servicios

El objetivo aqui es duplicar nuestra capacidad de respuesta instanciando un "worker" mas en nuestra infraestructura. Para ello deberíamos aumentar la cantidad de replicas que tenemos del contenedor *model* y monitorear las mejoras en grafana usando nuestro cliente locust para exigir la carga.

## 4. Obtener y almacenar feedback de usuarios
TODO
(Puede ser ejercicio opcional, será muy difícil de hacer? Mi idea es poner dos botones onda pulgar para arriba o abajo, que vos puedas clickear si te pareció bien o mal la predicción. Esto habría que almacenarlo en un csv ponele para luego tener una lista de las oraciones en la cual la api falló.)


## (opcional) 5. Usar traefik como un DNS resolver y descubrir sus features
Entre las muchas funcionalidades que traefik tiene integradas podemos encontrar un balanceador de carga con resoluciones DNS. La idea de este punto es poder utilizar traefik y descubrir sus funcionalidades integrandolo en nuestro proyecto de manera tal que podamos enviar una peticion a nuestra API llamando al endpoint http://my.own.api y obtener un balanceo entre 2 instancias.
