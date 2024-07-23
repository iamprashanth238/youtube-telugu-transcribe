chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'updateTranscription') {
      console.log('Updating transcription:', request.transcription);  // Debug print
      document.getElementById('transcription').innerText = request.transcription;
  }
});


