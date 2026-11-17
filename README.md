# Voice of Customer Copilot

An AI-assisted customer feedback analytics MVP for fashion e-commerce teams. It converts customer reviews into sentiment trends, recurring pain points and prioritised product opportunities.

## Problem
Product teams receive feedback across reviews and support channels, but manually identifying repeated issues is slow. This project provides a repeatable first-pass analysis workflow.

## Features
- Upload a CSV of customer reviews or use the included sample.
- Sentiment classification using VADER.
- Categorise feedback into delivery, sizing, quality, returns, pricing and support themes.
- View sentiment, rating and issue trends in an interactive dashboard.
- Inspect representative reviews and download the enriched dataset.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Input format
CSV must include a `review` column. Optional columns: `rating`, `product_category`, `date`, `review_id`. A sample is provided in `data/sample_reviews.csv`.

## Metrics
The dashboard reports review volume, positive share, average rating, category-level complaint volume and issue mix. These are descriptive signals, not causal proof of product defects.

## Project structure
- `app.py`: Streamlit dashboard and analysis pipeline
- `data/sample_reviews.csv`: illustrative synthetic dataset
- `requirements.txt`: Python dependencies

## Limitations
Sentiment and theme assignment are lightweight heuristics; sarcasm, multilingual feedback and overlapping issues may be misclassified. Validate findings with customer research before making product decisions.

## Author
Adarsh Kumar · [GitHub](https://github.com/adarshkumar9199)

## License
MIT
