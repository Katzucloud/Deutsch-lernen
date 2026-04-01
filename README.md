# 🇩🇪 Deutsch Lernen — B2/C1 Phrase Trainer

A dark-themed German language learning app powered by **Google Gemini AI** (free) and hosted on **Streamlit Community Cloud** (free).

Every phrase is generated fresh by AI — unlimited B2–C1 level German with instant translation checking, a flip mode, and a personal notebook for tricky words.

---

## 🚀 Deploy in 5 Steps

### Step 1 — Get a Free Gemini API Key
1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API key"**
4. Copy the key — you'll need it in Step 4

> **Free tier:** Gemini Flash-Lite gives you 1,000 requests/day and 15 RPM — plenty for personal use.

---

### Step 2 — Fork this Repo to GitHub
1. Click **Fork** at the top-right of this GitHub page
2. Name it whatever you like (e.g. `deutsch-lernen`)
3. Make sure it's **Public** (required for free Streamlit hosting)

---

### Step 3 — Create a Streamlit Community Cloud Account
1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"** and connect your GitHub account
3. It's completely free

---

### Step 4 — Deploy Your App
1. In your Streamlit workspace, click **"Create app"** (top right)
2. Select **"Use existing repo"**
3. Fill in:
   - **Repository:** `your-username/deutsch-lernen`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
4. Click **"Advanced settings"** → go to **"Secrets"**
5. Paste this, replacing with your actual key:
   ```toml
   GEMINI_API_KEY = "AIza..."
   ```
6. Click **"Deploy!"**

Your app will be live at:
`https://your-username-deutsch-lernen-streamlit-app-xxxx.streamlit.app`

---

### Step 5 — (Optional) Set a Custom URL
In Streamlit app settings → **"App URL"** → pick a memorable subdomain like `deutsch-lernen`

---

## 🎮 Features

| Feature | Description |
|---|---|
| 🔄 New Phrase | Generates a fresh B2-C1 German phrase via Gemini AI |
| 🔀 Flip | Switch between DE→EN and EN→DE translation modes |
| ✓ Check | Validates your answer (generous matching) |
| 👁 Reveal | Shows the answer and saves to notebook |
| 💾 Save | Manually save any phrase to your notebook |
| 📓 Notebook | Sidebar list of saved/wrong/revealed phrases |

---

## 🏗 Project Structure

```
deutsch-lernen/
├── streamlit_app.py     # Main app
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🔑 Secrets Reference

Add this in Streamlit Cloud → App Settings → Secrets:

```toml
GEMINI_API_KEY = "your_key_here"
```

Never commit your API key to GitHub.

---

## 🛠 Local Development

```bash
pip install streamlit google-generativeai

# Create .streamlit/secrets.toml locally:
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "your_key_here"' > .streamlit/secrets.toml

streamlit run streamlit_app.py
```
