import axios from 'axios';
import React, { useState } from 'react';

function App() {
  const [image, setImage] = useState(null);
  const [heatmap, setHeatmap] = useState(null);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    setImage(file);

    const formData = new FormData();
    formData.append('image', file);

    const response = await axios.post('/gradcam', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      responseType: 'arraybuffer'
    });

    const blob = new Blob([response.data], { type: 'image/png' });
    const url = URL.createObjectURL(blob);
    setHeatmap(url);
  };

  return (
    <div>
      <input type="file" onChange={handleImageUpload} />
      {heatmap && <img src={heatmap} />}
    </div>
  );
}

export default App;
