document.getElementById("run").addEventListener("click", async () => {
  const source_code = document.getElementById("code").value;
  const customKeywordsText = document.getElementById("custom").value;
  let custom_keywords = {};

  if (customKeywordsText.trim()) {
    try {
      custom_keywords = JSON.parse(customKeywordsText);
    } catch (e) {
      document.getElementById("output").textContent = "❌ Invalid JSON for custom keywords!";
      return;
    }
  }

  try {
    const response = await fetch("/run", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        source_code,
        custom_keywords
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "Unknown error occurred");
    }

    const data = await response.json();
    document.getElementById("output").textContent = data.output || "(No output)";
  } catch (err) {
    document.getElementById("output").textContent = `❌ Error: ${err.message}`;
  }
});

