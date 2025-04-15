import React, { useState } from "react";
import axios from "axios";
import { Box, Typography, Button, CircularProgress, Alert } from "@mui/material";

const AnalyzePage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [graphUrl, setGraphUrl] = useState<string>("");
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
      const [analyzeResponse, graphResponse] = await Promise.all([
        axios.post("http://localhost:8000/analyze/", formData),
        axios.post("http://localhost:8000/graph/", formData)
      ]);
      setResult(analyzeResponse.data);
      setGraphUrl("http://localhost:8000/static/relationship_graph.html");
    } catch (err) {
      console.error("Analyze failed", err);
      setError("Failed to analyze document.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>Upload & Analyze Document</Typography>
      <input type="file" onChange={handleFileChange} />
      <Button variant="contained" color="success" sx={{ mt: 2 }} onClick={handleUpload}>
        Upload & Analyze
      </Button>
      {loading && <Box mt={2}><CircularProgress color="success" /></Box>}
      {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      {result && (
        <Box mt={4} p={2} border={1} borderColor="grey.300" borderRadius={2}>
          <Typography variant="h6">Summary:</Typography>
          <Typography paragraph>{result.summary}</Typography>
          <Typography variant="h6">Entities:</Typography>
          <ul>
            {result.entities.map((ent: any, idx: number) => (
              <li key={idx}><strong>{ent.label}</strong>: {ent.text}</li>
            ))}
          </ul>
        </Box>
      )}
      {graphUrl && (
        <Box mt={4}>
          <Typography variant="h6">Entity Relationship Graph:</Typography>
          <iframe src={graphUrl} title="Entity Graph" style={{ width: "100%", height: "500px", border: "1px solid #ccc" }} />
        </Box>
      )}
    </Box>
  );
};

export default AnalyzePage;