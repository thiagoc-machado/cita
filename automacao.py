from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import cv2
from dotenv import load_dotenv
import pytesseract
import time
import keyboard
from datetime import datetime
import requests
import sys
import os
from shutil import which
from os import path
from automacao_lib import human_pause, compute_wait_seconds, is_support_blocked
from pathlib import Path

load_dotenv()

exit_key = False

print('selecione o tipo de serviço')
print('1 - busca e marcação padrão')
print('2 - carta de concordancia (apenas avisar no Telegram)')
service_choice = input().strip()

person = None
doc = None
if service_choice == '1':
    print(f'selecione 1 para {os.getenv("NOMBRE_1")}')
    print(f'selecione 2 para {os.getenv("NOMBRE_2")}')
    person = input().strip()
    print('selecione 1 para NIE')
    print('selecione 2 para Passaporte')
    doc = input().strip()

bot_token = os.getenv("TELEGRAM_TOKEN")
bot_chat_id = os.getenv("TELEGRAM_ID")

if service_choice == '1':
    if person == '1':
        print('Selecionado ')
        DATA_MARCADO = os.getenv("DATA_MARCADO_1")
        DATA_INICIAL = os.getenv("DATA_INICIAL_1")
        NOMBRE = os.getenv("NOMBRE_1")
        APELLIDO1 = os.getenv("APELLIDO1_1")
        APELLIDO2 = os.getenv("APELLIDO2_1")
        FECHA_NASC = os.getenv("FECHA_NASC_1")
        TELEFONO = os.getenv("TELEFONO_1")
        EMAIL = os.getenv("EMAIL_1")
        if doc == '1':
            print('Selecionado NIE')
            DOCUMENTO = os.getenv("NIE_1")
        elif doc == '2':
            print('Selecionado Passaporte')
            DOCUMENTO = os.getenv("PASSAPORTE_1")
        else:
            print('Opção inválida')
            exit()

    elif person == '2':
        print('Selecionado ')
        DATA_MARCADO = os.getenv("DATA_MARCADO_2")
        DATA_INICIAL = os.getenv("DATA_INICIAL_2")
        NOMBRE = os.getenv("NOMBRE_2")
        APELLIDO1 = os.getenv("APELLIDO1_2")
        APELLIDO2 = os.getenv("APELLIDO2_2")
        FECHA_NASC = os.getenv("FECHA_NASC_2")
        TELEFONO = os.getenv("TELEFONO_2")
        EMAIL = os.getenv("EMAIL_2")
        if doc == '1':
            print('Selecionado NIE')
            DOCUMENTO = os.getenv("NIE_2")
        elif doc == '2':
            print('Selecionado Passaporte')
            DOCUMENTO = os.getenv("PASSAPORTE_2")
        else:
            print('Opção inválida')
            exit()
    else:
        print('Opção inválida')
        exit()

if service_choice == '2':
    # Modo concordancia: usa chaves simples do .env e não pergunta mais nada.
    NOMBRE = os.getenv("NOMBRE")
    DOCUMENTO = os.getenv("DNI")
    if not NOMBRE or not DOCUMENTO:
        print("Preencha NOMBRE e DNI no .env para usar o modo concordancia.")
        sys.exit(1)
    DATA_MARCADO = ""
    DATA_INICIAL = ""
    APELLIDO1 = ""
    APELLIDO2 = ""
    FECHA_NASC = ""
    TELEFONO = ""
    EMAIL = ""

def send_message_to_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            "chat_id": bot_chat_id,
            "text": text
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Erro ao enviar mensagem para o Telegram: {response.text}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")


def send_image_to_telegram(image_path):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        with open(image_path, 'rb') as image_file:
            files = {
                "photo": image_file
            }
            data = {
                "chat_id": bot_chat_id
            }
            response = requests.post(url, files=files, data=data)
            if response.status_code != 200:
                print(
                    f"Erro ao enviar imagem para o Telegram: {response.text}")
    except Exception as e:
        print(f"Erro ao enviar imagem para o Telegram: {e}")







