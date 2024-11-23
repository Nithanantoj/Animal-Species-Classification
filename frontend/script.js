document.getElementById("predictBtn").addEventListener("click", async () => {
    const imageInput = document.getElementById("imageInput").files[0];
    
    if (!imageInput) {
      alert("Please upload an image.");
      return;
    }
  
    const formData = new FormData();
    formData.append("file", imageInput);
  
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });
  
      if (!response.ok) {
        throw new Error("Failed to fetch prediction");
      }
  
      const data = await response.json();
      document.getElementById("resultText").textContent = `Predicted species: ${data.class}`;
      document.getElementById("confidenceText").textContent = `Confidence: ${data.confidence}`;
      document.getElementById("result-section").style.display = "block";
    } catch (error) {
      console.error(error);
      alert("An error occurred while predicting. Please try again.");
    }
});
