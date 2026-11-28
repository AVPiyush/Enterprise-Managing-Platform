import { useState } from "react";
import InvoiceUpload from "./components/InvoiceUpload";
import InvoiceProcessor from "./components/InvoiceProcessor";
import "./App.css";

function App() {
  const [document, setDocument] = useState(null);
  const [result, setResult] = useState(null);

  const handleUploadSuccess = (data) => {
    setDocument(data);
    setResult(null);
  };

  return (
    <main className="dashboard">
      <header className="header">
        <div>
          <h1>Enterprise Agent Platform</h1>
          <p>Accounts Payable Automation</p>
        </div>
        <span className="environment">DEVELOPMENT</span>
      </header>

      <section className="welcome">
        <h2>Invoice Verification Dashboard</h2>
        <p>
          Upload invoices, extract financial information,
          and verify them against purchase orders.
        </p>
      </section>

      <InvoiceUpload onUploadSuccess={handleUploadSuccess} />

      {document && (
        <>
          <section className="panel">
            <h2>Uploaded document</h2>
            <p><strong>Filename:</strong> {document.filename}</p>
            <p><strong>Document ID:</strong> {document.id}</p>
            <p>
              <strong>Extraction status:</strong>{" "}
              {document.extraction_status}
            </p>
            <p>
              <strong>Extracted characters:</strong>{" "}
              {document.extracted_characters}
            </p>
          </section>

          <InvoiceProcessor
            documentId={document.id}
            onProcessSuccess={setResult}
          />
        </>
      )}

      {result && (
        <section className="panel results">
          <h2>Verification results</h2>

          <div
            className={`status ${
              result.verification_status === "matched"
                ? "success"
                : "exception"
            }`}
          >
            {result.verification_status?.toUpperCase()}
          </div>

          <h3>Extracted invoice details</h3>
          <pre>{JSON.stringify(result.invoice_data, null, 2)}</pre>

          <h3>Purchase order</h3>
          <pre>
            {JSON.stringify(result.purchase_order, null, 2)}
          </pre>

          <h3>Discrepancies</h3>
          {result.discrepancies?.length > 0 ? (
            <ul>
              {result.discrepancies.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          ) : (
            <p>No discrepancies found.</p>
          )}

          <h3>AI exception explanation</h3>
          <p>{result.exception_explanation}</p>
        </section>
      )}

      <footer>
        Enterprise Agent Platform · Accounts Payable
      </footer>
    </main>
  );
}

export default App;