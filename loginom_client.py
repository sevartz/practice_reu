
import requests
import config
import mock_data


def call_service(method: str, user_id: int) -> list[dict]:
    if config.MOCK_LOGINOM:
        return mock_data.get_rows(method, user_id)

    url = f"{config.LOGINOM_BASE_URL}/lgi/rest/{config.LOGINOM_PACKAGE}/{method}"
    payload = {"Variables": {"user_id": str(user_id)}}

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status() 

    data = response.json()
    return data.get("DataSet", {}).get("Rows", [])


def user_exists(user_id: int) -> bool:
    rows = call_service("CheckUserID", user_id)
    if not rows:
        return False
    return rows[0].get("user_exists", 0) == 1


def get_user_history(user_id: int) -> list[dict]:
    return call_service("GetUserHistory", user_id)


def get_anchor_products(user_id: int) -> list[dict]:
    return call_service("GetAnchorProducts", user_id)


def get_purchase_rhythm(user_id: int) -> dict:
    rows = call_service("GetPurchaseRhythm", user_id)
    return rows[0] if rows else {}


def get_order_timing(user_id: int) -> list[dict]:
    return call_service("GetOrderTiming", user_id)


def get_cart_order(user_id: int) -> list[dict]:
    return call_service("GetCardOrder", user_id)
