# 📱 Bank App Reviews – Sentiment & Thematic Analysis

A data pipeline and analysis project focused on understanding user feedback for Ethiopian bank mobile applications through sentiment analysis, keyword extraction, and theme identification.


## 📌 Project Overview

This project analyzes customer reviews collected from Google Play Store for selected Ethiopian banks.
It aims to uncover user satisfaction, pain points, and recurring themes based on natural language processing (NLP) techniques.

The project includes:

🔹 Automated scraping of bank app reviews

🔹 Data preprocessing pipeline

🔹 Sentiment analysis using VADER & TextBlob

🔹 Keyword extraction using Bag-of-Words & TF-IDF

🔹 Topic exploration with simple LDA

🔹 EDA notebook for visual and textual analysis

🔹 Clean and modular folder structure


## 📂 Project Structure

project-root/

│

├── scripts/

│   ├── scraper.py          # Scrapes Google Play reviews

│   ├── preprocessing.py    # Cleans, filters, and prepares review data

│   └── config.py           # Bank IDs and configuration settings

│

├── notebooks/

│   ├── preprocessing_eda.ipynb   # EDA & sentiment exploration

│   └── sentiment_analysis.ipynb  # Task-2 analysis

│

├── data/

│   ├── raw/                # Raw scraped data

│   └── processed/          # Cleaned output CSV files

│

└── README.md



## ⚙️ Setup Instructions

1️⃣ Clone Repository

- git clone https://github.com/your-repo.git

- cd project-root

2️⃣ Create & Activate Virtual Environment

- python -m venv venv

- source venv/bin/activate      # Linux/Mac

- venv\Scripts\activate         # Windows

3️⃣ Install Requirements

- pip install -r requirements.txt

4️⃣ Environment Variables

- Create a .env file in the project root (if required):

- API_KEY=your_key_here


## 🗂️ Data Sources

This project uses publicly available Google Play Store reviews for Ethiopian banking applications, including:

- CBE

- Dashen Bank

- Abyssinia Bank


## 🧹 Data Preprocessing

- The preprocessing pipeline performs:

- Lowercasing and whitespace cleanup

- Removing non-English reviews

- Handling missing or invalid rows

- Normalizing dates

- Adding text-length & helpful metadata

- Preparing clean dataset for sentiment and thematic analysis


✅ Output is saved in:

- data/processed/clean_reviews.csv


## 📊 Sentiment Analysis

The project evaluates user sentiment using:

✔️ VADER

Best for short app reviews.

Generates:

- compound score

- positive / neutral / negative labels


✔️ TextBlob

Provides:

- polarity

- subjectivity

Sentiment is compared with star ratings to validate trends.


## 🧵 Thematic & Keyword Analysis

The project extracts core user concerns using:

✔️ CountVectorizer (BoW)

- To identify frequency-based keywords.

✔️ TF-IDF

- To highlight unique or informative words.

✔️ Basic Topic Modeling (optional LDA)

To observe clusters of words forming potential themes.

Themes can include:

- App performance & speed

- Login / authentication issues

- UI & ease of use

- Transaction reliability

- Feature requests


## 📘 Notebooks

Two main Jupyter notebooks guide the analysis:

### 📒 preprocessing_eda.ipynb

- Loads processed data

- Visualizes rating distribution

- Word frequencies

- TF-IDF scores


### 📘 sentiment_analysis.ipynb

- Applies VADER & TextBlob

- Compares sentiment vs star rating

- Extracts keywords

- Explores topics & themes


## 🔀 Git Workflow

Branching strategy used:

- main → stable code

- task-1 → scraping + preprocessing

- task-2 → sentiment + thematic analysis


All tasks merged through pull requests.


## 📦 Data Sources

Reviews are scraped directly from:

✔️ Google Play Store public review pages

No private or sensitive data is collected.


## Summary

This project provides a complete pipeline for:

- Collecting app reviews

- Cleaning and structuring text data

- Performing sentiment analysis

- Extracting themes from real user feedback


It helps identify actionable insights for improving banking mobile applications.
