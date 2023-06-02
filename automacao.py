from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import cv2
from dotenv import load_dotenv
import pytesseract
import time
import keyboard
from datetime import datetime
import requests
import sys

exit_key = False

print('selecione 1 para Julie')
print('selecione 2 para Thiago')
person = input()
print('selecione 1 para NIE')
print('selecione 2 para Passaporte')
doc = input()

bot_token = ":"
bot_chat_id = ""

if person == '1':
    print('Selecionado Julie')
    DATA_MARCADO='18/12/2023 20:00'
    NOMBRE=' '
    APELLIDO1=''
    APELLIDO2=''
    FECHA_NASC='//'
    TELEFONO=''
    EMAIL=''
    if  doc == '1':
        print('Selecionado NIE')
        DOCUMENTO=''
    elif doc == '2':
        print('Selecionado Passaporte')
        DOCUMENTO=''
    else:  
        print('Opção inválida')
        exit()

elif person == '2':
    print('Selecionado Thiago')
    DATA_MARCADO='01/11/2023 09:30'
    NOMBRE=''
    APELLIDO1=''
    APELLIDO2=''
    FECHA_NASC='//'
    TELEFONO=''
    EMAIL=''
    if  doc == '1':
        print('Selecionado NIE')
        DOCUMENTO=''
    elif doc == '2':
        print('')
        DOCUMENTO=''
    else:  
        print('Opção inválida')
        exit()
else:
    print('Opção inválida')
    exit()

cap = 0
print('')
print('Abrindo o navegador...')

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
                print(f"Erro ao enviar imagem para o Telegram: {response.text}")
    except Exception as e:
        print(f"Erro ao enviar imagem para o Telegram: {e}")


send_message_to_telegram(f'Bot iniciado\nBuscando cita para {NOMBRE}\nDocumento: {DOCUMENTO}\nBuscando cita com data antes de {DATA_MARCADO}')

