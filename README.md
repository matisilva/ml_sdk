# Despliegue de sistemas predictivos
> Diplodatos 2019

## Instalar y ejecutar

```
$ docker-compose up --build -d
```

Para detener los servicios:

```
$ docker-compose down
```

## Tests

### Integración

Necesitas tener instalado *requests* (`pip install requests>=2.22.0`).

`$ python3 tests/test_integration.py`

### API

`$ docker-compose exec api python3 tests/test_api.py`

### Model

`$ docker-compose exec model python3 tests/test_model.py`
