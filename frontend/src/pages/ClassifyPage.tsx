import React, { useState } from "react";
import axios from "axios";
import { Button, TextField, CircularProgress, Alert, Typography, Box } from "@mui/material";

const ClassifyPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [query, setQuery] = useState<string>("");
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] || null);
  };

  const handleUploadAndQuery = async () => {
    if (!file || !query) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post("http://localhost:8000/classify-query/?query=" + encodeURIComponent(query), formData);
      setResult((response.data as { answer: string }).answer);
    } catch (err) {
      console.error("Classification query failed", err);
      setError("Failed to get classification response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>Classify with Natural Language</Typography>
      <input type="file" onChange={handleFileChange} />
      <TextField fullWidth label="Ask a question about the document" variant="outlined" value={query} onChange={(e) => setQuery(e.target.value)} sx={{ my: 2 }} />
      <Button variant="contained" color="secondary" onClick={handleUploadAndQuery}>Ask & Classify</Button>
      {loading && <Box mt={2}><CircularProgress color="secondary" /></Box>}
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {result && (
        <Box mt={4} p={2} border={1} borderColor="grey.300" borderRadius={2}>
          <Typography variant="h6">Answer:</Typography>
          <Typography>{result}</Typography>
        </Box>
      )}
    </Box>
  );
};

export default ClassifyPage;