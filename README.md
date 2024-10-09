---

# TalentTrack: ATS Tracking System

This Streamlit-based web application integrates with the Google Gemini model to analyze and improve resumes based on job descriptions. It is designed to help job applicants align their profiles with specific roles by providing professional evaluations, improvement suggestions, and a percentage match between their resumes and job descriptions.

## Features
1. **Analyze Resume**: Evaluate a resume against a provided job description.
2. **Suggest Improvements**: Receive tailored suggestions to improve the resume.
3. **Match Percentage**: Calculate a match percentage and identify missing keywords from the resume.

## Technologies Used
- **Streamlit**: For creating the web-based user interface.
- **Google Generative AI (Gemini)**: Used to analyze resumes and generate responses.
- **PyPDF2**: For extracting text from PDF resumes.
- **Python-dotenv**: To securely load environment variables such as API keys.

## Installation

### Prerequisites
- Python 3.x
- A valid API key for the Google Gemini model

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Anubothu-Aravind/ATS/talenttrack-ats.git
   ```
   
2. Navigate to the project directory:
   ```bash
   cd talenttrack-ats
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file in the project directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=<your_gemini_api_key>
   ```

## Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Upload a PDF resume and input a job description in the respective fields.
3. Choose one of the following actions:
   - **Analyze Resume**: Provides a professional evaluation.
   - **Suggest Improvements**: Offers feedback for improving the resume.
   - **Match Percentage**: Calculates a match percentage and suggests missing keywords.

## License
This project is open-source.

---
