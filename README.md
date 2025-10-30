# Practica: Fiesta Meter — Flask + Gunicorn + Nginx

## Objetivo

Publicar la aplicacion Flask "Fiesta Meter" (votos humoristicos entre nombres ficticios) detras de Nginx. La app debe ejecutarse con Gunicorn como servidor de aplicaciones. Se trabaja con 2 contenedores y 1 red Docker creada manualmente.

## Material entregado

```
fiesta-meter/
├─ app/
│  ├─ app.py
│  ├─ wsgi.py
│  └─ requirements.txt
└─ templates/
   └─ index.html
```

No se entrega Dockerfile ni configuracion de Nginx. Eso se construye en los pasos 1 a 6.

## Tareas (sigue exactamente los pasos 1 a 6)

1. **Crear el Dockerfile de la aplicacion (Gunicorn)**
   - Base: `python:3.14.0-alpine3.22`
   - Directorio de trabajo: /app
   - Instala dependencias desde `requirements.txt` sin cache
   - Copia el codigo al contenedor
   - Publicalo en el puerto 8000
   - `CMD` debe arrancar Gunicorn en `0.0.0.0:8000` con `wsgi:app`

   Pista de comando final: `gunicorn -b 0.0.0.0:8000 wsgi:app`

2. **Construir la imagen de la app**

   Desde la carpeta `app/`:

   Construye una imagen llamada: viaje-estudios

3. **Crear la red Docker compartida**

   Crea una red docker compartida llamada webnet

4. **Ejecutar la app en esa red**

   Adicionalmente:
   docker logs fiesta_app    # Verifica Gunicorn escuchando en 0.0.0.0:8000

5. **Configurar Nginx como reverse proxy**

   - Crea `nginx/default.conf` con un servidor que escuche en `80`, use `server_name app.localhost;` y haga proxy de `/` a `http://fiesta_app:8000`.
   - Asegura las cabeceras `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`.

   ```bash
   docker run -d --name nginx_proxy \
     --network webnet \
     -p 8080:80 \
     -v ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro \
     nginx:1.27-alpine
   ```

6. **Probar**

   - Abre `http://localhost:8080/` y realiza votos.
   - Comprueba `http://localhost:8080/health` para obtener `{"status":"ok"}`.

## Entrega

- Lista de comandos utilizados en cada paso (1 a 6) en `README.md`.
- Captura de pantalla de la app en `http://localhost:8080/`.
- Explicacion breve (3 a 5 lineas) sobre por que Flask no se expone directamente y que aporta Nginx como reverse proxy.

## Criterios de evaluacion (10 puntos)

- Dockerfile + Gunicorn correctos (3 pt)
- Red Docker y ejecucion (2 pt)
- Reverse proxy funcional (3 pt)
- README + captura + explicacion (2 pt)

### Bonus (hasta +2)

- Dos cabeceras de seguridad (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, etc).

## FAQ rapidas

- **502 Bad Gateway**: revisa que el contenedor se llame `fiesta_app`, que ambos esten en `webnet` y que Nginx apunte a `http://fiesta_app:8000`.
- **No carga en 8080**: verifica que expongas `-p 8080:80` en Nginx (no en la app).
- **Funciona local pero no en Docker**: Gunicorn debe escuchar en `0.0.0.0` (no `127.0.0.1`).

Recuerda: el navegador nunca habla con Flask directamente. Siempre entra por Nginx, que reenvia a Gunicorn y luego Flask.
