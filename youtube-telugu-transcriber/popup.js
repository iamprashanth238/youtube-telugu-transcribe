const btn = document.getElementById("transcribe");

btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Transcribing...";
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs) {
        var url = tabs[0].url;
        console.log(url);
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://localhost:5000/transcribe?url=" + encodeURIComponent(url), true);
        xhr.onload = function() {
            var text = xhr.responseText;
            const p = document.getElementById("output");
            p.innerHTML = text;
            btn.disabled = false;
            btn.innerHTML = "Transcribe";
        };
        xhr.onerror = function() {
            console.error("Request failed");
            const p = document.getElementById("output");
            p.innerHTML = "Failed to fetch transcription.";
            btn.disabled = false;
            btn.innerHTML = "Transcribe";
        };
        xhr.send();  // Send the request
    });
});
