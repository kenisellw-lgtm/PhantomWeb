async function startRemix() {
    const audioFile = document.getElementById("audioInput").files[0];
    const prompt = document.getElementById("promptInput").value;
    const status = document.getElementById("statusText");
    const btn = document.getElementById("generateBtn");
    const resultArea = document.getElementById("resultArea");

    if (!audioFile || !prompt) {
        alert("⚠️ Please upload a file and describe the style!");
        return;
    }

    // Lock UI
    btn.disabled = true;
    btn.style.opacity = "0.5";
    status.innerText = "📡 Uploading & Processing... (Wait ~30s)";
    resultArea.style.display = "none";

    const formData = new FormData();
    formData.append("audio", audioFile);
    formData.append("prompt", prompt);

    try {
        const response = await fetch("/generate", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        // Success
        status.innerText = "✅ Done!";
        document.getElementById("audioPlayer").src = data.audio_url;
        document.getElementById("downloadLink").href = data.audio_url;
        resultArea.style.display = "block";

    } catch (error) {
        console.error(error);
        status.innerText = "❌ Error: " + error.message;
        alert("Error: " + error.message);
    } finally {
        btn.disabled = false;
        btn.style.opacity = "1";
    }
}