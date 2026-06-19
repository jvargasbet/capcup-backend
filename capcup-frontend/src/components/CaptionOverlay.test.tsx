import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import CaptionOverlay from './CaptionOverlay'

const segments = [
  { start: 0, end: 2, text: 'hola mundo' },
  { start: 2, end: 4, text: 'capcup es genial' },
]

describe('CaptionOverlay', () => {
  it('renders nothing when no segment is active', () => {
    const { container } = render(<CaptionOverlay segments={segments} currentTime={10} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('renders the active segment words in uppercase', () => {
    render(<CaptionOverlay segments={segments} currentTime={0.1} />)
    expect(screen.getByText('HOLA')).toBeInTheDocument()
    expect(screen.getByText('MUNDO')).toBeInTheDocument()
  })

  it('highlights only the word matching the current playback time', () => {
    render(<CaptionOverlay segments={segments} currentTime={3.5} />)
    expect(screen.getByText('GENIAL')).toHaveClass('highlight')
    expect(screen.getByText('CAPCUP')).not.toHaveClass('highlight')
  })
})
