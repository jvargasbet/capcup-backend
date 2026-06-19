import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import App from './App'
import * as api from './api/client'

describe('App', () => {
  it('uploads a video, transcribes it, and shows the detected speech', async () => {
    vi.spyOn(api, 'uploadVideo').mockResolvedValue({ video_id: 'vid123', filename: 'vid123.mp4' })
    vi.spyOn(api, 'transcribeVideo').mockResolvedValue({
      video_id: 'vid123',
      language: 'es',
      segments: [{ start: 0, end: 1.5, text: 'audio detectado correctamente' }],
    })
    vi.spyOn(api, 'videoFileUrl').mockReturnValue('http://localhost:8000/videos/vid123/file')

    render(<App />)

    const file = new File(['fake-bytes'], 'clip.mp4', { type: 'video/mp4' })
    const input = document.querySelector('input[type="file"]') as HTMLInputElement
    await userEvent.upload(input, file)

    await waitFor(() => {
      expect(screen.getByText('audio detectado correctamente')).toBeInTheDocument()
    })

    expect(api.uploadVideo).toHaveBeenCalledWith(file)
    expect(api.transcribeVideo).toHaveBeenCalledWith('vid123')
  })

  it('shows an error message when upload fails', async () => {
    vi.spyOn(api, 'uploadVideo').mockRejectedValue(new Error('Error al subir el video: 400'))

    render(<App />)

    const file = new File(['fake-bytes'], 'clip.mp4', { type: 'video/mp4' })
    const input = document.querySelector('input[type="file"]') as HTMLInputElement
    await userEvent.upload(input, file)

    await waitFor(() => {
      expect(screen.getByText('Error al subir el video: 400')).toBeInTheDocument()
    })
  })
})
