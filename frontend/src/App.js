import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

const API_URL = 'http://127.0.0.1:5000';

function App() {
  const [file, setFile] = useState(null);
  const [arch, setArch] = useState("aarch64");
  const [logs, setLogs] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleArchChange = (e) => {
    setArch(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("arch", arch);

    try {
      const response = await axios.post(`${API_URL}/compile`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.data.success) {
        setLogs(response.data.logs);
        setDownloadUrl(`${API_URL}${response.data.download_url}`);
      } else {
        setLogs(response.data.logs);
        setDownloadUrl("");
      }
    } catch (error) {
      setLogs("Compilation failed. Please check the logs.");
      setDownloadUrl("");
    }
  };

  return (
    <div className="App">
      <h1 className="projectTitle">Cross Platform C Compiler for Embedded systems</h1>

      <div className="nameContainer">
        <div className="submittedBy">
          <label>Submitted By:</label>
          <div className="person">
            <h4>J. Supreeth kumar</h4>
            <p>Register No.: 192372021</p>
          </div>
          <div className="person">
            <h4>M. Deepika</h4>
            <p>Register No.: 192311027</p>
          </div>
        </div>
      </div>

      <h2>Upload a C file for Compilation</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="file">Select C File:</label>
          <input type="file" id="file" onChange={handleFileChange} required />
        </div>
        <div>
          <label htmlFor="arch">Select Target Architecture:</label>
          <select id="arch" value={arch} onChange={handleArchChange} required>
            <option value="aarch64">ARM64 (Apple Silicon)</option>
            <option value="x86-64">x86-64 (Intel/AMD)</option>
            <option value="avr">AVR (Atmel)</option>
          </select>
        </div>
        <button type="submit">Compile</button>
      </form>

      {logs && (
        <div className="logs">
          <h3>Compilation Logs:</h3>
          <pre>{logs}</pre>
        </div>
      )}

      {downloadUrl && (
        <div className="download">
          <h3>Download Compiled File:</h3>
          <a href={downloadUrl} download>
            Click here to download
          </a>
        </div>
      )}
      <footer className="subjectCode">CSA1427 - Compiler Design for SLR Parser</footer>
    </div>
  );
}

export default App;