while exit_key == False:
    cap += 1
    load_dotenv()
    #options = Options()
    #options.add_argument("--headless")  # Executa o Chrome em modo headless (sem janela visível)

    # Instancia o serviço e o navegador
    servico = Service(ChromeDriverManager().install())
    #navegador = webdriver.Chrome(service=servico, options=options)
    navegador = webdriver.Chrome(service=servico)

    navegador.get("https://www.tramita.gva.es/ctt-att-atr/asistente/iniciarTramite.html?tramite=CITA_PREVIA&version=2&idioma=es&idProcGuc=14104&idCatGuc=PR")
    navegador.implicitly_wait(10)
    time.sleep(5)

    print('Preenchendo dados...')

    ############################## PROVINCIA #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[4]/div[2]/div/a/span').click()
        print('Seleciona provincia')
        time.sleep(0.5)
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[4]/div[2]/div/div/ul/li[4]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar provincia, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## MUNICIPIO #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[6]/div[2]/div/a/span').click()
        print('Seleciona municipio')
        time.sleep(0.5)
        body = navegador.find_element(By.TAG_NAME, 'body')
        for _ in range(14): # ajuste este valor conforme necessário
            body.send_keys(Keys.DOWN)
            time.sleep(0.1)  # adicione um pequeno atraso entre cada pressionamento de tecla, se necessário
        time.sleep(0.5)
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[6]/div[2]/div/div/ul/li[15]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar municipio, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## SERVICIO #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[8]/div[2]/div/a/span').click()
        print('seleciona servicio')
        time.sleep(0.5)
        for _ in range(10): # ajuste este valor conforme necessário
            body.send_keys(Keys.DOWN)
            time.sleep(0.2)  # adicione um pequeno atraso entre cada pressionamento de tecla, se necessário
        #time.sleep(1.5)
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[8]/div[2]/div/div/ul/li[11]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar servicio, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## CENTRO #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[10]/div[2]/div/a/span').click()
        print('clica no centro')
        time.sleep(0.5)
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[10]/div[2]/div/div/ul/li[2]/a').click()
        time.sleep(3)
    except:
        print('Erro ao selecionar centro, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## DNI/NIE #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/a/span').click()
        
        time.sleep(0.5)
        if doc == "1":
            print('clica no NIE')
            navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/div/ul/li[2]/a').click()
        else:
            print('clica no PASSAPORTE')
            navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/div/ul/li[3]/a').click()
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
        navegador.find_element(By.XPATH, '//*[@id="SOL_DNI"]').send_keys(DOCUMENTO)
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
        navegador.find_element(By.XPATH, '//*[@id="SOL_NOMBRE"]').send_keys(NOMBRE)
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
        navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO1"]').send_keys(APELLIDO1)
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
        navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO2"]').send_keys(APELLIDO2)
    except:
        print('Erro ao selecionar segundo apellido, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue    

    ############################## FECHA DE NACIMIENTO #################################################
    try:
        navegador.find_element(By.XPATH, '//*[@id="SOL_FECHA"]').click()
        print('clica no FECHA DE NACIMIENTO')
        time.sleep(0.2)
        navegador.find_element(By.XPATH, '//*[@id="SOL_FECHA"]').send_keys(FECHA_NASC)
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
        navegador.find_element(By.XPATH, '//*[@id="SOL_TFNO"]').send_keys(TELEFONO)
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
        navegador.find_element(By.XPATH, '//*[@id="SOL_EMAIL"]').send_keys(EMAIL)
    except:
        print('Erro ao selecionar correo electrónico, tentando novamente')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## CROP CAPTCHA ##################################################
    def captcha():
        print('Lendo o captcha')
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[48]/p').click()
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
        recognized_text = pytesseract.image_to_string(threshold_image, config=custom_config)

        print("Texto reconhecido:", recognized_text)

        # Remova todos os caracteres não numéricos do texto reconhecido
        numbers_only = ''.join(char for char in recognized_text if char.isdigit())
        if numbers_only == "":
            numbers_only = '0000'

        print("Números do captcha:", numbers_only)

        ############################## Incluye el texto de la imagen #################################################
        navegador.find_element(By.XPATH, '//*[@id="ID_1666791417799"]').click()
        time.sleep(0.1)
        navegador.find_element(By.XPATH, '//*[@id="ID_1666791417799"]').send_keys(f'{numbers_only}')

        
        ############################## envia #################################################

        navegador.find_element(By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click()
        time.sleep(3.0)
        return()

        ############################## confirma #################################################
    captcha_resolvido = False
    tentativas = 0 
    while not captcha_resolvido:
        
        tentativas += 1
        print(f"Tentativa {tentativas}")
        captcha()
        try:
            navegador.find_element(By.XPATH, '//*[@id="SOL_DESDE"]').click() 
            captcha_resolvido = True
            print("Captcha resolvido")
            print('Continua - Próxima tela (confirmação dos dados)')
        except:
            navegador.find_element(By.XPATH, '//*[@id="imc-forms--missatge"]/div/div/div[3]/button[5]').click()
            if navegador.find_element(By.XPATH, '//*[@id="imc-forms--missatge"]/div/div/h2/span').text == "No coincide el texto introducido con el que aparece en la imagen. Se ha generado otra imagen con un nuevo texto, en caso de que no lo visualice correctamente pulse sobre el boton Regenerar para generar un nuevo texto.":
                print("Captcha errado, tentando novamente...")

            else:
                print("Pagina com erro, tentando novamente...")
                navegador.find_element(By.XPATH, '//*[@id="imc-forms--missatge"]/div/div/div[3]/button[5]/span').click()
                break
            navegador.find_element(By.XPATH, '//*[@id="ID_1666791417799"]').clear()
        

    ############################## CONTINUA PRX PANTALLA #################################################  
    try:
        time.sleep(7.0)
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click() 
        print('Continua - Próxima tela (citas disponíveis)')
    except:
        print('Erro na pagina, tentando novamente...')
        navegador.quit()
        time.sleep(5)
        continue

    ############################## LEER RESULTADOS #################################################   
    try:
        time.sleep(8.0)
        label_elemento = navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/fieldset/ul/li/div/label')
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
        data2_obj = datetime.strptime(texto_label, "%d/%m/%Y %H:%M")
        if  data1_obj < data2_obj:
            print(f"Cita encontrada para {texto_label}")
            print(f"Cita marcada para {DATA_MARCADO}")
            print(f"Voltando a procurar...")
            print("Fechando navegador...")
            navegador.quit()
        else:
            print(f"Cita encontrada para {texto_label}")
            print("Marcando a cita")
            send_message_to_telegram(f"Cita encontrada para {texto_label}\n Marcando a cita")
            #Clica seleconar cita
            try:
                time.sleep(2)
                navegador.find_element(By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li[1]/button/span').click()
            except:
                print('Erro ao selecionar cita, tentando novamente...')
                navegador.quit()
                time.sleep(5)

            #clica em confirmar cita
            try:
                time.sleep(5)
                navegador.find_element(By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li[1]/button/span').click()
                print(f'Cita marcada para {data2_obj}')
                send_message_to_telegram(f"Cita marcada para {data2_obj}\n arquivo pdf de confirmação salvo no computador")
                time.sleep(5)
                #clina no campo hora para abaixar a tela e deixar os dados dad cita visiveis para o pront
                navegador.find_element(By.XPATH, '//*[@id="SOL_HORA"]').click()
                #tira o print
                navegador.save_screenshot("cita_marcada.png")
                send_image_to_telegram("cita_marcada.png")
                print("salvo Print da tela da cita marcada")
                #clica no botão de imprimir cita para iniciar o download
                navegador.find_element(By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click()
                input("Pressione enter para sair...")
                navegador.quit()
                sys.exit()
            except:
                print('Erro ao selecionar cita, Verifique o navegador\n tentando novamente em 5 minutos')
                send_message_to_telegram(f"Erro ao marcar cita, verifique o navegador\nCita encontrada para {data2_obj}\n voltando a buscar em 5 minutos")
                
                i=0
                while i < 300:
                    minutes, seconds = divmod(300 - i, 60)
                    print(f"Voltando a procurar nova cita para {NOMBRE} no documento {DOCUMENTO}em {minutes:02d}:{seconds:02d}", end="\r")
                    i+=1
                    time.sleep(1)

                navegador.quit()
                time.sleep(5)
                continue
    else:
        print(texto_label)
        print("Fechando navegador...")
        navegador.quit()
    i=0
    print("Procurando cita novamente em 5 minutos")
    print("pressione CTRL + C para sair")
    print(f"Numero de tentativas: {cap}")
    while i < 300:
        
        if keyboard.is_pressed('esc'):
                navegador.quit()
                print("Finalizando.")
                exit_key = True
                break 
        time.sleep(1)
        minutes, seconds = divmod(300 - i, 60)
        print(f"Procurando nova cita para {NOMBRE} no documento {DOCUMENTO} em {minutes:02d}:{seconds:02d}", end="\r")    
        i+=1
