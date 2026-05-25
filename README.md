# 🛒 CartIQ — Know Your True Price Before You Order

> Quick commerce apps like Zepto and Blinkit add ₹6–30 in hidden charges that appear only at checkout — after you're already committed. CartIQ uses Machine Learning to predict your TRUE final price before you place the order.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cartiq.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

---

## 🎯 The Problem

Ever noticed this?

| Stage | What you see |
|---|---|
| Adding to cart | ₹299 |
| At checkout | ₹327 |
| You paid extra | ₹28 in hidden charges |

These hidden charges include:
- **Handling fee** — charged on every order (₹3–15)
- **Small cart fee** — if your order is below a threshold
- **Rain/weather surge** — added silently during bad weather
- **Night surge** — late night orders cost more
- **Peak hour charge** — 12–2pm and 7–10pm cost extra

No app tells you this **before** checkout. CartIQ does.

---

## ✨ Features

### Module 1 — True Price Calculator
Predicts your actual checkout price including all hidden charges before you order. Powered by a **Random Forest Regressor** trained on 5,000 orders with features like platform, city, weather, time of day, and cart value.

### Module 2 — Platform Comparison
Runs the same prediction across Zepto, Blinkit, and Instamart for your exact cart — tells you which platform is genuinely cheapest **today**, not just by MRP.

### Module 3 — Offer Genuineness Scorer
Analyses promo text using **NLP** to score whether a cashback offer or discount is likely real or a dark pattern. Because "Free cashback!" isn't always free.

### Module 4 — Smart Reorder Predictor
Uses **KMeans clustering** to identify your order behavior pattern and predict what you'll run out of — so you can reorder before surge pricing hits.

---

## 🚀 Live Demo

👉 **[cartiq.streamlit.app](https://cartiq.streamlit.app)**

---

## 📸 Screenshots

> *(Add screenshots of your app here after building)*

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| ML — Supervised | Scikit-learn (Random Forest, XGBoost) |
| ML — Unsupervised | Scikit-learn (KMeans Clustering) |
| NLP | Rule-based scorer + HuggingFace |
| Data | Synthetic dataset — 5,000 orders, 26 features |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |
| Version Control | GitHub |

---

## 📁 Project Structure

```
CartIQ/
│
├── data/
│   └── synthetic_orders.csv      # 5000 orders, 26 features
│
├── models/
│   ├── price_predictor.pkl       # Trained Random Forest model
│   └── user_clusters.pkl         # KMeans cluster model
│
├── modules/
│   ├── price_model.py            # Module 1 — price prediction
│   ├── comparison.py             # Module 2 — platform comparison
│   ├── offer_checker.py          # Module 3 — NLP offer scorer
│   └── clustering.py             # Module 4 — reorder predictor
│
├── app.py                        # Main Streamlit app
├── generate_dataset.py           # Synthetic data generation script
├── requirements.txt
└── README.md
```

---

## ⚙️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/CartIQ.git
cd CartIQ

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 📊 Dataset

The dataset was built using **rule-based synthetic data generation** — a standard technique used when proprietary data isn't publicly available.

Real platform policies were researched and encoded as rules:

| Rule | Source |
|---|---|
| Blinkit free delivery above ₹299 | Blinkit platform policy |
| Small cart fee below ₹99–149 | Documented user complaints |
| Rain surge charge ₹10–30 | Reported by Inc42, user reviews |
| Night surge after 10pm | Real platform behavior |
| Cashback offers often unclaimable | Verified via user reviews |

**5,000 orders × 26 features** including platform, city, category, cart value, time of day, weather, all charge breakdowns, offer details, and user behavior signals.

---

## 🤖 ML Models

### Price Predictor (Random Forest)
- **Target:** `final_price` (true checkout price)
- **Features:** cart value, platform, city, hour, weather, is_weekend, num_items
- **Why Random Forest:** handles non-linear interactions (e.g. rain + night + Blinkit = high surge) better than linear models

### User Clustering (KMeans)
- **Features:** order hour, cart value, num_items, category, days_since_last_order
- **Clusters:** Bulk buyer, Late night orderer, Health conscious, Impulsive buyer
- **Use:** powers the smart reorder predictor

### Offer Scorer (NLP)
- **Input:** offer promo text
- **Output:** genuineness score 0–1
- **Flags:** Cashback with high value + low actual discount = dark pattern

---

## 💡 Why CartIQ is Different

| Feature | Buyhatke | QuickCompare | CartIQ |
|---|---|---|---|
| Compares MRP | ✅ | ✅ | ✅ |
| Predicts hidden charges | ❌ | ❌ | ✅ |
| Surge & weather aware | ❌ | ❌ | ✅ |
| Offer genuineness score | ❌ | ❌ | ✅ |
| Powered by ML | ❌ | ❌ | ✅ |
| Reorder prediction | ❌ | ❌ | ✅ |

> *"Competitors show you the sticker price. CartIQ shows you the checkout price."*

---

## 👨‍💻 Author

**Your Name**
3rd Year CS Student | ML & Data Enthusiast
[LinkedIn](https://linkedin.com/in/yourprofile) • [GitHub](https://github.com/yourusername)

---

## 📌 Acknowledgements

- Hidden charge data modeled from real user complaints and news reporting (Inc42, Moneylife)
- Synthetic data generation technique inspired by industry-standard privacy-preserving ML practices
- Built as part of a 75-day summer learning challenge

---

*If this project helped you or gave you ideas — drop a ⭐ on GitHub. It means a lot!*
