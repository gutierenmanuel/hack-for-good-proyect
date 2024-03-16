
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pyperclip


numero_chat_ = 1


def new_chat(driver1):

    nuevo_chat = '#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.dark.flex-shrink-0.overflow-x-hidden.bg-black > div > div > div > div > nav > div.flex-col.flex-1.transition-opacity.duration-500.-mr-2.pr-2.overflow-y-auto > div.sticky.left-0.right-0.top-0.z-20.bg-black.pt-3\.5 > div > a'

    boton_nuevo_chat = driver1.find_element(By.CSS_SELECTOR, nuevo_chat)

    boton_nuevo_chat.click()
    

def close_driver(driver1):


    driver = driver1

    # Cerrar el navegador al finalizar
    driver.quit()


def open_driver():

    max_retries = 3
    for retry in range(max_retries):
        try:
            options = uc.ChromeOptions()
            options.headless = False  # Cambia a True si deseas que sea headless (sin interfaz gráfica)
            options.add_argument("--disable-blink-features=AutomationControlled")

            options.user_data_dir = ""

            
            driver = uc.Chrome(options = options,
                user_data_dir='/home/tr4shhh/Proyects/Chrome_profile/Perfil_uc_portatil/', # CUALQUIER CARPETA PERFIL
                browser_executable_path='/usr/bin/chromium-browser', # RUTA DEL EJECUTABLE DEL NAVEGADOR
                )

            time.sleep(3)

            # Establecer el tamaño de la pantalla (ancho x alto)
            driver.set_window_size(1200, 800)

            driver.get( 'https://chat.openai.com/' )  

            return driver

        except Exception as e:
            print(f"Error en el intento {retry + 1}: {e}")



def scrap_gpt(driver1, prompt):
    
    driver = driver1

    global numero_chat_

    prompt_a_enviar = prompt

    #Seleccionamos el input e introducimos 
    css_input = '#prompt-textarea'
    input = driver.find_element(By.CSS_SELECTOR , css_input)
    input.send_keys(prompt_a_enviar)

    time.sleep(3)

    input.send_keys(Keys.ENTER)

    numero_chat = int(numero_chat_) *2+1

    time.sleep(3)


    # Css selectores

    valor_css = f'#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col > div.flex-1.overflow-hidden > div > div > div > div:nth-child({str(numero_chat)}) > div > div > div.relative.flex.w-full.flex-col.agent-turn > div.flex-col.gap-1.md\:gap-3 > div.mt-1.flex.justify-start.gap-3.empty\:hidden > div > span:nth-child(2) > button'


    # Bucle hasta encontrar el elemento 

    for i in range(120):

        time.sleep(0.5)
        try: 
            
            comprobar_elemento = driver.find_element(By.CSS_SELECTOR, valor_css)
            break

        except NoSuchElementException:
            pass


    boton  = driver.find_element(By.CSS_SELECTOR, valor_css )

    time.sleep(1)

    boton.click()

    time.sleep(1)

    contenido_portapapeles = pyperclip.paste()


    numero_chat_ += 1

    return contenido_portapapeles


