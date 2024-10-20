async function callGeminiAPI(prompt,key) {
    const apiKey = key; // Replace with your actual API key
    const url = "https://api.geminiai.com/api/v1/generate";
  
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          prompt: prompt   
  
        })
      });
  
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
  
      const data = await response.json();
      return data.text; // Access the generated text from the response
    } catch (error) {
      console.error("Error calling Gemini API:", error);
      return null;
    }
  }