def click_by_text_or_value(driver, wait, texts):
    """Tenta clicar em um botao/input pelo texto visivel ou valor, com fallback em JS click."""
    for text in texts:
        normalized = text.lower()
        locator_candidates = [
            (By.XPATH, f"//button[normalize-space()='{text}']"),
            (By.XPATH, f"//button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{normalized}')]") ,
            (By.XPATH, f"//input[@type='submit' and @value='{text}']"),
            (By.XPATH, f"//input[@type='submit' and contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{normalized}')]"),
            (By.XPATH, f"//input[@type='button' and contains(translate(@value, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{normalized}')]"),
            (By.XPATH, "//*[@id='btnAceptar']"),
        ]
        for locator in locator_candidates:
            try:
                elem = wait.until(EC.element_to_be_clickable(locator))
                try:
                    elem.click()
                    human_pause()
                    return True
                except Exception:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                    driver.execute_script("arguments[0].click();", elem)
                    human_pause()
                    return True
            except Exception:
                continue
    return False


def click_xpath(driver, wait, xpath):
    """Clica por XPath com fallback em scroll + JS."""
    try:
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        try:
            elem.click()
        except Exception:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            driver.execute_script("arguments[0].click();", elem)
        human_pause()
        return True
    except Exception:
        return False

def select_option(wait, locator_candidates, option_text):
    """Seleciona uma opção em um <select> tentando vários localizadores."""
    for locator in locator_candidates:
        try:
            select_elem = wait.until(EC.element_to_be_clickable(locator))
            Select(select_elem).select_by_visible_text(option_text)
            human_pause()
            return True
        except Exception:
            continue
    return False


