import React, { useState } from "react";
import axios from "axios";
import { Button, CircularProgress, Alert, Typography, Box } from "@mui/material";

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] || null);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post("http://localhost:8000/classify/", formData);
      setResult(response.data);
    } catch (err) {
      console.error("Upload failed", err);
      setError("Failed to classify document.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>Upload & Classify Document</Typography>
      <input type="file" onChange={handleFileChange} />
      <Button variant="contained" onClick={handleUpload} sx={{ mt: 2 }}>
        Upload & Classify
      </Button>
      {loading && <Box mt={2}><CircularProgress color="primary" /></Box>}
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {result && (
        <Box mt={4} p={2} border={1} borderColor="grey.300" borderRadius={2}>
          <Typography variant="h6">Classification Result:</Typography>
          <Typography><strong>Type:</strong> {result.predicted_type}</Typography>
          <Typography><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</Typography>
        </Box>
      )}
    </Box>
  );
};

export default UploadPage;