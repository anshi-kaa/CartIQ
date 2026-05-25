import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

n = 5000
platforms = ['Zepto', 'Blinkit', 'Instamart']
categories = ['Grocery', 'Dairy', 'Snacks', 'Beverages', 'Personal Care', 'Fruits & Veg', 'Frozen', 'Medicines']
weather_opts = ['Clear', 'Rainy', 'Cloudy', 'Hot']
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Lucknow']

def generate_order():
    platform = random.choice(platforms)
    city = random.choice(cities)
    hour = random.choices(range(24), weights=[1,0.5,0.5,0.5,0.5,1,2,4,6,6,5,6,7,6,5,5,5,6,7,7,6,5,4,3])[0]
    is_weekend = random.random() < 0.3
    weather_cond = random.choice(weather_opts)
    num_items = random.randint(1, 14)
    category = random.choice(categories)
    cart_value = round(random.uniform(80, 1200), 2)

    if platform == 'Zepto':
        base_delivery = 0 if cart_value > 199 else round(random.uniform(15, 30), 2)
        handling_fee = round(random.uniform(3, 12), 2)
        surge = round(random.uniform(10, 25), 2) if weather_cond == 'Rainy' else 0
        small_cart_fee = 20 if cart_value < 99 else 0
        platform_discount = round(random.uniform(0, 60), 2) if random.random() < 0.4 else 0
    elif platform == 'Blinkit':
        base_delivery = 0 if cart_value > 299 else round(random.uniform(20, 40), 2)
        handling_fee = round(random.uniform(5, 15), 2)
        surge = round(random.uniform(15, 30), 2) if weather_cond == 'Rainy' else 0
        small_cart_fee = 25 if cart_value < 149 else 0
        platform_discount = round(random.uniform(0, 80), 2) if random.random() < 0.35 else 0
    else:
        base_delivery = 0 if cart_value > 249 else round(random.uniform(18, 35), 2)
        handling_fee = round(random.uniform(4, 10), 2)
        surge = round(random.uniform(12, 22), 2) if weather_cond == 'Rainy' else 0
        small_cart_fee = 15 if cart_value < 119 else 0
        platform_discount = round(random.uniform(0, 70), 2) if random.random() < 0.38 else 0

    night_surge = round(random.uniform(8, 20), 2) if hour >= 22 or hour <= 5 else 0
    peak_surge = round(random.uniform(5, 15), 2) if hour in [12, 13, 19, 20, 21] else 0

    total_hidden = round(handling_fee + surge + small_cart_fee + night_surge + peak_surge, 2)
    final_price = round(max(cart_value + base_delivery + total_hidden - platform_discount, cart_value * 0.85), 2)

    has_offer = random.random() < 0.55
    if has_offer:
        offer_type = random.choice(['Cashback', 'Free Delivery', 'Flat Discount', 'Free Gift', 'BOGO'])
        offer_value = round(random.uniform(10, 150), 2)
        dark = 0
        if offer_value > 100 and platform_discount < 20: dark += 0.4
        if offer_type == 'Cashback' and random.random() < 0.5: dark += 0.3
        if offer_type == 'Free Gift' and random.random() < 0.6: dark += 0.3
        offer_genuine = round(max(0, min(1, 1 - dark + random.uniform(-0.1, 0.1))), 2)
    else:
        offer_type = 'None'
        offer_value = 0.0
        offer_genuine = None

    return {
        'order_id': f'ORD{random.randint(100000,999999)}',
        'platform': platform,
        'city': city,
        'category': category,
        'num_items': num_items,
        'cart_value': cart_value,
        'hour_of_day': hour,
        'is_weekend': int(is_weekend),
        'weather': weather_cond,
        'base_delivery_fee': base_delivery,
        'handling_fee': handling_fee,
        'surge_charge': surge,
        'small_cart_fee': small_cart_fee,
        'night_surge': night_surge,
        'peak_surge': peak_surge,
        'total_hidden_charges': total_hidden,
        'platform_discount': platform_discount,
        'final_price': final_price,
        'has_offer': int(has_offer),
        'offer_type': offer_type,
        'offer_value': offer_value,
        'offer_genuine_score': offer_genuine,
        'is_late_night_order': int(hour >= 22 or hour <= 5),
        'is_bulk_order': int(num_items >= 8),
        'is_health_category': int(category in ['Fruits & Veg', 'Dairy', 'Medicines']),
        'days_since_last_order': random.randint(1, 30),
    }

rows = [generate_order() for _ in range(n)]
df = pd.DataFrame(rows)
df.to_csv('/home/claude/synthetic_orders.csv', index=False)

print(f"Dataset: {len(df)} rows x {len(df.columns)} cols")
print("\nPlatform stats:")
print(df.groupby('platform')[['cart_value','total_hidden_charges','platform_discount','final_price']].mean().round(2))
print("\nOffer types:")
print(df['offer_type'].value_counts())
print("\nSample row:")
print(df.iloc[0].to_dict())
