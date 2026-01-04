import os
import random
import time


def human_pause(min_s=0.3, max_s=1.2):
    """Pequena pausa aleatoria para simular tempo humano entre acoes."""
    time.sleep(random.uniform(min_s, max_s))


def compute_wait_seconds():
    """Calcula intervalo em segundos baseado no .env com jitter de +/-20%."""
    try:
        base_minutes = float(os.getenv("INTERVALO_BUSCA_MINUTOS", "5"))
    except ValueError:
        base_minutes = 5.0
    jitter_factor = random.uniform(0.8, 1.2)
    seconds = max(30, int(base_minutes * 60 * jitter_factor))
    return seconds, base_minutes, jitter_factor


def is_support_blocked(driver):
    """Detecta tela de bloqueio 'The requested URL was rejected'."""
    page = driver.page_source
    if "The requested URL was rejected" in page or "Your support ID is" in page:
        return True
    return False
