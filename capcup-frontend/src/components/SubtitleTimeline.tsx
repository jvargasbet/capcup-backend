import type { TranscriptSegment } from '../api/client'

interface SubtitleTimelineProps {
  segments: TranscriptSegment[]
  currentTime: number
  onSeek: (time: number) => void
}

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60)
  const s = Math.floor(seconds % 60)
  return `${m}:${s.toString().padStart(2, '0')}`
}

export default function SubtitleTimeline({ segments, currentTime, onSeek }: SubtitleTimelineProps) {
  if (segments.length === 0) {
    return <p className="subtitle-empty">Aun no hay transcripcion. Sube un video y transcribelo.</p>
  }

  return (
    <ul className="subtitle-list">
      {segments.map((segment, index) => {
        const isActive = currentTime >= segment.start && currentTime < segment.end
        return (
          <li
            key={`${segment.start}-${index}`}
            className={isActive ? 'subtitle-item active' : 'subtitle-item'}
            onClick={() => onSeek(segment.start)}
          >
            <span className="subtitle-time">
              {formatTime(segment.start)} - {formatTime(segment.end)}
            </span>
            <span className="subtitle-text">{segment.text}</span>
          </li>
        )
      })}
    </ul>
  )
}
