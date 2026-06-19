# CapCup Backend

API en FastAPI para subir videos y transcribir su audio (speech-to-text) usando `faster-whisper`, como base para un editor de video estilo CapCut.

## Setup

```bash
cd capcup-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `POST /videos/upload` — sube un archivo de video (`multipart/form-data`, campo `file`). Devuelve `video_id`.
- `GET /videos/{video_id}/file` — descarga/streamea el video subido.
- `POST /videos/{video_id}/transcribe` — transcribe el audio del video y devuelve segmentos con texto, `start` y `end`.
- `GET /health` — chequeo de estado.

## Variables de entorno

- `WHISPER_MODEL_SIZE` (default `base`): tamaño del modelo Whisper (`tiny`, `base`, `small`, `medium`, `large-v3`).
- `WHISPER_DEVICE` (default `cpu`): `cpu` o `cuda`.
- `WHISPER_COMPUTE_TYPE` (default `int8`).
