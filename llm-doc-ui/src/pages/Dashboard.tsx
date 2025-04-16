import { useState } from "react";
import axios from "../api/axiosInstance";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { UploadCloud } from "lucide-react";

const Dashboard = () => {
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState("");
  const [entities, setEntities] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0] || null;
    setFile(uploadedFile);
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("/analyze/", formData);
      setSummary(response.data.summary);
      setEntities(response.data.entities);
    } catch (err) {
      alert("Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white px-8 py-10">
      <div className="max-w-5xl mx-auto space-y-8">
        <header className="space-y-2">
          <h1 className="text-3xl font-bold text-teal-700">📄 Document Analyzer</h1>
          <p className="text-gray-600 text-sm">Upload any PDF, Word doc, or text file and extract key insights instantly.</p>
        </header>

        <Card className="p-6 space-y-4 border border-gray-200 shadow-md">
          <div className="flex flex-col sm:flex-row sm:items-center gap-4">
            <Input type="file" onChange={handleFileChange} className="w-full" />
            <Button onClick={handleSubmit} disabled={loading} className="bg-teal-600 hover:bg-teal-700">
              {loading ? "Analyzing..." : "Analyze Document"}
            </Button>
          </div>
        </Card>

        {summary && (
          <Card className="p-6 shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold mb-2">📝 Summary</h2>
            <p className="text-gray-700 leading-relaxed">{summary}</p>
          </Card>
        )}

        {entities.length > 0 && (
          <Card className="p-6 shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold mb-4">🔍 Extracted Entities</h2>
            <div className="flex flex-wrap gap-2">
              {entities.map((ent, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 rounded-full bg-teal-100 text-teal-800 text-sm font-medium"
                >
                  {ent.label}: {ent.text}
                </span>
              ))}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Dashboard;