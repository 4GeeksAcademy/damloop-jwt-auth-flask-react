import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

const API_URL = "https://solid-computing-machine-wwrr99v45ppc5g9w-5000.app.github.dev/api";

export function AuthProvider({ children }) {
  const [token, setToken] = useState(sessionStorage.getItem("token") || null);

  // -----------------------------
  // LOGIN
  // -----------------------------
  const login = async (email, password) => {
    try {
      const resp = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await resp.json();

      if (!resp.ok) {
        throw new Error(data.msg || "Credenciales inválidas");
      }

      sessionStorage.setItem("token", data.token);
      setToken(data.token);
      return { success: true };

    } catch (error) {
      return { success: false, message: error.message };
    }
  };

  // -----------------------------
  // SIGNUP
  // -----------------------------
  const signup = async (email, password) => {
    try {
      const resp = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await resp.json();

      if (!resp.ok) {
        throw new Error(data.msg || "Error al registrar");
      }

      return { success: true };

    } catch (error) {
      return { success: false, message: error.message };
    }
  };

  const logout = () => {
    sessionStorage.removeItem("token");
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        isAuthenticated: !!token,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
