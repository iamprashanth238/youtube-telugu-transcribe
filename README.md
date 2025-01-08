# Telugu Transcription for YouTube Videos

## Abstract
This project develops a browser extension for transcribing Telugu YouTube videos using the OpenAI Whisper model. The transcription tool aims to improve accessibility for Telugu-speaking audiences by providing accurate and real-time transcriptions directly within the video interface. Powered by Flask on the backend, the system processes audio and delivers text outputs seamlessly. The fine-tuned Whisper model ensures transcription quality, capturing nuances of regional dialects and diverse speech patterns. Applications include online education, content creation, and enhancing media accessibility for the hearing impaired.

### Key Features
- Automatic punctuation and contextual understanding.
- Integration with YouTube for real-time transcription.
- Supports regional Telugu dialects and varying accents.

---

## Results
### Word Error Rate (WER) Comparison:
| **Metric**            | **Before Fine-Tuning** | **After Fine-Tuning** |
|------------------------|------------------------|------------------------|
| **Orthographic WER**   | Not explicitly given  | **40.66%**            |
| **Standard WER**       | **123.08%**           | **15.38%**            |

### Additional Metrics:
- **Training Loss**: 0.2289
- **Validation Loss**: 0.0903
- **Epochs Completed**: 9

---

## Outputs
1. **Generated Transcriptions**:
   - High-quality transcriptions capturing regional nuances and contextual clarity.
   - Transcriptions evaluated using Word Error Rate (WER) for accuracy.

2. **Visual Comparison**:
   ![Screenshot 2024-10-23 211017](https://github.com/user-attachments/assets/2a19ffba-4906-4f71-838b-d4056d4b6cc7)
   ![Screenshot 2024-10-23 210840](https://github.com/user-attachments/assets/7145c0db-1da2-4403-9d2c-ec0b09095689)


---

## Features
- **Backend**: Flask for processing transcription requests.
- **Frontend**: User-friendly interface for uploading YouTube video links and viewing transcriptions.
- **Fine-Tuned Whisper Model**: Improved transcription accuracy through targeted training on Telugu datasets.

---

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/telugu-transcription.git
   cd telugu-transcription
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Access the application in your browser:
   - Upload a YouTube video link to view real-time Telugu transcriptions.

---

## Future Enhancements
- **Dialect-Specific Fine-Tuning**: Extend support for Telugu dialects to improve regional accuracy.
- **Mobile Support**: Integrate transcription capabilities into mobile applications.
- **Multilingual Transcriptions**: Support mixed-language transcription (e.g., Telugu-English).

---

