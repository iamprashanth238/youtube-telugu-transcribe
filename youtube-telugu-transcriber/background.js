
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => { // Chrome API Listen for request
    if (message.action === 'transcribe') {
        console.log(`Received URL for transcription: ${message.url}`);  // Debug print
        fetch('http://localhost:5000/transcribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: message.url })
        })
        .then(response => response.json())
        .then(data => {
            console.log(`Received transcription data: ${data.transcription}`);  // Debug print
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                chrome.tabs.sendMessage(tabs[0].id, { action: 'updateTranscription', transcription: data.transcription });
            });
        })
        .catch(error => console.error('Error:', error));
    }
});
