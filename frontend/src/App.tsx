import { Route, Routes } from 'react-router-dom'
import LoginPage from './pages/LoginPage/LoginPage'
import RegisterPage from './pages/RegisterPage/RegisterPage'
import BookListPage from './pages/BookListPage/BookListPage'
import BookCreatePage from './pages/BookCreatePage/BookCreatePage'
import BookEditPage from './pages/BookEditPage/BookEditPage'
import BookDetailPage from './pages/BookDetailPage/BookDetailPage'
import TagManagePage from './pages/TagManagePage/TagManagePage'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/" element={<BookListPage />} />
      <Route path="/books/new" element={<BookCreatePage />} />
      <Route path="/books/:id" element={<BookDetailPage />} />
      <Route path="/books/:id/edit" element={<BookEditPage />} />
      <Route path="/tags" element={<TagManagePage />} />
    </Routes>
  )
}

export default App
