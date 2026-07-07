<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README - Sentiment Analysis Project</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #24292e;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
        }
        h1, h2, h3 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }
        h1 { font-size: 2em; }
        h2 { font-size: 1.5em; }
        h3 { font-size: 1.25em; }
        a { color: #0366d6; text-decoration: none; }
        a:hover { text-decoration: underline; }
        code {
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 85%;
        }
        pre {
            background-color: #f6f8fa;
            padding: 16px;
            border-radius: 6px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #dfe2e5;
            padding: 8px 13px;
            text-align: left;
        }
        th {
            background-color: #f6f8fa;
            font-weight: 600;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        .badge {
            display: inline-block;
            padding: 0.2em 0.6em;
            margin: 0 0.2em;
            font-size: 75%;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 0.25rem;
            color: #fff;
            background-color: #28a745;
        }
        .badge-blue { background-color: #0366d6; }
        .badge-purple { background-color: #6f42c1; }
    </style>
</head>
<body>

    <h1>🧠 Sentiment Analysis of Digital Product Reviews</h1>

    <p>
        <span class="badge">Python</span>
        <span class="badge badge-blue">Machine Learning</span>
        <span class="badge badge-purple">Web Scraping</span>
        <span class="badge">NLP</span>
    </p>

    <blockquote>
        <strong>Course Project</strong> – Computer Programming Fundamentals<br>
        Instructor: Tayebeh Rafiei · Semester: Summer 2025
    </blockquote>

    <hr>

    <h2>📌 Project Overview</h2>
    <p>
        This project aims to automatically classify user sentiment (positive/negative) from product reviews using <strong>web scraping</strong>, <strong>text preprocessing</strong>, and <strong>machine learning</strong>. Reviews are collected from three platforms:
    </p>
    <ul>
        <li>🇮🇷 <strong>Basalam</strong> (Persian)</li>
        <li>🇮🇷 <strong>Taaghche</strong> (Persian)</li>
        <li>🇬🇧 <strong>Trustpilot</strong> (English)</li>
    </ul>

    <h2>🧰 Tools & Technologies</h2>
    <ul>
        <li><strong>Web Scraping</strong>: <code>requests</code>, <code>BeautifulSoup</code>, <code>Selenium</code></li>
        <li><strong>Data Processing</strong>: <code>pandas</code>, <code>numpy</code>, <code>regex</code></li>
        <li><strong>Visualization</strong>: <code>matplotlib</code>, <code>seaborn</code>, <code>wordcloud</code></li>
        <li><strong>ML Models</strong>: <code>Logistic Regression</code>, <code>Multinomial Naive Bayes</code>, <code>Linear SVM</code></li>
        <li><strong>Text Vectorization</strong>: <code>TF-IDF</code></li>
        <li><strong>Evaluation</strong>: <code>accuracy</code>, <code>precision</code>, <code>recall</code>, <code>F1-score</code>, <code>confusion matrix</code></li>
    </ul>

    <h2>📁 Project Structure</h2>
    <pre>
SentimentProject/
│
├── data/
│   ├── Basalam_reviews.csv
│   ├── Taghcheh_reviews.csv
│   └── Trustpilot_reviews.csv
│
├── figures/
│   ├── basalam/
│   ├── taaghche/
│   └── trustpilot/
│
├── files/
│   ├── train/ & test/ comments
│   └── font/
│
├── models/
│   ├── LogisticRegression_model.pkl
│   ├── MultinomialNB_model.pkl
│   ├── LinearSVM_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── sentiment_model_final.pkl
│
├── reports/
│   ├── final_report.pdf
│   └── final_report.docx
│
├── requirements/
│   ├── TextPreprocessing/
│   └── WebScraping/
│
└── README.md
    </pre>

    <h2>⚙️ How to Run</h2>
    <h3>1. Clone the repository</h3>
    <pre><code>git clone https://github.com/AmirHosseinRezaaie/Sentiment-Analysis-Reviews.git
cd Sentiment-Analysis-Reviews</code></pre>

    <h3>2. Install dependencies</h3>
    <pre><code>pip install -r requirements.txt</code></pre>

    <h3>3. Run the notebook</h3>
    <p>Open <code>final_project.ipynb</code> in Jupyter or Colab and run all cells.</p>

    <h3>4. (Optional) Scrape new data</h3>
    <p>Use scripts inside <code>requirements/WebScraping/</code> to scrape fresh reviews.</p>

    <h2>📊 Results Summary</h2>
    <table>
        <thead>
            <tr>
                <th>Model</th>
                <th>Accuracy</th>
                <th>F1-Score</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Logistic Regression</td>
                <td>~88%</td>
                <td>~0.87</td>
            </tr>
            <tr>
                <td>Multinomial Naive Bayes</td>
                <td>~86%</td>
                <td>~0.85</td>
            </tr>
            <tr>
                <td><strong>Linear SVM</strong></td>
                <td><strong>~89%</strong></td>
                <td><strong>~0.88</strong></td>
            </tr>
        </tbody>
    </table>
    <blockquote>
        ✅ Linear SVM performed best overall with balanced precision/recall.
    </blockquote>

    <h2>📈 Visualizations</h2>
    <ul>
        <li>Sentiment distribution</li>
        <li>Word clouds for positive/negative reviews</li>
        <li>Text length analysis</li>
        <li>Confusion matrices for each model</li>
    </ul>

    <h2>🧠 What I Learned</h2>
    <ul>
        <li>Real-world data scraping challenges (dynamic content, pagination)</li>
        <li>Importance of text cleaning for Persian (نویسه‌های خاص، نیم‌فاصله)</li>
        <li>TF-IDF vs. CountVectorizer</li>
        <li>Model evaluation beyond accuracy</li>
        <li>Project structuring and documentation</li>
    </ul>

    <h2>🚀 Future Improvements</h2>
    <ul>
        <li>Deep learning models (LSTM, BERT)</li>
        <li>Multi-lingual support (Persian + English)</li>
        <li>Real-time dashboard</li>
        <li>Aspect-based sentiment analysis</li>
        <li>Scraping from more platforms</li>
    </ul>

    <h2>👤 Author</h2>
    <p>
        <strong>AmirHossein Rezaaie</strong><br>
        <a href="https://github.com/AmirHosseinRezaaie">GitHub</a> · 
        <a href="https://www.linkedin.com/in/amirhoseinrezaaie">LinkedIn</a>
    </p>

    <h2>📜 License</h2>
    <p>This project is for educational purposes only.</p>

    <hr>
    <p style="text-align: center; color: #586069;">
        Made with ❤️ for the love of data and machine learning
    </p>

</body>
</html>