def build_chrome_options():
    """Cria opções do Chrome procurando o binário caso o sistema não exponha por padrão."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    binary = os.getenv("CHROME_BINARY")
    if not binary:
        for candidate in (
            "google-chrome",
            "chromium-browser",
            "chromium",
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
            "/snap/bin/chromium",
            "/snap/bin/chromium-browser",
        ):
            found = which(candidate)
            if found:
                binary = found
                break
    if binary:
        chrome_options.binary_location = binary
    return chrome_options


def build_chrome_service():
    """Seleciona o chromedriver adequado: variável de ambiente, snap ou download."""
    driver_path = os.getenv("CHROMEDRIVER_BINARY")
    if driver_path and path.exists(driver_path):
        return Service(executable_path=driver_path)

    snap_driver = "/snap/bin/chromium.chromedriver"
    if path.exists(snap_driver):
        return Service(executable_path=snap_driver)

    return Service(ChromeDriverManager().install())






def detect_unavailable_final(navegador):
    """Verifica se a tela final exibe mensagem de 'no hay citas' buscando direto no HTML."""
    try:
        page = navegador.page_source
        normalized = page.lower().replace("\xa0", " ")
        alvo = "en este momento no hay citas disponibles"

        found_page = alvo in normalized

        # Tenta capturar textos visíveis para log
        container_text = ""
        msg_info_text = ""
        try:
            container_text = navegador.find_element(By.ID, "container").text.strip()
        except Exception:
            pass
        try:
            msg_info_text = navegador.find_element(By.CSS_SELECTOR, "p.mf-msg__info").text.strip()
        except Exception:
            pass

        # Logs de depuração (mantém curtos)
        print(f"[DEBUG] detect_unavailable_final found_page={found_page}")
        if container_text:
            print(f"[DEBUG] container_text={container_text[:200]}")
        if msg_info_text:
            print(f"[DEBUG] msg_info_text={msg_info_text[:200]}")

        return found_page or (alvo in container_text.lower()) or (alvo in msg_info_text.lower())
    except Exception:
        print("[DEBUG] detect_unavailable_final exception")
        return False


def assert_not_blocked(navegador, contexto=""):
    """Levanta exceção se a página mostrar bloqueio 'requested URL rejected'."""
    if is_support_blocked(navegador):
        msg = "Bloqueio detectado"
        if contexto:
            msg += f" ({contexto})"
        print(f"[DEBUG] {msg}")
        raise Exception(msg)


def dump_debug_page(navegador, label="concordancia"):
    """Salva HTML e screenshot para depuração quando o fluxo falha."""
    try:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        debug_dir = Path("debug")
        debug_dir.mkdir(exist_ok=True)
        html_path = debug_dir / f"debug_{label}_{ts}.html"
        png_path = debug_dir / f"debug_{label}_{ts}.png"
        html_path.write_text(navegador.page_source, encoding="utf-8", errors="ignore")
        try:
            navegador.save_screenshot(str(png_path))
        except Exception:
            pass
        print(f"[DEBUG] Dump salvo: {html_path} {png_path}")
    except Exception as e:
        print(f"[DEBUG] Falha ao salvar dump: {e}")


def executar_fluxo_concordancia(navegador, wait, documento, nombre):
    """Fluxo especifico para CERTIFICADOS CONCORDANCIA usando XPaths fornecidos."""
    try:
        if not select_option(wait, [(By.ID, 'form'), (By.NAME, 'form')], 'Valencia'):
            print("[DEBUG] falha ao selecionar provincia Valencia")
            return 'erro'

        assert_not_blocked(navegador, "apos selecionar provincia")

        if not click_xpath(navegador, wait, "//*[@id='btnAceptar']"):
            print("[DEBUG] falha ao clicar primeiro Aceptar")
            return 'erro'

        assert_not_blocked(navegador, "apos aceitar provincia")

        if not select_option(
            wait,
            [(By.ID, 'tramiteGrupo[0]'), (By.NAME, 'tramiteGrupo[0]'), (By.XPATH, "//*[@id='tramiteGrupo[0]']")],
            'POLICIA - CERTIFICADOS CONCORDANCIA'
        ):
            print("[DEBUG] falha ao selecionar tramite concordancia")
            return 'erro'

        assert_not_blocked(navegador, "apos selecionar tramite")

        if not click_xpath(navegador, wait, "//*[@id='btnAceptar']"):
            print("[DEBUG] falha ao clicar segundo Aceptar")
            return 'erro'

        assert_not_blocked(navegador, "apos segundo aceitar")

        if not click_xpath(navegador, wait, "//*[@id='btnEntrar']"):
            print("[DEBUG] falha ao clicar Entrar")
            return 'erro'

        assert_not_blocked(navegador, "apos entrar")

        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='txtIdCitado']"))).send_keys(documento)
        human_pause()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='txtDesCitado']"))).send_keys(nombre)
        human_pause()

        if not click_xpath(navegador, wait, "//*[@id='btnEnviar']"):
            return 'erro'

        time.sleep(0.5)
        if not click_xpath(navegador, wait, "//*[@id='btnEnviar']"):
            return 'erro'

        # Botão "Solicitar Cita" (mesmo id) e checagem de disponibilidade
        human_pause()
        try:
            click_xpath(navegador, wait, "//*[@id='btnEnviar']")
        except Exception:
            # segue para checar mensagem mesmo se o segundo clique falhar
            print("[DEBUG] segundo clique em btnEnviar falhou, seguindo para checar mensagem")
            pass

        # Checa mensagem final na tela (disponibilidade)
        time.sleep(2)
        assert_not_blocked(navegador, "tela final (apos solicitar)")

        unavailable = detect_unavailable_final(navegador)
        print(f"[DEBUG] resultado detect_unavailable_final={unavailable}")
        if unavailable:
            click_xpath(navegador, wait, "//*[@id='btnSalir']")
            return 'sem_cita'

        # Se não encontrou a mensagem de indisponibilidade, considera cita disponível
        return 'cita_disponivel'
    except Exception as e:
        print(f'Erro no fluxo de concordancia: {e}')
        # Mesmo em erro, tenta decidir com base no HTML atual
        try:
            if is_support_blocked(navegador):
                print("[DEBUG] is_support_blocked -> bloqueado (via excecao)")
                return 'bloqueado'
            if detect_unavailable_final(navegador):
                print("[DEBUG] detect_unavailable_final -> sem_cita (via excecao)")
                return 'sem_cita'
            # se não encontrar a mensagem de indisponibilidade, assume que há disponibilidade
            print("[DEBUG] detect_unavailable_final -> cita_disponivel (via excecao)")
            return 'cita_disponivel'
        except Exception:
            # como fallback final, assume indisponível para evitar loop eterno de erro
            print("[DEBUG] fallback sem_cita (via excecao secundaria)")
            return 'sem_cita'



def buscar_carta_concordancia(documento, nombre):
    """Loop que verifica a carta de concordancia e apenas avisa no Telegram."""
    tentativa = 0
    send_message_to_telegram(
        f'Bot iniciado no modo CERTIFICADOS CONCORDANCIA para {nombre} ({documento}).'
    )

    while not exit_key:
        tentativa += 1
        print(f'Tentativa (concordancia): {tentativa}')
        load_dotenv()
        servico = build_chrome_service()
        navegador = webdriver.Chrome(service=servico, options=build_chrome_options())
        wait = WebDriverWait(navegador, 15)

        result = 'erro'
        try:
            navegador.get('https://icp.administracionelectronica.gob.es/icpplus/index.html')
            navegador.implicitly_wait(10)
            if is_support_blocked(navegador):
                result = 'bloqueado'
                raise Exception("Tela de bloqueio detectada")
            result = executar_fluxo_concordancia(navegador, wait, documento, nombre)
        except Exception as e:
            print(f'Erro ao buscar concordancia: {e}')

        # Se retornou erro, tenta reclassificar pela tela atual antes de fechar
        if result == 'erro':
            try:
                if is_support_blocked(navegador):
                    print("[DEBUG] reclassificando erro para bloqueado (tela mostra bloqueio)")
                    result = 'bloqueado'
                elif detect_unavailable_final(navegador):
                    print("[DEBUG] reclassificando erro para sem_cita (tela mostra indisponibilidade)")
                    result = 'sem_cita'
            except Exception:
                pass

        if result == 'cita_disponivel':
            print('Cita disponivel para concordancia! Notificando no Telegram.')
            send_message_to_telegram(
                'Ha cita disponivel para CERTIFICADOS CONCORDANCIA. Entre no site para marcar.'
            )
            try:
                navegador.save_screenshot('cita_concordancia.png')
                send_image_to_telegram('cita_concordancia.png')
            except Exception as e:
                print(f'Erro ao enviar print: {e}')
            print('Navegador mantido aberto para marcar manualmente.')
            return

        if result == 'erro':
            dump_debug_page(navegador, label="concordancia_erro")
        navegador.quit()

        print(f"[DEBUG] resultado final do loop: {result}")
        if result == 'sem_cita':
            print('Sem citas disponiveis para concordancia.')
        elif result == 'bloqueado':
            print('Tela de bloqueio detectada (The requested URL was rejected). Reiniciando contagem.')
        elif result == 'erro':
            print('Fluxo de concordancia nao completado; tentando novamente.')
        else:
            print('Fluxo de concordancia nao completado; tentando novamente (resultado inesperado).')

        wait_seconds, base_minutes, jitter = compute_wait_seconds()
        print(f"Procurando novamente em ~{wait_seconds // 60} min (base {base_minutes}m, fator {jitter:.2f}) (ESC para sair).")
        i = 0
        while i < wait_seconds:
            if keyboard.is_pressed('esc'):
                print('Finalizando.')
                return
            time.sleep(1)
            minutes, seconds = divmod(wait_seconds - i, 60)
            print(
                f'Repetindo busca de concordancia em {minutes:02d}:{seconds:02d}',
                end='\r')
            i += 1


if service_choice == '2':
    buscar_carta_concordancia(DOCUMENTO, NOMBRE)
    sys.exit()
elif service_choice != '1':
    print('Opção de serviço inválida')
    sys.exit()

cap = 0
print('\nAbrindo o navegador...')


send_message_to_telegram(
    f'Bot iniciado\nBuscando cita para {NOMBRE}\nDocumento: {DOCUMENTO}\nBuscando cita com data entre {DATA_INICIAL} e {DATA_MARCADO}.')

while exit_key == False:
    cap += 1
    load_dotenv()
    # options = Options()
    # options.add_argument("--headless")  # Executa o Chrome em modo headless (sem janela visível)

    # Instancia o serviço e o navegador
    servico = build_chrome_service()
    # navegador = webdriver.Chrome(service=servico, options=options)
    navegador = webdriver.Chrome(service=servico, options=build_chrome_options())

    navegador.get("https://www.tramita.gva.es/ctt-att-atr/asistente/iniciarTramite.html?tramite=CITA_PREVIA&version=2&idioma=es&idProcGuc=14104&idCatGuc=PR")
    navegador.implicitly_wait(10)
    if is_support_blocked(navegador):
        print("Tela de bloqueio detectada (The requested URL was rejected). Reiniciando contagem.")
        navegador.quit()
        wait_seconds, base_minutes, jitter = compute_wait_seconds()
        i = 0
        while i < wait_seconds:
            minutes, seconds = divmod(wait_seconds - i, 60)
            print(
                f"Procurando nova cita para {NOMBRE} no documento {DOCUMENTO} em {minutes:02d}:{seconds:02d}", end="\r")
            i += 1
            time.sleep(1)
        continue
    time.sleep(5)

    print('Preenchendo dados...')

    ############################## PROVINCIA #################################################
    try:
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[4]/div[2]/div/a/span').click()
        print('Seleciona provincia')
        time.sleep(0.5)
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[4]/div[2]/div/div/ul/li[4]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar provincia, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## MUNICIPIO #################################################
    try:
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[6]/div[2]/div/a/span').click()
        print('Seleciona municipio')
        time.sleep(0.5)
        body = navegador.find_element(By.TAG_NAME, 'body')
        for _ in range(14):  # ajuste este valor conforme necessário
            body.send_keys(Keys.DOWN)
            # adicione um pequeno atraso entre cada pressionamento de tecla, se necessário
            time.sleep(0.1)
        time.sleep(0.5)
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[6]/div[2]/div/div/ul/li[15]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar municipio, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## SERVICIO #################################################
    try:
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[8]/div[2]/div/a/span').click()
        print('seleciona servicio')
        time.sleep(0.5)
        for _ in range(10):  # ajuste este valor conforme necessário
            body.send_keys(Keys.DOWN)
            # adicione um pequeno atraso entre cada pressionamento de tecla, se necessário
            time.sleep(0.2)
        # time.sleep(1.5)
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[8]/div[2]/div/div/ul/li[11]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar servicio, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## CENTRO #################################################
    try:
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[10]/div[2]/div/a/span').click()
        print('clica no centro')
        time.sleep(0.5)
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[10]/div[2]/div/div/ul/li[2]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar centro, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## DNI/NIE #################################################
    try:
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/a/span').click()

        time.sleep(0.5)
        if doc == "1":
            print('clica no NIE')
            navegador.find_element(
                By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/div/ul/li[2]/a').click()
        else:
            print('clica no PASSAPORTE')
            navegador.find_element(
                By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/div/ul/li[3]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar dni/nie, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## IDENTIFICACIÓN #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="SOL_DNI"]').click()
        print('clica no IDENTIFICACIÓN')

        time.sleep(0.5)
        navegador.find_element(
            By.XPATH, '//*[@id="SOL_DNI"]').send_keys(DOCUMENTO)
    except:
        print('Erro ao selecionar identificación, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## NOMBRE #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="SOL_NOMBRE"]').click()
        print('clica no NOMBRE')
        time.sleep(0.5)
        navegador.find_element(
            By.XPATH, '//*[@id="SOL_NOMBRE"]').send_keys(NOMBRE)
    except:
        print('Erro ao selecionar nombre, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## PRIMER APELLIDO #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO1"]').click()
        print('clica no PRIMER APELLIDO')
        time.sleep(0.2)
        navegador.find_element(
            By.XPATH, '//*[@id="SOL_APELLIDO1"]').send_keys(APELLIDO1)
    except:
        print('Erro ao selecionar primer apellido, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## SEGUNDO APELLIDO #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO2"]').click()
        print('clica no SEGUNDO APELLIDO')
        time.sleep(0.2)
        navegador.find_element(
            By.XPATH, '//*[@id="SOL_APELLIDO2"]').send_keys(APELLIDO2)
    except:
        print('Erro ao selecionar segundo apellido, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## FECHA DE NACIMIENTO #################################################

    try:
        # navegador.find_element(By.XPATH, '//*[@id="SOL_FECHA"]').click()
        navegador.switch_to.active_element.send_keys(Keys.TAB)
        print('clica no FECHA DE NACIMIENTO')
        time.sleep(0.2)
        navegador.find_element(
            By.XPATH, '//*[@id="SOL_FECHA"]').send_keys(FECHA_NASC)
    except:
        print('Erro ao selecionar fecha de nacimiento, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## TELÉFONO #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="SOL_TFNO"]').click()
        print('clica no TELÉFONO')
        time.sleep(0.2)
        navegador.find_element(
            By.XPATH, '//*[@id="SOL_TFNO"]').send_keys(TELEFONO)
    except:
        print('Erro ao selecionar teléfono, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## CORREO ELECTRÓNICO #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="SOL_EMAIL"]').click()
        print('clica no CORREO ELECTRÓNICO')
        time.sleep(0.2)
        navegador.find_element(
            By.XPATH, '//*[@id="SOL_EMAIL"]').send_keys(EMAIL)
    except:
        print('Erro ao selecionar correo electrónico, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## CROP CAPTCHA ##################################################
    def captcha():
        print('Lendo o captcha')
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[48]/p').click()
        print('clica no captcha')

        # Tire o screenshot da página inteira
        navegador.save_screenshot("screenshot.png")
        print('Tirando o screenshot')

        def is_close_to_dimensions(w, h, target_width, target_height, tolerance=0.2):
            width_diff = abs(w - target_width) / target_width
            height_diff = abs(h - target_height) / target_height
            return width_diff < tolerance and height_diff < tolerance

        # Carregue a imagem da tela e converta para escala de cinza
        screenshot = cv2.imread('screenshot.png')
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Detecte bordas na imagem
        edges = cv2.Canny(gray_screenshot, 50, 150)

        # Encontre contornos na imagem
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Percorra todos os contornos e encontre o retângulo com dimensões próximas a 120x50
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if is_close_to_dimensions(w, h, 120, 50):
                # Se as dimensões estiverem próximas das desejadas, desenhe o retângulo na imagem
                cv2.rectangle(screenshot, (x, y),
                              (x + w, y + h), (0, 255, 0), 2)
                # Salve a imagem do captcha
                captcha_crop = gray_screenshot[y:y + h, x:x + w]
                cv2.imwrite('captcha_cropped.png', captcha_crop)
                break

        ################################### CAPTCHA SOLVER ########################################
        print('Resolvendo o captcha')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Carregue a imagem do captcha
        captcha_image = cv2.imread('captcha_cropped.png', cv2.IMREAD_GRAYSCALE)

        # Aplique um desfoque suave à imagem para remover ruídos
        blurred_image = cv2.GaussianBlur(captcha_image, (5, 5), 0)

        # Binarize a imagem usando um limite adaptativo
        threshold_image = cv2.adaptiveThreshold(
            blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )

        # Configure o Tesseract para usar apenas números como caracteres possíveis
        custom_config = r'--oem 3 --psm 6 outputbase digits'

        # Use o Tesseract para reconhecer os caracteres na imagem
        recognized_text = pytesseract.image_to_string(
            threshold_image, config=custom_config)

        print("Texto reconhecido:", recognized_text)

        # Remova todos os caracteres não numéricos do texto reconhecido
        numbers_only = ''.join(
            char for char in recognized_text if char.isdigit())
        if numbers_only == "" or numbers_only == ".":
            numbers_only = '0000'

        print("Números do captcha:", numbers_only)

        ############################## Incluye el texto de la imagen #################################################
        navegador.find_element(By.XPATH, '//*[@id="ID_1666791417799"]').click()
        time.sleep(0.1)
        navegador.find_element(
            By.XPATH, '//*[@id="ID_1666791417799"]').send_keys(f'{numbers_only}')

        ############################## envia #################################################

        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click()
        time.sleep(3.0)
        return ()

        ############################## confirma #################################################
    captcha_resolvido = False
    tentativas = 0
    while not captcha_resolvido:

        tentativas += 1
        print(f"Tentativa {tentativas}")
        captcha()
        tent = 0
        try:
            navegador.find_element(By.XPATH, '//*[@id="SOL_DESDE"]').click()
            captcha_resolvido = True
            print("Captcha resolvido")
            print('Continua - Próxima tela (confirmação dos dados)')
        except:
            navegador.find_element(
                By.XPATH, '//*[@id="imc-forms--missatge"]/div/div/div[3]/button[5]').click()
            if navegador.find_element(By.XPATH, '//*[@id="imc-forms--missatge"]/div/div/h2/span').text == "No coincide el texto introducido con el que aparece en la imagen. Se ha generado otra imagen con un nuevo texto, en caso de que no lo visualice correctamente pulse sobre el boton Regenerar para generar un nuevo texto.":
                print("Captcha errado, tentando novamente...")

            else:
                print("Pagina com erro, tentando novamente...")
                navegador.find_element(
                    By.XPATH, '//*[@id="imc-forms--missatge"]/div/div/div[3]/button[5]/span').click()
                break
            navegador.find_element(
                By.XPATH, '//*[@id="ID_1666791417799"]').clear()

    ############################## CONTINUA PRX PANTALLA #################################################
    try:
        time.sleep(7.0)
        navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click()
        print('Continua - Próxima tela (citas disponíveis)')
    except:
        print('Erro na pagina, tentando novamente...')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## LEER RESULTADOS #################################################
    try:
        time.sleep(8.0)
        label_elemento = navegador.find_element(
            By.XPATH, '//*[@id="imc-forms-formulari"]/div/fieldset/ul/li/div/label')
        print('LEER RESULTADOS')
        texto_label = label_elemento.text
    except:
        print('Erro na pagina, tentando novamente...')
        navegador.quit()
        time.sleep(5)
        continue
    ############################## print results #################################################

    if texto_label != "Sin citas disponibles":
        print(texto_label)
        data1_obj = datetime.strptime(DATA_MARCADO, "%d/%m/%Y %H:%M")
        data3_obj = datetime.strptime(DATA_INICIAL, "%d/%m/%Y %H:%M")
        data2_obj = datetime.strptime(texto_label, "%d/%m/%Y %H:%M")

        if data1_obj < data2_obj and data2_obj > data3_obj:
            print(f"Cita encontrada para {texto_label}")
            print(
                f"Procurando cita con data entre {DATA_INICIAL} e {DATA_MARCADO}")
            print(f"Voltando a procurar...")
            print("Fechando navegador...")

            data_hora = time.strftime("%d-%m-%Y %H:%M:%S")
            mensagem = f"{data_hora}: Cita encontrada para {NOMBRE} na data {texto_label}, não marcada, buscando cita entre {DATA_INICIAL} e {DATA_MARCADO}\n"
            with open("arquivo.txt", "a") as arquivo:
                arquivo.write(mensagem)

            navegador.quit()
        else:
            print(f"Cita encontrada para {texto_label}")
            print("Marcando a cita")
            send_message_to_telegram(
                f"Cita encontrada para {texto_label}\n Marcando a cita")
            # Clica seleconar cita
            try:
                time.sleep(2)
                navegador.find_element(
                    By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li[1]/button/span').click()
            except:
                print('Erro ao selecionar cita, tentando novamente...')
                navegador.quit()
                time.sleep(5)

            # clica em confirmar cita
            cita = 0
            try:
                time.sleep(5)
                navegador.find_element(
                    By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li[1]/button/span').click()
                print(f'Cita marcada para {texto_label}')
                send_message_to_telegram(
                    f"Cita marcada para {texto_label}\n arquivo pdf de confirmação salvo no computador")
                time.sleep(5)
                # clina no campo hora para abaixar a tela e deixar os dados dad cita visiveis para o pront
                navegador.find_element(By.XPATH, '//*[@id="SOL_HORA"]').click()
                # tira o print
                navegador.save_screenshot("cita_marcada.png")
                send_image_to_telegram("cita_marcada.png")
                print("salvo Print da tela da cita marcada")
                # clica no botão de imprimir cita para iniciar o download
                navegador.find_element(
                    By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click()
                cita = 1
                data_hora = time.strftime("%d-%m-%Y %H:%M:%S")

                nome = NOMBRE.replace(" ", "_")

                mensagem = f"{data_hora}: Cita encontrada para {NOMBRE} no doc {DOCUMENTO} na data {texto_label}, Marcada com sucesso\n"
                with open(f"arquivo_{nome}.txt", "a") as arquivo:
                    arquivo.write(mensagem)

                mensagem = f"{data_hora}: Cita marcada para {NOMBRE} doc {DOCUMENTO} na data {texto_label}\n"
                with open(f"citas_marcadas_{nome}.txt", "a") as arquivo:
                    arquivo.write(mensagem)

                input("Pressione enter para sair...")
                navegador.quit()
                sys.exit()
            except:
                if cita == 0:
                    print(
                        'Erro ao selecionar cita, Verifique o navegador\n tentando novamente em alguns minutos')
                    send_message_to_telegram(
                        f"Erro ao marcar cita, verifique o navegador\nCita encontrada para {data2_obj}\n voltando a buscar em breve")

                wait_seconds, base_minutes, jitter = compute_wait_seconds()
                i = 0
                while i < wait_seconds:
                    minutes, seconds = divmod(wait_seconds - i, 60)
                    print(
                        f"Voltando a procurar nova cita para {NOMBRE} no documento {DOCUMENTO}em {minutes:02d}:{seconds:02d}", end="\r")
                    i += 1
                    time.sleep(1)

                navegador.quit()
                time.sleep(5)
                continue
    else:
        print(texto_label)
        print("Fechando navegador...")
        navegador.quit()
    wait_seconds, base_minutes, jitter = compute_wait_seconds()
    i = 0
    print(f"Procurando cita novamente em ~{wait_seconds // 60} min (base {base_minutes}m, fator {jitter:.2f})")
    print("pressione CTRL + C para sair")
    print(f"Numero de tentativas: {cap}")
    while i < wait_seconds:

        if keyboard.is_pressed('esc'):
            navegador.quit()
            print("Finalizando.")
            exit_key = True
            break
        time.sleep(1)
        minutes, seconds = divmod(wait_seconds - i, 60)
        print(
            f"Procurando nova cita para {NOMBRE} no documento {DOCUMENTO} em {minutes:02d}:{seconds:02d}", end="\r")
        i += 1
