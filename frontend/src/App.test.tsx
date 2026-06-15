import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import App from './App'

describe('App', () => {
  it('「/」にアクセスすると書籍一覧画面が表示される', () => {
    render(<App />, { wrapper: MemoryRouter })

    expect(screen.getByRole('heading', { name: '書籍一覧' })).toBeInTheDocument()
  })

  it('「/login」にアクセスするとログイン画面が表示される', () => {
    render(<App />, {
      wrapper: ({ children }) => <MemoryRouter initialEntries={['/login']}>{children}</MemoryRouter>,
    })

    expect(screen.getByRole('heading', { name: 'ログイン' })).toBeInTheDocument()
  })
})
