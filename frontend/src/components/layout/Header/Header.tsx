import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../../../contexts/AuthContext'

export function Header() {
  const { logout } = useAuth()

  return (
    <header className="border-b border-gray-200 bg-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-8">
            <Link to="/" className="text-xl font-bold text-gray-900">
              Book Shelf
            </Link>
            <nav className="flex gap-6">
              <NavLink
                to="/"
                end
                className={({ isActive }) =>
                  isActive
                    ? 'text-sm font-medium text-blue-600'
                    : 'text-sm text-gray-600 hover:text-gray-900'
                }
              >
                書籍一覧
              </NavLink>
              <NavLink
                to="/tags"
                className={({ isActive }) =>
                  isActive
                    ? 'text-sm font-medium text-blue-600'
                    : 'text-sm text-gray-600 hover:text-gray-900'
                }
              >
                タグ管理
              </NavLink>
            </nav>
          </div>
          <button
            type="button"
            onClick={logout}
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            ログアウト
          </button>
        </div>
      </div>
    </header>
  )
}
