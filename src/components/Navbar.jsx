import { Link, NavLink } from "react-router-dom";

const Navbar = () => {
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
      </div>
    </nav>
  );
};

export default Navbar;
