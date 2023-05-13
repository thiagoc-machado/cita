from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image
import cv2
import numpy as np
from dotenv import load_dotenv
import os
from twilio.rest import Client
import pytesseract
import time

cap = 0
load_dotenv()

servico = Service(ChromeDriverManager().install())

navegador= webdriver.Chrome(service = servico)

navegador.get("https://www.tramita.gva.es/ctt-att-atr/asistente/iniciarTramite.html?tramite=CITA_PREVIA&version=2&idioma=es&idProcGuc=14104&idCatGuc=PR")
time.sleep(5)

############################## PROVINCIA #################################################
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[4]/div[2]/div/a/span').click()
time.sleep(1)
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[4]/div[2]/div/div/ul/li[4]/a').click()
time.sleep(1)

############################## MUNICIPIO #################################################
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[6]/div[2]/div/a/span').click()
time.sleep(1)
body = navegador.find_element(By.TAG_NAME, 'body')
for _ in range(14): # ajuste este valor conforme necessário
    body.send_keys(Keys.DOWN)
    time.sleep(0.1)  # adicione um pequeno atraso entre cada pressionamento de tecla, se necessário
time.sleep(0.5)
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[6]/div[2]/div/div/ul/li[15]/a').click()
time.sleep(1)

############################## SERVICIO #################################################
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[8]/div[2]/div/a/span').click()
time.sleep(1)
for _ in range(10): # ajuste este valor conforme necessário
    body.send_keys(Keys.DOWN)
    time.sleep(0.2)  # adicione um pequeno atraso entre cada pressionamento de tecla, se necessário
time.sleep(1)
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[8]/div[2]/div/div/ul/li[11]/a').click()
time.sleep(1)

############################## CENTRO #################################################
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[10]/div[2]/div/a/span').click()
time.sleep(1)
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[10]/div[2]/div/div/ul/li[2]/a').click()
time.sleep(1)

############################## DNI/NIE #################################################
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/a/span').click()
time.sleep(1)
#NIE
navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/div/ul/li[2]/a').click()
#PASSAPORTE
#navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/div/ul/li[3]/a').click()
time.sleep(1)

############################## IDENTIFICACIÓN #################################################
navegador.find_element(By.XPATH, '//*[@id="SOL_DNI"]').click()
time.sleep(0.1)
navegador.find_element(By.XPATH, '//*[@id="SOL_DNI"]').send_keys(os.environ.get('NIE'))

############################## NOMBRE #################################################
navegador.find_element(By.XPATH, '//*[@id="SOL_NOMBRE"]').click()
time.sleep(0.2)
navegador.find_element(By.XPATH, '//*[@id="SOL_NOMBRE"]').send_keys(os.environ.get('NOMBRE'))

############################## PRIMER APELLIDO #################################################
navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO1"]').click()
time.sleep(0.1)
navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO1"]').send_keys(os.environ.get('APELLIDO1'))

############################## SEGUNDO APELLIDO #################################################
navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO2"]').click()
time.sleep(0.1)
navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO2"]').send_keys(os.environ.get('APELLIDO2'))

############################## FECHA DE NACIMIENTO #################################################
navegador.find_element(By.XPATH, '//*[@id="SOL_FECHA"]').click()
time.sleep(0.1)
navegador.find_element(By.XPATH, '//*[@id="SOL_FECHA"]').send_keys(os.environ.get('FECHA_NASC'))

############################## TELÉFONO #################################################
navegador.find_element(By.XPATH, '//*[@id="SOL_TFNO"]').click()
time.sleep(0.1)
navegador.find_element(By.XPATH, '//*[@id="SOL_TFNO"]').send_keys(os.environ.get('TELEFONO'))

############################## CORREO ELECTRÓNICO #################################################
navegador.find_element(By.XPATH, '//*[@id="SOL_EMAIL"]').click()
time.sleep(0.1)
navegador.find_element(By.XPATH, '//*[@id="SOL_EMAIL"]').send_keys(os.environ.get('EMAIL'))


############################## CROP CAPTCHA ##################################################
def captcha():
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[48]/p').click()

    # Tire o screenshot da página inteira
    navegador.save_screenshot("screenshot.png")

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
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Percorra todos os contornos e encontre o retângulo com dimensões próximas a 120x50
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        if is_close_to_dimensions(w, h, 120, 50):
            # Se as dimensões estiverem próximas das desejadas, desenhe o retângulo na imagem
            cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Salve a imagem do captcha
            captcha_crop = gray_screenshot[y:y + h, x:x + w]
            cv2.imwrite('captcha_cropped.png', captcha_crop)
            break


    ################################### CAPTCHA SOLVER ########################################

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
    recognized_text = pytesseract.image_to_string(threshold_image, config=custom_config)

    print("Texto reconhecido:", recognized_text)

    # Remova todos os caracteres não numéricos do texto reconhecido
    numbers_only = ''.join(char for char in recognized_text if char.isdigit())

    print("Números do captcha:", numbers_only)

    ############################## Incluye el texto de la imagen #################################################
    navegador.find_element(By.XPATH, '//*[@id="ID_1666791417799"]').click()
    time.sleep(0.1)
    navegador.find_element(By.XPATH, '//*[@id="ID_1666791417799"]').send_keys(f'{numbers_only}')

    
    ############################## envia #################################################

    navegador.find_element(By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click()
    time.sleep(5.0)
    return()

if cap == 0:
    cap += 1
    print(f"CAP {cap}")
    captcha()

    ############################## confirma #################################################
try:
    navegador.find_element(By.XPATH, '//*[@id="SOL_DESDE"]').click() 
except:
    navegador.find_element(By.XPATH, '//*[@id="imc-forms--missatge"]/div/div/div[3]/button[5]').click()
    print("Captcha errado, tentando denovo...")
    time.sleep(1.0)
    navegador.find_element(By.XPATH, '//*[@id="ID_1666791417799"]').clear()
    captcha()

############################## CONTINUA PRX PANTALLA #################################################  
navegador.find_element(By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click() 

############################## TEST CAPTCHA #################################################   
time.sleep(5.0)
label_elemento = navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/fieldset/ul/li/div/label')
texto_label = label_elemento.text

############################## print results #################################################

if texto_label == "Sin citas disponibles":
    print(texto_label)
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=f"SEM CITA {texto_label}",
                        from_='+12707703927',
                        to='+34653579325'
                    )

    print(message.sid)
    time.sleep(20) 
else:
    print(texto_label)

    navegador.quit()
