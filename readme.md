# Web Automation Project

Automação para buscar e marcar cita prévia (fluxo padrão) e para monitorar certificados de concordancia (apenas alerta). Usa Python, Selenium WebDriver, OpenCV, Tesseract OCR, Telegram e Twilio.

## Features

- Busca/seleciona província/município, resolve captcha e marca cita (fluxo padrão)
- Modo CERTIFICADOS CONCORDANCIA (apenas informa disponibilidade via Telegram)
- Captura de tela e recorte de captcha com OpenCV + Tesseract
- Notificações via Telegram (e Twilio opcional)
- Intervalo de busca configurável via `.env` com jitter ±20% para evitar bloqueios
- Loads configuration values from a `.env` file
- Pode ser empacotado com PyInstaller

## Requirements

- Python 3.6 or higher
- Selenium WebDriver
- Google Chrome or another supported browser
- ChromeDriver or another compatible WebDriver
- OpenCV
- Tesseract OCR
- Pytesseract
- Twilio
- python-dotenv

## Setup rápido

1. Crie e ative o venv.
2. `pip install -r requirements.txt`.
3. Instale o Tesseract OCR (Windows: `C:\Program Files\Tesseract-OCR\tesseract.exe`).
4. Baixe o `chromedriver.exe` compatível com seu Chrome e configure em `.env` `CHROMEDRIVER_BINARY=C:/tools/chromedriver.exe`.
5. Preencha `.env` com os dados (vide `env_example`).

## Execução

```bash
python automacao.py
```

- Escolha `1` para fluxo padrão (marcar cita) ou `2` para modo CONCORDANCIA (apenas alerta).
- O intervalo de repetição usa `INTERVALO_BUSCA_MINUTOS` com jitter ±20% para simular comportamento humano.
- Pausas curtas são inseridas entre interações para reduzir bloqueios.

## Variáveis principais (.env)

- `NOMBRE`, `DNI` (para modo concordancia) ou blocos `_1/_2` para fluxo padrão.
- `INTERVALO_BUSCA_MINUTOS`: base em minutos para intervalo entre tentativas (default 5, com jitter ±20%).
- `CHROMEDRIVER_BINARY`: caminho absoluto do chromedriver.
- `TELEGRAM_TOKEN`, `TELEGRAM_ID`: para alertas.
- Opcional teste Telegram: `TELEGRAM_TEST_TOKEN`, `TELEGRAM_TEST_CHAT_ID` (usados apenas em teste de integração).

## Modo CERTIFICADOS CONCORDANCIA

Fluxo determinístico por XPath:
1) Seleciona província `Valencia` e clica `Aceptar`.
2) Seleciona `POLICIA - CERTIFICADOS CONCORDANCIA` e clica `Aceptar`.
3) Clica `Entrar`.
4) Preenche `txtIdCitado` (DNI) e `txtDesCitado` (nome) e clica `Enviar`.
5) Se mensagem for “En este momento no hay citas disponibles...”, clica `Salir` e recomeça após intervalo com jitter.
6) Se houver disponibilidade, notifica Telegram e mantém navegador aberto para marcação manual.

Se aparecer tela de bloqueio “The requested URL was rejected / Your support ID...”, o navegador fecha e o contador reinicia.

## Testes

- Unitários: `python -m pytest tests/test_automacao_lib.py`
- Teste de integração Telegram (envia mensagem real): defina `TELEGRAM_TEST_TOKEN` e `TELEGRAM_TEST_CHAT_ID` e rode `python -m pytest -m integration tests/test_automacao_lib.py`

## Contributing

Feel free to fork the repository and submit pull requests with your improvements and bug fixes. You can also open issues to report bugs or request new features.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
