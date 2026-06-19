# CapCup Backend — Tareas pendientes

Estado actual: API en FastAPI que sube video/audio, lo guarda en disco local y transcribe el audio con faster-whisper, devolviendo segmentos con timestamps.

## Prioridad alta

- [ ] **Procesamiento asincrono / background jobs**: `transcribe` corre sincrono dentro del request. Con videos largos esto bloquea el worker y puede dar timeout. Mover a una cola (Celery, RQ, o BackgroundTasks de FastAPI + polling de estado).
- [ ] **Persistencia real**: hoy los videos y transcripciones viven en `storage/` sin base de datos. Si el proceso se reinicia se pierde el mapeo. Agregar una DB (SQLite para empezar, Postgres a futuro) con tabla de videos/transcripciones/estado.
- [ ] **Limites de tamano de archivo**: no hay validacion de tamano maximo en `/videos/upload`. Agregar limite (ej. 500MB) y devolver 413 si se excede.
- [ ] **Manejo de errores de Whisper**: si el archivo esta corrupto o sin audio, `transcribe_audio` puede fallar sin un mensaje claro al frontend. Envolver en try/except y devolver 422 con detalle.
- [ ] **Limpieza de archivos**: no hay job que borre videos viejos de `storage/`. Definir politica de retencion (ej. borrar despues de 24h) con un cron o background task.

## Prioridad media

- [ ] **Exportar video con subtitulos quemados**: endpoint nuevo `POST /videos/{id}/export` que use ffmpeg para renderizar el video final con los subtitulos superpuestos (estilo CapCut), devolviendo un archivo descargable.
- [ ] **Edicion de transcripcion**: endpoint `PATCH /videos/{id}/transcript` para que el usuario corrija texto/tiempos de un segmento y se persista el cambio.
- [ ] **Deteccion automatica de silencios**: endpoint que devuelva rangos de silencio (usando ffmpeg silencedetect) para soportar "auto-cut" en el frontend.
- [ ] **Soporte multi-idioma explicito**: permitir pasar `language` opcional al transcribir en vez de autodetectar siempre.
- [ ] **Autenticacion basica**: si esto deja de ser solo para QA personal, agregar API key o JWT minimo antes de exponerlo publicamente.

## Prioridad baja / nice-to-have

- [ ] **Webhooks o WebSocket de progreso**: para mostrar progreso real de transcripcion en vez de un spinner generico.
- [ ] **Tests de integracion con archivos reales** (no solo bytes fake) usando un wav corto de fixture.
- [ ] **Dockerfile** para desplegar el backend de forma reproducible (Render, Fly.io, etc).
- [ ] **Rate limiting** basico en `/videos/upload` para evitar abuso si se expone publicamente.

## Deuda tecnica

- [ ] `resolve_video_path` y la logica de glob por video_id asume un solo archivo por id; revisar si hace falta versionado de archivos.
- [ ] CORS actualmente permite `localhost:5173` y dominios `*.app.github.dev` via regex — antes de produccion, restringir al dominio real del frontend desplegado.
