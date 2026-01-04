import os

from dotenv import load_dotenv
import automacao_lib
import pytest
import requests

load_dotenv()


def test_compute_wait_seconds_with_env_and_jitter_low(monkeypatch):
    monkeypatch.setenv("INTERVALO_BUSCA_MINUTOS", "5")
    monkeypatch.setattr(automacao_lib.random, "uniform", lambda a, b: 0.8)
    seconds, base, jitter = automacao_lib.compute_wait_seconds()
    assert base == 5.0
    assert jitter == 0.8
    assert seconds == 240  # 5min * 60 * 0.8


def test_compute_wait_seconds_with_env_and_jitter_high(monkeypatch):
    monkeypatch.setenv("INTERVALO_BUSCA_MINUTOS", "2")
    monkeypatch.setattr(automacao_lib.random, "uniform", lambda a, b: 1.2)
    seconds, base, jitter = automacao_lib.compute_wait_seconds()
    assert base == 2.0
    assert jitter == 1.2
    assert seconds == 144  # 2min * 60 * 1.2


def test_compute_wait_seconds_invalid_env(monkeypatch):
    monkeypatch.setenv("INTERVALO_BUSCA_MINUTOS", "invalid")
    monkeypatch.setattr(automacao_lib.random, "uniform", lambda a, b: 1.0)
    seconds, base, jitter = automacao_lib.compute_wait_seconds()
    assert base == 5.0
    assert jitter == 1.0
    assert seconds == 300


def test_human_pause_uses_random_and_sleep(monkeypatch):
    monkeypatch.setattr(automacao_lib.random, "uniform", lambda a, b: 0.42)
    slept = []
    monkeypatch.setattr(automacao_lib.time, "sleep", slept.append)
    automacao_lib.human_pause()
    assert slept == [0.42]


def test_is_support_blocked_detects_blocked_and_ok():
    class Dummy:
        def __init__(self, page_source):
            self.page_source = page_source

    blocked = Dummy("The requested URL was rejected. Your support ID is: 123")
    ok = Dummy("<html><body>normal</body></html>")
    assert automacao_lib.is_support_blocked(blocked) is True
    assert automacao_lib.is_support_blocked(ok) is False


@pytest.mark.integration
def test_send_telegram_test_message():
    token = os.getenv("TELEGRAM_TEST_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_TEST_CHAT_ID") or os.getenv("TELEGRAM_ID")
    if not token or not chat_id:
        pytest.skip(
            "Defina TELEGRAM_TEST_TOKEN/TELEGRAM_TEST_CHAT_ID "
            "ou TELEGRAM_TOKEN/TELEGRAM_ID para rodar o teste de integracao com Telegram."
        )

    resp = requests.get(
        f"https://api.telegram.org/bot{token}/sendMessage",
        params={"chat_id": chat_id, "text": "Mensagem de teste do bot CITA (automated test)"},
        timeout=10,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("ok") is True
