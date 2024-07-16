// App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [output, setOutput] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    const data = await response.text();
    setOutput(data);
  };

  return (
    <div className="App">
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleSubmit}>Upload</button>
      <pre>{output}</pre>
    </div>
  );
}

export default App;