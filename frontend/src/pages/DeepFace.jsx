import React, { useState } from 'react';
import api from '../services/api';

function DeepFace() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [detectionResult, setDetectionResult] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result); // Base64 string for display
      };
      reader.readAsDataURL(file);
    } else {
      setImagePreview(null);
    }
  };

  const handleDetectFaces = async () => {
    if (!selectedFile) {
      setMessage('Please select an image first.');
      return;
    }

    setMessage('Detecting faces...');
    try {
      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64Image = reader.result.split(',')[1]; // Get only the base64 part
        const response = await api.post('/deepface/detect/', {
          image_base64: base64Image,
          detector_backend: 'opencv',
          return_face_chip: true,
        });
        setDetectionResult(response.data);
        setMessage(`Detected ${response.data.detected_faces_count} faces.`);
      };
      reader.readAsDataURL(selectedFile);
    } catch (error) {
      setMessage(`Detection failed: ${error.response?.data?.detail || error.message}`);
      setDetectionResult(null);
    }
  };

  return (
    <div>
      <h2>DeepFace Operations</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {imagePreview && <img src={imagePreview} alt="Preview" style={{ maxWidth: '300px', margin: '10px 0' }} />}
      <button onClick={handleDetectFaces}>Detect Faces</button>
      {message && <p>{message}</p>}
      {detectionResult && (
        <div>
          <h3>Detection Results:</h3>
          <p>Count: {detectionResult.detected_faces_count}</p>
          {detectionResult.faces.map((face, index) => (
            <div key={index} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
              <p>Face {index + 1}: ({face.x}, {face.y}, {face.w}, {face.h}) Confidence: {face.confidence.toFixed(2)}</p>
              {face.face_chip_base64 && (
                <img src={`data:image/jpeg;base64,${face.face_chip_base64}`} alt="Face Chip" style={{ width: '100px' }} />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default DeepFace;