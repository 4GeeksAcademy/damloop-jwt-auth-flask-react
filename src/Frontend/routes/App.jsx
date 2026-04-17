import { BrowserRouter, Routes, Route } from "react-router-dom";

import Signup from "../pages/Signup";
import Login from "../pages/Login";
import Private from "../pages/Private";

import { ProtectedRoute } from "./ProtectedRoute";
import { AuthProvider } from "../context/authContext";
import Navbar from "../components/Navbar";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />

        <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />

          <Route
            path="/private"
            element={
              <ProtectedRoute>
                <Private />
              </ProtectedRoute>
            }
          />

          <Route path="/" element={<h1>Home</h1>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
