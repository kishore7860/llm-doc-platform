import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { TextField, Button, Typography, Box, Alert } from "@mui/material";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogin = async () => {
    setError(null);
    try {
      const response = await axios.post("http://localhost:8000/login", { username, password });
      localStorage.setItem("token", (response.data as { access_token: string }).access_token);
      navigate("/upload");
    } catch (err) {
      console.error("Login failed", err);
      setError("Invalid username or password");
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>Login</Typography>
      <TextField fullWidth label="Username" value={username} onChange={(e) => setUsername(e.target.value)} sx={{ mb: 2 }} />
      <TextField fullWidth label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} sx={{ mb: 2 }} />
      <Button variant="contained" onClick={handleLogin}>Login</Button>
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
    </Box>
  );
};

export default LoginPage;