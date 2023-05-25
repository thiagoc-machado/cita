from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import cv2
from dotenv import load_dotenv
from twilio.rest import Client
import pytesseract
import time
import keyboard

exit_key = False

print('digite 1 para NIE')
print('digite 2 para Passaporte FV902583')
print('digite 3 para Passaporte YE534479')
doc = input()

NOMBRE='Victor'
APELLIDO1='Aguiar'
APELLIDO2='Dias Rodrigues'
FECHA_NASC='13/06/2003'
TELEFONO='693036666'
EMAIL='victoraguiarrodrigues@yahoo.com'
if  doc == '1':
    print('Selecionado NIE Y7563471G')
    DOCUMENTO='Y7563471G'
elif doc == '2':
    print('Selecionado Passaporte FV902583')
    DOCUMENTO='FV902583'
elif doc == '3':
    print('Selecionado Passaporte YE534479')
    DOCUMENTO='YE534479'
else:  
    print('Opção inválida')
    exit()

cap = 0
print('')
print('Abrindo o navegador...')

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
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[4]/div[2]/div/a/span').click()
    print('Seleciona provincia')
    time.sleep(0.5)
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[4]/div[2]/div/div/ul/li[4]/a').click()
    time.sleep(3)

    ############################## MUNICIPIO #################################################
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

    ############################## SERVICIO #################################################
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[8]/div[2]/div/a/span').click()
    print('seleciona servicio')
    time.sleep(0.5)
    for _ in range(10): # ajuste este valor conforme necessário
        body.send_keys(Keys.DOWN)
        time.sleep(0.2)  # adicione um pequeno atraso entre cada pressionamento de tecla, se necessário
    #time.sleep(1.5)
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[8]/div[2]/div/div/ul/li[11]/a').click()
    time.sleep(3)

    ############################## CENTRO #################################################
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[10]/div[2]/div/a/span').click()
    print('clica no centro')
    time.sleep(0.5)
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[10]/div[2]/div/div/ul/li[2]/a').click()
    time.sleep(3)

    ############################## DNI/NIE #################################################
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/a/span').click()
    
    time.sleep(0.5)
    if doc == "1":
        print('clica no NIE')
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/div/ul/li[2]/a').click()
    else:
        print('clica no PASSAPORTE')
        navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/div[17]/div[2]/div/div/ul/li[3]/a').click()
    time.sleep(3)

    ############################## IDENTIFICACIÓN #################################################
    navegador.find_element(By.XPATH, '//*[@id="SOL_DNI"]').click()
    print('clica no IDENTIFICACIÓN')
        
    time.sleep(0.5)
    navegador.find_element(By.XPATH, '//*[@id="SOL_DNI"]').send_keys(DOCUMENTO)

    ############################## NOMBRE #################################################
    navegador.find_element(By.XPATH, '//*[@id="SOL_NOMBRE"]').click()
    print('clica no NOMBRE')
    time.sleep(0.5)
    navegador.find_element(By.XPATH, '//*[@id="SOL_NOMBRE"]').send_keys(NOMBRE)

    ############################## PRIMER APELLIDO #################################################
    navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO1"]').click()
    print('clica no PRIMER APELLIDO')
    time.sleep(0.2)
    navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO1"]').send_keys(APELLIDO1)

    ############################## SEGUNDO APELLIDO #################################################
    navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO2"]').click()
    print('clica no SEGUNDO APELLIDO')
    time.sleep(0.2)
    navegador.find_element(By.XPATH, '//*[@id="SOL_APELLIDO2"]').send_keys(APELLIDO2)

    ############################## FECHA DE NACIMIENTO #################################################
    navegador.find_element(By.XPATH, '//*[@id="SOL_FECHA"]').click()
    print('clica no FECHA DE NACIMIENTO')
    time.sleep(0.2)
    navegador.find_element(By.XPATH, '//*[@id="SOL_FECHA"]').send_keys(FECHA_NASC)

    ############################## TELÉFONO #################################################
    navegador.find_element(By.XPATH, '//*[@id="SOL_TFNO"]').click()
    print('clica no TELÉFONO')
    time.sleep(0.2)
    navegador.find_element(By.XPATH, '//*[@id="SOL_TFNO"]').send_keys(TELEFONO)

    ############################## CORREO ELECTRÓNICO #################################################
    navegador.find_element(By.XPATH, '//*[@id="SOL_EMAIL"]').click()
    print('clica no CORREO ELECTRÓNICO')
    time.sleep(0.2)
    navegador.find_element(By.XPATH, '//*[@id="SOL_EMAIL"]').send_keys(EMAIL)


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
    time.sleep(7.0)
    navegador.find_element(By.XPATH, '//*[@id="imc-forms-navegacio"]/ul/li/button').click() 
    print('Continua - Próxima tela (citas disponíveis)')

    ############################## LEER RESULTADOS #################################################   
    time.sleep(8.0)
    label_elemento = navegador.find_element(By.XPATH, '//*[@id="imc-forms-formulari"]/div/fieldset/ul/li/div/label')
    print('LEER RESULTADOS')
    texto_label = label_elemento.text

    ############################## print results #################################################

    if texto_label != "Sin citas disponibles":
        print(texto_label)
        from twilio.rest import Client

        account_sid = 'ACef1da88cb8569c6a6d159901520bfd0f'
        auth_token = '[AuthToken]'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'Cita encontrada para {NOMBRE} no documento {DOCUMENTO}.\n{texto_label}',
        to='whatsapp:+34692036666'
        )
        print(message.sid)
        while True:
            if keyboard.is_pressed('esc'):
                navegador.quit()
                print("Navegador fechado.")
                break
            time.sleep(3)
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

#Clica seleconar cita
#//*[@id="imc-forms-navegacio"]/ul/li[1]/button/span
#//*[@id="imc-forms-navegacio"]/ul/li[1]/button

#Clica confirmar cita
#//*[@id="imc-forms-navegacio"]/ul/li[1]/button/span
#//*[@id="imc-forms-navegacio"]/ul/li[1]/button