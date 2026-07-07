import loginom_client
import llm_client
import prompts
import cache

JUNK_DEPARTMENTS = {"snacks", "beverages"}

DOW_RUS = ["воскресенье", "понедельник", "вторник", "среда",
           "четверг", "пятница", "суббота"]


def _ask_with_cache(service: str, user_id: int, system_prompt: str, user_prompt: str):
    """Спросить LLM, но сначала заглянуть в кэш. Возвращает (текст, from_cache)."""
    key = cache.make_key(service, user_id, user_prompt)

    cached = cache.get(key)
    if cached is not None:
        return cached, True

    answer = llm_client.ask(system_prompt, user_prompt)
    cache.put(key, service, user_id, user_prompt, answer)
    return answer, False


def build_products_text(products: list[dict]) -> str:
    lines = []
    for p in products:
        lines.append(
            f"- {p.get('product_name')} "
            f"({p.get('department_rus')}, куплено {p.get('order_count')} раз)"
        )
    return "\n".join(lines)


def analyze_products(products: list[dict]) -> dict:
    by_department = {}
    top_labels = []
    top_values = []
    junk_count = 0
    healthy_count = 0

    for p in products:
        name = p.get("product_name", "—")
        dep_rus = p.get("department_rus", "прочее")
        dep_en = (p.get("department") or "").lower()
        count = int(p.get("order_count", 0))

        top_labels.append(name)
        top_values.append(count)

        by_department[dep_rus] = by_department.get(dep_rus, 0) + count
        if dep_en in JUNK_DEPARTMENTS:
            junk_count += count
        else:
            healthy_count += count

    total = junk_count + healthy_count
    junk_share = round(junk_count / total * 100) if total else 0

    return {
        "by_department": by_department,
        "top_labels": top_labels,
        "top_values": top_values,
        "junk_count": junk_count,
        "healthy_count": healthy_count,
        "junk_share": junk_share,
    }


def get_history_page(user_id: int) -> dict:
    products = loginom_client.get_user_history(user_id)
    if not products:
        return {"products": [], "analysis": None}

    return {"products": products, "analysis": analyze_products(products)}



def _anchors_text(anchors: list[dict]) -> str:
    lines = []
    for a in anchors:
        lines.append(
            f"- {a.get('product_name')} "
            f"({a.get('department_rus')}, брал {a.get('times_bought')} раз, "
            f"повторных {a.get('reorder_rate')}%)"
        )
    return "\n".join(lines)


def feature_anchors(user_id: int) -> dict:
    anchors = loginom_client.get_anchor_products(user_id)
    if not anchors:
        return {"error": "Нет данных о повторных покупках"}

    rates = [int(a.get("reorder_rate", 0)) for a in anchors]
    reorder_share = round(sum(rates) / len(rates)) if rates else 0

    prompt_text = prompts.anchors_prompt(_anchors_text(anchors), reorder_share)
    answer, from_cache = _ask_with_cache("anchors", user_id, prompts.SYSTEM, prompt_text)
    return {"anchors": anchors, "reorder_share": reorder_share,
            "prompt_text": prompt_text, "answer": answer, "from_cache": from_cache}


def build_timing_grid(timing: list[dict]) -> dict:

    matrix = [[0] * 24 for _ in range(7)]
    points = []
    for t in timing:
        dow = int(t.get("order_dow", 0))
        hour = int(t.get("order_hour_of_day", 0))
        count = int(t.get("orders_count", 0))
        if 0 <= dow <= 6 and 0 <= hour <= 23:
            matrix[dow][hour] += count
            points.append({"x": hour, "y": dow, "v": count})

    top_dow, top_hour, best = 0, 12, -1
    dow_totals = [sum(row) for row in matrix]
    if any(dow_totals):
        top_dow = dow_totals.index(max(dow_totals))
    for t in timing:
        if int(t.get("orders_count", 0)) > best:
            best = int(t.get("orders_count", 0))
            top_hour = int(t.get("order_hour_of_day", 12))

    return {"matrix": matrix, "points": points,
            "top_dow": top_dow, "top_hour": top_hour}


def feature_rhythm(user_id: int) -> dict:
    rhythm = loginom_client.get_purchase_rhythm(user_id)
    timing = loginom_client.get_order_timing(user_id)
    if not rhythm and not timing:
        return {"error": "Нет данных о заказах клиента"}

    grid = build_timing_grid(timing)
    avg_days = float(rhythm.get("avg_days", 0) or 0)
    top_day_human = DOW_RUS[grid["top_dow"]]

    prompt_text = prompts.rhythm_prompt(avg_days, top_day_human, grid["top_hour"])
    answer, from_cache = _ask_with_cache("rhythm", user_id, prompts.SYSTEM, prompt_text)
    return {"rhythm": rhythm, "avg_days": round(avg_days, 1),
            "top_day_human": top_day_human, "top_hour": grid["top_hour"],
            "heat_points": grid["points"], "dow_rus": DOW_RUS,
            "prompt_text": prompt_text, "answer": answer, "from_cache": from_cache}


def _cart_text(items: list[dict]) -> str:
    lines = []
    for c in items:
        lines.append(
            f"- {c.get('product_name')} "
            f"({c.get('department_rus')}, средняя позиция в корзине "
            f"{c.get('avg_position')}, брал {c.get('times_bought')} раз)"
        )
    return "\n".join(lines)


def split_cart(cart: list[dict]) -> dict:
    must_have = [c for c in cart if float(c.get("avg_position", 99)) <= 3]
    impulse = [c for c in cart if float(c.get("avg_position", 99)) > 3]
    return {"must_have": must_have, "impulse": impulse}


def feature_cart(user_id: int) -> dict:
    cart = loginom_client.get_cart_order(user_id)
    if not cart:
        return {"error": "Нет данных о порядке добавления в корзину"}

    split = split_cart(cart)
    must_text = _cart_text(split["must_have"]) or "— (нет явных приоритетов)"
    impulse_text = _cart_text(split["impulse"]) or "— (нет импульсных покупок)"

    prompt_text = prompts.cart_prompt(must_text, impulse_text)
    answer, from_cache = _ask_with_cache("cart", user_id, prompts.SYSTEM, prompt_text)
    return {"must_have": split["must_have"], "impulse": split["impulse"],
            "prompt_text": prompt_text, "answer": answer, "from_cache": from_cache}
