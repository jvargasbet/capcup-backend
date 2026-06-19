import { render, screen, fireEvent } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import SubtitleTimeline from './SubtitleTimeline'

const segments = [
  { start: 0, end: 1.5, text: 'Hola a todos' },
  { start: 1.5, end: 3, text: 'bienvenidos al editor' },
]

describe('SubtitleTimeline', () => {
  it('shows an empty state when there are no segments', () => {
    render(<SubtitleTimeline segments={[]} currentTime={0} onSeek={() => {}} />)
    expect(screen.getByText(/Aun no hay transcripcion/i)).toBeInTheDocument()
  })

  it('renders every segment with its text', () => {
    render(<SubtitleTimeline segments={segments} currentTime={0} onSeek={() => {}} />)
    expect(screen.getByText('Hola a todos')).toBeInTheDocument()
    expect(screen.getByText('bienvenidos al editor')).toBeInTheDocument()
  })

  it('marks the segment matching currentTime as active', () => {
    render(<SubtitleTimeline segments={segments} currentTime={2} onSeek={() => {}} />)
    const activeItem = screen.getByText('bienvenidos al editor').closest('li')
    expect(activeItem).toHaveClass('active')
  })

  it('calls onSeek with the segment start time when clicked', () => {
    const onSeek = vi.fn()
    render(<SubtitleTimeline segments={segments} currentTime={0} onSeek={onSeek} />)
    fireEvent.click(screen.getByText('bienvenidos al editor'))
    expect(onSeek).toHaveBeenCalledWith(1.5)
  })
})
