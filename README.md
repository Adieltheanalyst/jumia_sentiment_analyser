# 📱 Sentiment Analysis on Jumia Smartphones Under KES 10,000

An end-to-end data science project that scrapes, processes, and analyzes Jumia customer reviews for budget smartphones (≤ KES 10,000), combining web scraping, SQL storage, NLP preprocessing, topic modeling, and machine learning.

---

## 🎯 Project Overview

- **Objective**: Scrape smartphone reviews from Jumia, store them in a database, and apply NLP and ML to uncover customer sentiments and trending themes.
- **Dataset**: Reviews, star ratings, product metadata from Jumia smartphones priced under KES 10,000.
- **Outcomes**:
  - Sentiment distribution breakdown (positive, neutral, negative)
  - Insights into battery life, camera, pricing issues
  - Topic modeling to identify key review themes
  - Evaluation of multiple sentiment models (TextBlob, VADER, RoBERTa)
  - ML classification to detect negative sentiments with high recall

---

## 🧰 Tools & Tech Stack

| Category              | Tools / Libraries                          |
|-----------------------|--------------------------------------------|
| Web Scraping          | Scrapy, Selenium                          |
| Database              | SQLite (`jumia_data.db`)                  |
| Data Processing       | Pandas, `re`, `sqlite3`                   |
| NLP & Sentiment       | NLTK, TextBlob, VADER, RoBERTa            |
| Topic Modeling        | LDA                                       |
| Feature Engineering   | TF-IDF (unigrams + bigrams)               |
| Machine Learning      | Scikit-learn (Naive Bayes, SVM, Logistic) |
| Visualization         | Matplotlib, Seaborn                       |
| Environment           | Python, Jupyter, VSCode                   |

---

## 🔄 Project Workflow

1. **Data Extraction**
   - `scraping.py`: Scrapy spider extracts smartphone URLs.
   - Dynamic review loading handled with Selenium.
   - Output stored as `page_source.html` and into `jumia_data.db`.

2. **Data Storage**
   - SQLite DB with tables for reviews and product metadata.

3. **Data Preprocessing & Sentiment Scoring**
   - `sentiment_analyser.ipynb`: pipeline to clean text, tokenize, and lemmatize.
   - Generates sentiment scores with TextBlob, VADER, and RoBERTa.
   - Analyzes mismatches (12.5%) between sentiment vs. star ratings.

4. **Topic Modeling**
   - Visualized in `lda_visualization.html`, identifying 3 core review themes.

5. **Feature Engineering & ML Modeling**
   - Converts text to TF-IDF features.
   - Trains and compares Naive Bayes, Logistic Regression, Balanced SVM, and SMOTE-enhanced SVM.
   - Evaluates models based on accuracy, precision, recall, and F1-score.

---

## 📈 Key Findings

- ~70% of reviews were positive, 22% negative, 8% neutral.
- Battery life, charging time, camera quality, and pricing were prominent discussion topics.
- RoBERTa showed the strongest agreement (65.6%) with star ratings.
- Nokia models had the most polarized sentiments; Itel phones were most reviewed within the price range.
- Balanced SVM prioritized negative review recall, key for detecting customer issues.

---

## ⚠️ Challenges

- **Class imbalance** made negative sentiment detection tricky.
- Misuse of star ratings and sarcasm affected sentiment alignment.
- SMOTE skewed model bias toward minority classes.

---

## 🚀 Next Steps

- Extend scraping to other platforms (e.g., Kilimall) to compare sentiment across marketplaces.
- Broaden category scope (e.g., tablets, accessories).
- Collect more data to improve training and class balance.
- Explore advanced NLP models (fine-tuned BERT/RoBERTa) for sentiment nuance.

---

## 📂 Repository Contents

- `scraping.py` – Scrapes URLs and reviews via Scrapy/Selenium  
- `page_source.html` – Sample HTML from review pages  
- `jumia_data.db` – SQLite database containing reviews and product info  
- `sentiment_analyser.ipynb` – Preprocessing, sentiment scoring, topic modeling, ML training  
- `lda_visualization.html` – Interactive visualization of LDA topics  
- `requirements.txt` – Python dependencies  
- `.idea/`, `localurls/` – IDE and config files

---

## 📥 Setup & Usage

1. **Clone the repo**  
   ```bash
   git clone https://github.com/Adieltheanalyst/jumia_sentiment_analyser.git
   cd jumia_sentiment_analyser
