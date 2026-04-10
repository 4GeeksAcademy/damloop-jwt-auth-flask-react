// Utiliza sessionStorage para guardar y recuperar tokens
import { Navigate } from "react-router-dom";

documentation: // Mejora para almacenar token en storage local
export function ProtectedRoute({ children }) {
  const token = sessionStorage.getItem("token");

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}