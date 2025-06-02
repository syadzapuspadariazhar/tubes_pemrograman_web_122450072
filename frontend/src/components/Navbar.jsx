import { Link, NavLink } from "react-router-dom";
import { useContext, useState } from "react";
import { AuthContext } from "../contexts/AuthContext";

const Navbar = () => {
  const { user, logout, isAuthenticated } = useContext(AuthContext);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleLogout = () => {
    logout();
    setShowUserMenu(false);
  };

  // Don't render navbar if not authenticated
  if (!isAuthenticated) {
    return null;
  }

  return (
    <nav className="bg-pink-500 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <Link to="/" className="flex items-center space-x-2 text-2xl font-bold tracking-wide">
          <img
            src="/logo.png"
            alt="Logo"
            className="w-8 h-8 rounded-full object-cover"
          />
          <span>BudgetTracker</span>
        </Link>

        <div className="flex items-center space-x-6">
          {/* Navigation Links */}
          <div className="flex space-x-6 text-base">
            <NavLink
              to="/"
              className={({ isActive }) =>
                isActive
                  ? "font-semibold text-yellow-200 border-b-2 border-yellow-200 pb-1"
                  : "hover:text-yellow-100 transition"
              }
            >
              Dashboard
            </NavLink>
            <NavLink
              to="/transactions"
              className={({ isActive }) =>
                isActive
                  ? "font-semibold text-yellow-200 border-b-2 border-yellow-200 pb-1"
                  : "hover:text-yellow-100 transition"
              }
            >
              Transactions
            </NavLink>
            <NavLink
              to="/categories"
              className={({ isActive }) =>
                isActive
                  ? "font-semibold text-yellow-200 border-b-2 border-yellow-200 pb-1"
                  : "hover:text-yellow-100 transition"
              }
            >
              Categories
            </NavLink>
          </div>

          {/* User Menu */}
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-2 bg-pink-600 hover:bg-pink-700 px-4 py-2 rounded-lg transition-colors"
            >
              <div className="w-8 h-8 bg-white text-pink-500 rounded-full flex items-center justify-center font-bold">
                {user?.username?.charAt(0).toUpperCase() || 'U'}
              </div>
              <span className="hidden md:block">{user?.username || 'User'}</span>
              <svg 
                className={`w-4 h-4 transition-transform ${showUserMenu ? 'rotate-180' : ''}`} 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {/* Dropdown Menu */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 z-50">
                <div className="px-4 py-2 text-gray-700 border-b">
                  <div className="font-medium">{user?.username || 'User'}</div>
                  <div className="text-sm text-gray-500">{user?.email || 'Budget Tracker'}</div>
                </div>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 flex items-center space-x-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                  <span>Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
