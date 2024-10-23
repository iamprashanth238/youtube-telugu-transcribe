const btn = document.getElementById("transcribe");
const output = document.getElementById("output");

btn.addEventListener("click", function () {
    btn.disabled = true;
    btn.innerHTML = "Transcribing...";

    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
        const url = tabs[0].url;
        chrome.runtime.sendMessage({ type: "START_TRANSCRIPTION", url: url });

        // fetch transcription from server
        fetch("http://localhost:5000/transcribe?url=" + encodeURIComponent(url))
            .then(response => {
                if (!response.ok) throw new Error("Network response was not ok");
                return response.json();
            })
            .then(data => {
                output.innerHTML = data.transcription;
                btn.disabled = false;
                btn.innerHTML = "Transcribe";
            })
            .catch(error => {
                console.error("Error during transcription:", error);
                output.innerHTML = "Failed to fetch transcription.";
                btn.disabled = false;
                btn.innerHTML = "Transcribe";
            });
    });
});

