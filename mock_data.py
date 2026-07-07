_HISTORY = [
    {"product_name": "Original Beef Jerky", "aisle": "popcorn jerky",
     "department": "snacks", "department_rus": "снэки", "order_count": 10},
    {"product_name": "Soda", "aisle": "soft drinks",
     "department": "beverages", "department_rus": "напитки, соки", "order_count": 10},
    {"product_name": "Pistachios", "aisle": "nuts seeds dried fruit",
     "department": "snacks", "department_rus": "снэки", "order_count": 9},
    {"product_name": "Organic String Cheese", "aisle": "packaged cheese",
     "department": "dairy eggs", "department_rus": "молочные продукты, яйца", "order_count": 8},
    {"product_name": "Cinnamon Toast Crunch", "aisle": "cereal",
     "department": "breakfast", "department_rus": "сухие завтраки", "order_count": 3},
    {"product_name": "Zero Calorie Cola", "aisle": "soft drinks",
     "department": "beverages", "department_rus": "напитки, соки", "order_count": 3},
    {"product_name": "Aged White Cheddar Popcorn", "aisle": "popcorn jerky",
     "department": "snacks", "department_rus": "снэки", "order_count": 2},
    {"product_name": "Bag of Organic Bananas", "aisle": "fresh fruits",
     "department": "produce", "department_rus": "овощи, фрукты, зелень", "order_count": 2},
    {"product_name": "Organic Half & Half", "aisle": "cream",
     "department": "dairy eggs", "department_rus": "молочные продукты, яйца", "order_count": 2},
    {"product_name": "XL Pick-A-Size Paper Towel Rolls", "aisle": "paper goods",
     "department": "household", "department_rus": "товары для дома", "order_count": 2},
]
_ANCHORS = [
    {"product_name": "Original Beef Jerky", "department_rus": "снэки",
     "times_bought": 12, "times_reordered": 11, "reorder_rate": 92},
    {"product_name": "Soda", "department_rus": "напитки, соки",
     "times_bought": 12, "times_reordered": 11, "reorder_rate": 92},
    {"product_name": "Organic String Cheese", "department_rus": "молочные продукты, яйца",
     "times_bought": 9, "times_reordered": 8, "reorder_rate": 89},
    {"product_name": "Pistachios", "department_rus": "снэки",
     "times_bought": 10, "times_reordered": 8, "reorder_rate": 80},
    {"product_name": "Bag of Organic Bananas", "department_rus": "овощи, фрукты, зелень",
     "times_bought": 5, "times_reordered": 3, "reorder_rate": 60},
]
_RHYTHM = [
    {"avg_days": 9.3, "min_days": 2, "max_days": 30, "orders_count": 18},
]

_TIMING = [
    {"order_dow": 0, "order_hour_of_day": 10, "orders_count": 3},
    {"order_dow": 0, "order_hour_of_day": 11, "orders_count": 4},
    {"order_dow": 0, "order_hour_of_day": 14, "orders_count": 2},
    {"order_dow": 1, "order_hour_of_day": 9, "orders_count": 1},
    {"order_dow": 3, "order_hour_of_day": 18, "orders_count": 2},
    {"order_dow": 5, "order_hour_of_day": 20, "orders_count": 1},
    {"order_dow": 6, "order_hour_of_day": 10, "orders_count": 3},
    {"order_dow": 6, "order_hour_of_day": 11, "orders_count": 2},
]

_CART_ORDER = [
    {"product_name": "Bag of Organic Bananas", "department_rus": "овощи, фрукты, зелень",
     "times_bought": 5, "avg_position": 1.4, "times_first": 4},
    {"product_name": "Organic String Cheese", "department_rus": "молочные продукты, яйца",
     "times_bought": 9, "avg_position": 2.1, "times_first": 3},
    {"product_name": "Soda", "department_rus": "напитки, соки",
     "times_bought": 12, "avg_position": 3.6, "times_first": 2},
    {"product_name": "Original Beef Jerky", "department_rus": "снэки",
     "times_bought": 12, "avg_position": 6.8, "times_first": 0},
    {"product_name": "Aged White Cheddar Popcorn", "department_rus": "снэки",
     "times_bought": 4, "avg_position": 9.5, "times_first": 0},
]


def get_rows(method: str, user_id: int) -> list[dict]:
    if method == "CheckUserID":
        exists = 1 if user_id and int(user_id) > 0 else 0
        return [{"user_exists": exists}]

    if method == "GetUserHistory":
        return _HISTORY

    if method == "GetAnchorProducts":
        return _ANCHORS

    if method == "GetPurchaseRhythm":
        return _RHYTHM

    if method == "GetOrderTiming":
        return _TIMING

    if method == "GetCartOrder":
        return _CART_ORDER

    return []
