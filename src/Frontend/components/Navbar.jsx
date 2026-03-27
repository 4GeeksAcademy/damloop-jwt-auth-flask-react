import { Link, NavLink, useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const token = sessionStorage.getItem('token');

  const logout = () => {
    sessionStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary fixed-top border-bottom">
      <div className="container-fluid">
        <Link className="navbar-brand fw-bold" to="/">JWT Demo</Link>

        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav"
                aria-controls="nav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon" />
        </button>

        <div className="collapse navbar-collapse" id="nav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item"><NavLink className="nav-link" to="/">Home</NavLink></li>

            {!token && (
              <>
                <li className="nav-item"><NavLink className="nav-link" to="/signup">Signup</NavLink></li>
                <li className="nav-item"><NavLink className="nav-link" to="/login">Login</NavLink></li>
              </>
            )}

            {token && (
              <li className="nav-item"><NavLink className="nav-link" to="/private">Private</NavLink></li>
            )}
          </ul>

          {token && (
            <button className="btn btn-outline-danger" onClick={logout}>
              Cerrar sesión
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
