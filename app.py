import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="Voice of Customer Copilot", page_icon="💬", layout="wide")
st.title("💬 Voice of Customer Copilot")
st.caption("Turn fashion e-commerce reviews into customer experience insights.")

THEMES = {
    "Delivery": ["delivery", "late", "delayed", "rescheduled", "arrived"],
    "Size & Fit": ["size", "fit", "fitting", "chart", "small", "large"],
    "Product Quality": ["quality", "fabric", "material", "stitch", "damaged", "faded", "cheap"],
    "Returns & Refunds": ["return", "refund", "exchange", "pickup"],
    "Pricing & Discounts": ["price", "pricing", "discount", "expensive", "cost"],
    "Customer Support": ["support", "service", "response", "complaint", "resolve"],
}
analyzer = SentimentIntensityAnalyzer()


def classify_theme(text):
    text = str(text).lower()
    scores = {theme: sum(1 for word in words if re.search(r"\b" + re.escape(word) + r"\b", text)) for theme, words in THEMES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "Other"


def enrich(data):
    df = data.copy()
    df["review"] = df["review"].fillna("").astype(str)
    df["sentiment_score"] = df["review"].apply(lambda x: analyzer.polarity_scores(x)["compound"])
    df["sentiment"] = df["sentiment_score"].apply(lambda x: "Positive" if x >= 0.05 else ("Negative" if x <= -0.05 else "Neutral"))
    df["theme"] = df["review"].apply(classify_theme)
    if "rating" in df.columns:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    return df


sample_path = Path(__file__).parent / "data" / "sample_reviews.csv"
uploaded = st.file_uploader("Upload customer reviews CSV", type="csv")
try:
    raw = pd.read_csv(uploaded) if uploaded else pd.read_csv(sample_path)
except Exception as exc:
    st.error(f"Could not read the CSV: {exc}")
    st.stop()

if "review" not in raw.columns:
    st.error("CSV must contain a 'review' column.")
    st.stop()

df = enrich(raw)
total = len(df)
negative_share = (df["sentiment"] == "Negative").mean() * 100 if total else 0
avg_rating = df["rating"].mean() if "rating" in df.columns else None
c1, c2, c3 = st.columns(3)
c1.metric("Reviews analysed", f"{total:,}")
c2.metric("Negative feedback", f"{negative_share:.1f}%")
c3.metric("Average rating", f"{avg_rating:.2f}/5" if pd.notna(avg_rating) else "Not provided")

left, right = st.columns(2)
with left:
    st.subheader("Sentiment distribution")
    sentiment_counts = df["sentiment"].value_counts().rename_axis("Sentiment").reset_index(name="Reviews")
    st.plotly_chart(px.pie(sentiment_counts, names="Sentiment", values="Reviews", hole=0.45), use_container_width=True)
with right:
    st.subheader("Customer pain points")
    theme_counts = df[df["sentiment"] == "Negative"]["theme"].value_counts().rename_axis("Theme").reset_index(name="Negative reviews")
    st.plotly_chart(px.bar(theme_counts, x="Theme", y="Negative reviews", color="Negative reviews"), use_container_width=True)

st.subheader("Insights to investigate")
if not theme_counts.empty:
    for _, row in theme_counts.head(3).iterrows():
        st.write(f"- **{row['Theme']}** appears in {int(row['Negative reviews'])} negative review(s). Review examples and validate root causes before prioritising.")
else:
    st.info("No negative reviews detected in this dataset.")

st.subheader("Review explorer")
filters = st.multiselect("Filter by theme", sorted(df["theme"].unique()), default=sorted(df["theme"].unique()))
view = df[df["theme"].isin(filters)]
st.dataframe(view, use_container_width=True, hide_index=True)
st.download_button("Download analysed reviews", df.to_csv(index=False).encode("utf-8"), "analysed_reviews.csv", "text/csv")
st.caption("Sentiment/theme labels are directional heuristics. They are not a substitute for qualitative research.")
