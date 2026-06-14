import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('「Book Shelf」というタイトルが表示される', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: 'Book Shelf' })).toBeInTheDocument()
  })
})
