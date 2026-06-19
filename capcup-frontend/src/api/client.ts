const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export interface TranscriptSegment {
  start: number
  end: number
  text: string
}

export interface TranscriptResponse {
  video_id: string
  language: string
  segments: TranscriptSegment[]
}

export interface UploadResponse {
  video_id: string
  filename: string
}

export async function uploadVideo(file: File): Promise<UploadResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`${API_BASE_URL}/videos/upload`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) {
    throw new Error(`Error al subir el video: ${res.status}`)
  }
  return res.json()
}

export async function transcribeVideo(videoId: string): Promise<TranscriptResponse> {
  const res = await fetch(`${API_BASE_URL}/videos/${videoId}/transcribe`, {
    method: 'POST',
  })
  if (!res.ok) {
    throw new Error(`Error al transcribir el video: ${res.status}`)
  }
  return res.json()
}

export function videoFileUrl(videoId: string): string {
  return `${API_BASE_URL}/videos/${videoId}/file`
}
