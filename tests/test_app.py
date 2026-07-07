import os
import sys
from pathlib import Path

os.environ["MOCK_LOGINOM"] = "1"

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import llm_client
import app as app_module


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(llm_client, "ask",
                        lambda system, user, **kw: "Тестовый ответ помощника.")
    import config
    monkeypatch.setattr(config, "CACHE_DB", str(tmp_path / "t.db"))
    import cache
    cache.init_db()

    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def login(client):
    return client.post("/login", data={"user_id": "1"})


def test_index_open(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Личный кабинет".encode() in r.data


def test_login_not_a_number(client):
    r = client.post("/login", data={"user_id": "abc"})
    assert "должен быть целым числом".encode() in r.data


def test_history_table_and_charts(client):
    login(client)
    r = client.get("/history")
    assert r.status_code == 200
    assert "Original Beef Jerky".encode() in r.data
    assert "topChart".encode() in r.data      
    assert "depChart".encode() in r.data    


def test_feature_anchors(client):
    login(client)
    r = client.post("/analysis/anchors")
    assert r.status_code == 200
    assert "Original Beef Jerky".encode() in r.data  
    assert "Тестовый ответ".encode() in r.data
    assert "повторных покупок".encode() in r.data   


def test_feature_rhythm(client):
    login(client)
    r = client.post("/analysis/rhythm")
    assert r.status_code == 200
    assert "heatmap".encode() in r.data               
    assert "дней между заказами".encode() in r.data    
    assert "Тестовый ответ".encode() in r.data


def test_feature_cart(client):
    login(client)
    r = client.post("/analysis/cart")
    assert r.status_code == 200
    assert "приоритет".encode() in r.data
    assert "импульс".encode() in r.data
    assert "Тестовый ответ".encode() in r.data


def test_api_history_requires_login(client):
    r = client.post("/api/history")
    assert r.status_code == 403


def test_cache_second_call_uses_cache(client, monkeypatch):
    calls = {"n": 0}

    def counting_ask(system, user, **kw):
        calls["n"] += 1
        return "Ответ один раз."

    monkeypatch.setattr(llm_client, "ask", counting_ask)

    login(client)
    client.post("/analysis/anchors")   
    client.post("/analysis/anchors")  
    assert calls["n"] == 1
