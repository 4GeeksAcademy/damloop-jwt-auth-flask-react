import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/authContext";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { signup } = useAuth();

  const handleSignup = async (e) => {
    e.preventDefault();

    const result = await signup(email, password);

    if (!result.success) {
      alert(result.message || "Error en el registro");
      return;
    }

    alert("Usuario creado correctamente");
    navigate("/login");
  };

  return (
    <div className="container mt-5">
      <h2>Crear cuenta</h2>

      <form onSubmit={handleSignup} className="mt-3">
        <div className="mb-3">
          <label>Email</label>
          <input
            type="email"
            className="form-control"
            placeholder="tuemail@correo.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label>Contraseña</label>
          <input
            type="password"
            className="form-control"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button className="btn btn-primary w-100" type="submit">
          Crear cuenta
        </button>
      </form>
    </div>
  );
}
