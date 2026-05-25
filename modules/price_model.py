import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os

# ─── 1. LOAD DATA ───────────────────────────────────────────────────────────
print("📦 Loading dataset...")
df = pd.read_csv('data/synthetic_orders.csv')
print(f"✅ Loaded {len(df)} rows, {len(df.columns)} columns")

# ─── 2. FEATURE ENGINEERING ─────────────────────────────────────────────────
print("\n🔧 Engineering features...")

# City surge multiplier (real-world logic)
city_multiplier = {
    'Mumbai': 1.3,
    'Delhi': 1.2,
    'Bangalore': 1.25,
    'Hyderabad': 1.1,
    'Pune': 1.05,
    'Chennai': 1.1,
    'Kolkata': 1.0,
    'Lucknow': 0.9
}
df['city_multiplier'] = df['city'].map(city_multiplier)

# Time-based features
df['is_peak_hour'] = df['hour_of_day'].apply(lambda x: 1 if x in [12,13,19,20,21] else 0)
df['is_late_night'] = df['hour_of_day'].apply(lambda x: 1 if x >= 22 or x <= 5 else 0)

# Encode categorical columns
le_platform = LabelEncoder()
le_weather  = LabelEncoder()
le_category = LabelEncoder()

df['platform_enc'] = le_platform.fit_transform(df['platform'])
df['weather_enc']  = le_weather.fit_transform(df['weather'])
df['category_enc'] = le_category.fit_transform(df['category'])

print(f"✅ Platforms encoded: {dict(zip(le_platform.classes_, le_platform.transform(le_platform.classes_)))}")
print(f"✅ Weather encoded:   {dict(zip(le_weather.classes_,  le_weather.transform(le_weather.classes_)))}")

# ─── 3. DEFINE FEATURES & TARGET ────────────────────────────────────────────
features = [
    'cart_value',
    'num_items',
    'platform_enc',
    'weather_enc',
    'category_enc',
    'hour_of_day',
    'is_weekend',
    'is_peak_hour',
    'is_late_night',
    'city_multiplier',
]

target = 'final_price'

X = df[features]
y = df[target]

print(f"\n📊 Features used: {features}")
print(f"🎯 Target: {target}")

# ─── 4. TRAIN TEST SPLIT ────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n🔀 Train size: {len(X_train)} | Test size: {len(X_test)}")

# ─── 5. TRAIN MODEL ─────────────────────────────────────────────────────────
print("\n🤖 Training Random Forest model...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("✅ Model trained!")

# ─── 6. EVALUATE ────────────────────────────────────────────────────────────
print("\n📈 Evaluating model...")
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae  = mean_absolute_error(y_test, y_pred)
r2   = r2_score(y_test, y_pred)

print(f"\n{'='*40}")
print(f"  R² Score  : {r2:.4f}  (1.0 = perfect)")
print(f"  RMSE      : ₹{rmse:.2f} (avg error)")
print(f"  MAE       : ₹{mae:.2f} (avg absolute error)")
print(f"{'='*40}")

# ─── 7. FEATURE IMPORTANCE ──────────────────────────────────────────────────
print("\n🔍 Feature importance (what affects price most):")
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for _, row in importance.iterrows():
    bar = '█' * int(row['importance'] * 50)
    print(f"  {row['feature']:20s} {bar} {row['importance']:.4f}")

# ─── 8. SAVE MODEL & ENCODERS ───────────────────────────────────────────────
print("\n💾 Saving model and encoders...")
os.makedirs('models', exist_ok=True)

joblib.dump(model,       'models/price_predictor.pkl')
joblib.dump(le_platform, 'models/le_platform.pkl')
joblib.dump(le_weather,  'models/le_weather.pkl')
joblib.dump(le_category, 'models/le_category.pkl')
joblib.dump(features,    'models/feature_names.pkl')
joblib.dump(city_multiplier, 'models/city_multiplier.pkl')

print("✅ Saved: models/price_predictor.pkl")
print("✅ Saved: models/le_platform.pkl")
print("✅ Saved: models/le_weather.pkl")
print("✅ Saved: models/le_category.pkl")

# ─── 9. TEST WITH A REAL EXAMPLE ────────────────────────────────────────────
print("\n🧪 Live prediction test:")
print("─" * 40)

test_cases = [
    {'cart_value': 299, 'platform': 'Zepto',    'weather': 'Rainy', 'hour': 21, 'city': 'Mumbai'},
    {'cart_value': 299, 'platform': 'Blinkit',  'weather': 'Rainy', 'hour': 21, 'city': 'Mumbai'},
    {'cart_value': 299, 'platform': 'Instamart', 'weather': 'Rainy', 'hour': 21, 'city': 'Mumbai'},
]

print(f"Cart value: ₹299 | Rainy | 9pm | Mumbai\n")
for tc in test_cases:
    sample = pd.DataFrame([{
        'cart_value':      tc['cart_value'],
        'num_items':       5,
        'platform_enc':    le_platform.transform([tc['platform']])[0],
        'weather_enc':     le_weather.transform([tc['weather']])[0],
        'category_enc':    le_category.transform(['Grocery'])[0],
        'hour_of_day':     tc['hour'],
        'is_weekend':      0,
        'is_peak_hour':    1,
        'is_late_night':   0,
        'city_multiplier': city_multiplier[tc['city']],
    }])
    pred = model.predict(sample)[0]
    hidden = pred - tc['cart_value']
    print(f"  {tc['platform']:10s} → Predicted: ₹{pred:.0f}  (hidden charges: ₹{hidden:.0f})")

print("\n✅ Day 2 Complete! Model ready for Streamlit.")
