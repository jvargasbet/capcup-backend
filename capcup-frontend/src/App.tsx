import { useRef, useState } from 'react'
import './App.css'
import { transcribeVideo, uploadVideo, videoFileUrl } from './api/client'
import type { TranscriptSegment } from './api/client'
import SubtitleTimeline from './components/SubtitleTimeline'
import CaptionOverlay from './components/CaptionOverlay'

type Status = 'idle' | 'uploading' | 'transcribing' | 'ready' | 'error'

function App() {
  const [videoId, setVideoId] = useState<string | null>(null)
  const [segments, setSegments] = useState<TranscriptSegment[]>([])
  const [status, setStatus] = useState<Status>('idle')
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [currentTime, setCurrentTime] = useState(0)
  const videoRef = useRef<HTMLVideoElement>(null)

  async function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]
    if (!file) return

    setErrorMessage(null)
    setSegments([])
    setStatus('uploading')

    try {
      const upload = await uploadVideo(file)
      setVideoId(upload.video_id)
      setStatus('transcribing')

      const transcript = await transcribeVideo(upload.video_id)
      setSegments(transcript.segments)
      setStatus('ready')
    } catch (error) {
      setStatus('error')
      setErrorMessage(error instanceof Error ? error.message : 'Error desconocido')
    }
  }

  function handleSeek(time: number) {
    if (videoRef.current) {
      videoRef.current.currentTime = time
      videoRef.current.play()
    }
  }

  return (
    <div className="editor-layout">
      <header className="editor-header">
        <h1>CapCup</h1>
        <p>Editor de video con deteccion de audio y subtitulos automaticos</p>
      </header>

      <main className="editor-main">
        <section className="preview-panel">
          <label className="upload-button">
            Subir video
            <input type="file" accept="video/*" onChange={handleFileChange} hidden />
          </label>

          {status === 'uploading' && <p className="status-msg">Subiendo video...</p>}
          {status === 'transcribing' && <p className="status-msg">Transcribiendo audio...</p>}
          {status === 'error' && <p className="status-msg error">{errorMessage}</p>}

          {videoId && (
            <div className="video-stage">
              <video
                ref={videoRef}
                className="video-preview"
                src={videoFileUrl(videoId)}
                controls
                onTimeUpdate={(e) => setCurrentTime(e.currentTarget.currentTime)}
              />
              <CaptionOverlay segments={segments} currentTime={currentTime} />
            </div>
          )}
        </section>

        <section className="subtitle-panel">
          <h2>Transcripcion</h2>
          <SubtitleTimeline segments={segments} currentTime={currentTime} onSeek={handleSeek} />
        </section>
      </main>
    </div>
  )
}

export default App
