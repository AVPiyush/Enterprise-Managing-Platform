import { useState } from "react";
import api from "../services/api";

function InvoiceUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async (event) => {
    event.preventDefault();

    if (!file) {
      setError("Please select a PDF invoice.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setError("");

      const response = await api.post(
        "/documents/upload",
        formData
      );

      onUploadSuccess(response.data);
      setFile(null);
      event.target.reset();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Invoice upload failed."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="panel">
      <h2>Upload invoice</h2>
      <p>Upload a PDF invoice (maximum 10 MB).</p>

      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".pdf,application/pdf"
          onChange={(event) => {
            setFile(event.target.files?.[0] || null);
            setError("");
          }}
        />

        {file && <p>Selected: {file.name}</p>}

        <button type="submit" disabled={!file || loading}>
          {loading ? "Uploading..." : "Upload invoice"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
    </section>
  );
}

export default InvoiceUpload;