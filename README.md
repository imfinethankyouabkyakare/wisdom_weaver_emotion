# Bhagavad Gita Wisdom Weaver

An AI-powered application that provides wisdom from the Bhagavad Gita based on user emotions and questions.

## Features

- Emotion detection through webcam
- AI-powered responses based on the Bhagavad Gita
- Browse Gita chapters and verses
- Personalized spiritual guidance

## Deployment Instructions for Streamlit Cloud

1. Fork or create a new GitHub repository with these files:
   - `app.py`
   - `requirements.txt`
   - `bhagavad_gita_verses.csv`
   - The image file `WhatsApp Image 2024-11-18 at 11.40.34_076eab8e.jpg`

2. Go to [Streamlit Cloud](https://streamlit.io/cloud)

3. Sign in with your GitHub account

4. Click "New app"

5. Select your repository, branch, and set the main file path to `app.py`

6. Advanced settings:
   - You may need to set up secrets for the API key (if you're not hardcoding it)
   - Add the following command to enable camera access:
     ```
     --server.enableCORS=false --server.enableXsrfProtection=false
     ```

7. Deploy your app

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Note

Make sure you have the proper image file uploaded to your repository with the correct filename:
`WhatsApp Image 2024-11-18 at 11.40.34_076eab8e.jpg`
