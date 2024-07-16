// App.js
import React, { useState } from 'react';
import './App.css';
import KeyValueTable from './components/KeyValueTable';

function App() {
  const [results, setResults] = useState({});
  const [selectedContentKey, setSelectedContentKey] = useState(null);
  const [fileName, setFileName] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isFileUploaded, setIsFileUploaded] = useState(false);

  const handleFileUpload = async (event) => {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      setFileName(file.name);
      const formData = new FormData();
      formData.append('customerLog', file);

      try {
        const response = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) throw new Error('Network response was not ok.');

        const data = await response.json();
        setResults(data);
        setIsFileUploaded(true); // Set file uploaded state to true
      } catch (error) {
        console.error('Error during fetch:', error);
      }
    }
  };

  const handleButtonClick = (contentKey) => {
    setSelectedContentKey(contentKey);
  };

  const getStatusColor = (status) => {
    return status ? '#006400' : '#8b0000'; // Darker green and red
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="App">
      <div className="top-section">
        <button onClick={() => document.getElementById('fileInput').click()}>Upload and Process ULog File</button>
        <input type="file" id="fileInput" onChange={handleFileUpload} />
        {fileName && <span className="filename-display">Uploaded File: {fileName}</span>}
      </div>
      <div className="main-content">
        {isFileUploaded && (
          <div className={`sidebar ${isSidebarOpen ? 'open' : 'closed'}`}>
            <button className="toggle-button" onClick={toggleSidebar}>
              <span className="hamburger-icon"></span>
              <span className="hamburger-icon"></span>
              <span className="hamburger-icon"></span>
            </button>
            {isSidebarOpen && Object.keys(results).map((key) => (
              <button
                key={key}
                onClick={() => handleButtonClick(key)}
                style={{ backgroundColor: getStatusColor(results[key].status) }}
                className={selectedContentKey === key ? 'active' : ''}
              >
                {key.replace(/_/g, ' ')}
              </button>
            ))}
          </div>
        )}
        <div className="content">
          {selectedContentKey && <KeyValueTable data={results[selectedContentKey]} />}
        </div>
      </div>
    </div>
  );
}

export default App;
