from flask import Flask, request, session, jsonify, render_template, redirect, url_for

import config
import cache
import loginom_client
import business_rules

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

cache.init_db()


@app.route("/")
def index():
    return render_template("index.html", user_id=session.get("user_id"))


@app.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id", "").strip()

    if not user_id.isdigit():
        return render_template("index.html", user_id=None,
                               error="user_id должен быть целым числом")

    try:
        if not loginom_client.user_exists(int(user_id)):
            return render_template("index.html", user_id=None,
                                   error=f"Клиент с user_id={user_id} не найден в базе")
    except Exception as e:
        return render_template("index.html", user_id=None,
                               error=f"Не удалось проверить user_id (Loginom недоступен): {e}")

    session["user_id"] = int(user_id)
    return redirect(url_for("index"))


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/history")
def history():
    user_id = session.get("user_id")
    if not user_id:
        return render_template("index.html", user_id=None,
                               error="Сначала авторизуйтесь по user_id")

    try:
        data = business_rules.get_history_page(user_id)
    except Exception as e:
        return render_template("history.html", user_id=user_id,
                               error=f"Ошибка при получении данных: {e}")

    if not data["products"]:
        return render_template("history.html", user_id=user_id,
                               error="Loginom вернул пустой список товаров")

    return render_template("history.html", user_id=user_id, error=None, **data)


@app.route("/analysis")
def analysis():
    user_id = session.get("user_id")
    if not user_id:
        return render_template("index.html", user_id=None,
                               error="Сначала авторизуйтесь по user_id")
    return render_template("analysis.html", user_id=user_id)


@app.route("/analysis/anchors", methods=["POST"])
def analysis_anchors():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))
    result = business_rules.feature_anchors(user_id)
    return render_template("analysis.html", user_id=user_id,
                           active="anchors", anchors=result)


@app.route("/analysis/rhythm", methods=["POST"])
def analysis_rhythm():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))
    result = business_rules.feature_rhythm(user_id)
    return render_template("analysis.html", user_id=user_id,
                           active="rhythm", rhythm=result)


@app.route("/analysis/cart", methods=["POST"])
def analysis_cart():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))
    result = business_rules.feature_cart(user_id)
    return render_template("analysis.html", user_id=user_id,
                           active="cart", cart=result)


@app.route("/api/history", methods=["POST"])
def api_history():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Сначала авторизуйтесь"}), 403
    try:
        data = business_rules.get_history_page(user_id)
        return jsonify({"user_id": user_id, **data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
