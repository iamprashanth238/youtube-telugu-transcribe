// Inject a button into the YouTube page
function injectButton() {
    const button = document.createElement('button');
    button.innerText = 'Transcribe';
    button.id = 'transcribe-button';
    button.style.position = 'fixed';
    button.style.top = '100px'; 
    button.style.right = '20px';
    button.style.zIndex = '1000';
    button.style.backgroundColor = '#ff0000';
    button.style.color = '#ffffff';
    button.style.border = 'none';
    button.style.padding = '10px 20px';
    button.style.cursor = 'pointer';

    // Create the div for displaying the transcription
    const transcriptionDiv = document.createElement('div');
    transcriptionDiv.id = 'transcription-output';
    transcriptionDiv.style.position = 'fixed';
    transcriptionDiv.style.top = '150px'; 
    transcriptionDiv.style.right = '20px';
    transcriptionDiv.style.zIndex = '1000';
    transcriptionDiv.style.backgroundColor = '#ffffff';
    transcriptionDiv.style.color = '#000000';
    transcriptionDiv.style.border = '1px solid #000000';
    transcriptionDiv.style.padding = '10px';
    transcriptionDiv.style.display = 'none';  

    document.body.appendChild(button);
    document.body.appendChild(transcriptionDiv);

    // Event Listner when a user click button
    button.addEventListener('click', () => {
        const videoUrl = window.location.href;
        console.log(`Sending URL to background script: ${videoUrl}`);  // Debug print
        chrome.runtime.sendMessage({ action: 'transcribe', url: videoUrl }); // Send video url to to background script
    });

    // Listen for messages from the background script from python server
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === 'updateTranscription') {
            console.log(`Received transcription: ${request.transcription}`);  // Debug print
            transcriptionDiv.innerText = request.transcription;
            transcriptionDiv.style.display = 'block';  // Show the div
        }
    });

}

injectButton();
