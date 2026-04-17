import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import { useAuth } from "../context/authContext";

const API_URL = "https://solid-computing-machine-wwrr99v45ppc5g9w-5000.app.github.dev/api";

export default function Private() {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { token, logout } = useAuth();

  useEffect(() => {
    if (!token) {
      navigate("/login", { replace: true });
      return;
    }

    fetch(`${API_URL}/private`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(async (res) => {
        if (!res.ok) throw new Error("Token inválido o expirado");
        const data = await res.json();
        setMessage(data.msg);
      })
      .catch((err) => {
        setError(err.message);
        logout();
        navigate("/login", { replace: true });
      });
  }, [token, logout, navigate]);

  return (
    <>
      <Navbar />
      <main className="container py-5">
        <div className="card shadow">
          <div className="card-body">
            <h2 className="h4">Zona privada</h2>

            {message && (
              <p className="mb-0">
                <strong>{message}</strong>
              </p>
            )}

            {error && <div className="alert alert-danger mt-3">{error}</div>}
          </div>
        </div>
      </main>
    </>
  );
}
