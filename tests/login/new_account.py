import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import random
import string
import time
import datetime
import json

import utils
import sys

gAccounts = []
count = 0



# driver = webdriver.Remote(
#     'http://127.0.0.1:4444/wd/hub',
#     options.to_capabilities()
# )

logger = utils.get_logger()
driver = 0

def driver_setup():
    global driver
    options = webdriver.ChromeOptions()
    #driver = webdriver.Chrome(options=options)
    driver = webdriver.Remote(
        command_executor = 'http://192.168.56.1:9515',
        desired_capabilities=options.to_capabilities()
    )

def driver_teardown():
    global driver
    logger.info("Terminating session")
    driver.quit()


def check_page(locator, inner_text):
    item = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,locator)))
    if inner_text in item.text:
        logger.info("Located '" + inner_text + "'")
    else:
        raise Exception('Page html item not found')

def identity_implementation():
    logger.info("identity_implementation ")
    recover = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(),"Confirma tu")]')))
    time.sleep(1)
    recover.click()
    time.sleep(1)

    emailrecover = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//input[@id = "identifierId"]')))
    emailrecover.send_keys(recov)

    time.sleep(1)
    nextB = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Siguiente"]')))
    nextB.click()
    time.sleep(20)

def login(email, password):
    global driver

    loginF = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//input[@id = "identifierId"]')))
    loginF.send_keys(email)
    nextB = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Siguiente"]')))
    nextB.click()
    time.sleep(1)
    passwordF = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
    passwordF.send_keys(password)
    passnext = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Siguiente"]')))
    passnext.click()
    time.sleep(5)

    # Verfica que eres tú
    logger.info("Checking identity ...")
    try:
        check_page('h1#headingText', 'Verifica que eres')
        identity_implementation()
    except Exception as e:
        logger.error("Not found 'Verifica que eres tu'")
        #print(e)

def advertising_goal():
    global driver

    try:
        check_page('h2.title', 'advertising goal')

        logger.info("Located advertising goal")
        item_goal = driver.find_element_by_css_selector('material-expansionpanel-set material-expansionpanel:nth-child(3)')

        # Unfolding menu
        logger.info("Unfolding menu ...")
        item = item_goal.find_element_by_css_selector('material-icon')
        item.click()

        # Click on 'Pick Goal' (Hover required)
        item = item_goal.find_element_by_css_selector('div.toolbelt material-button')
        hover = ActionChains(driver).move_to_element(item)
        hover.perform()
        time.sleep(2)

        item.click()

    except Exception as e:
        logger.error("Not found 'Verifica que eres tu'")
        print(e)



def describe_your_business():
    global driver

    inner_text = 'Describe your business'
    try:
        # Check whether proper page
        check_page('h2.title', inner_text)

        logger.info("Located '" + inner_text + "'")
        item = driver.find_element_by_css_selector('material-input .input')
        item.send_keys("Sport")

        print(item.get_attribute('outerHTML'))


    except Exception as e:
        logger.error("Not found '" + inner_text + "'")
        print(e)


if __name__ == "__main__":

    logger.info("Starting logger")

    # Setup driver
    driver_setup()

    line = "dralli060@gmail.com,hnAWp1C4nj,jodi414l0l@hotmail.com"
    email = line.split(',')[0]
    password = line.split(',')[1]
    recov = line.split(',')[2]

    logger.info("Generating for " + email)

    driver.get("https://ads.google.com/aw/billing/paymentmethods")

    # Login
    logger.info("Performing login ...")
    login(email, password)
    logger.info("DONE!")

    # Select target
    logger.info("advertising goal ...")
    advertising_goal()
    logger.info("DONE!")

    # Describe your business
    logger.info("describe your business ...")
    describe_your_business()
    logger.info("DONE!")

    # Wait for some time
    logger.info("About to abort ...")
    time.sleep(20)

    # Tear down
    driver_teardown()
    sys.exit(0)

#####################

with open("./googlenoves.txt") as tf:

    logger.info("Read file")

    for line in tf:
        gAccounts = line.split()
        email = gAccounts[0]
        passw = gAccounts[1]
        recov = gAccounts[2]

        logger.info("Generating for " + email)

        driver.get("https://ads.google.com/aw/billing/paymentmethods")

        loginF = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//input[@id = "identifierId"]')))
        loginF.send_keys(email)
        nextB = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Siguiente"]')))
        nextB.click()
        time.sleep(1)
        passwordF = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
        passwordF.send_keys(passw)
        passnext = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Siguiente"]')))
        passnext.click()
        time.sleep(2)

        # #verifica email
        # recover = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(),"Confirma tu")]')))
        # time.sleep(1)
        # recover.click()
        # time.sleep(1)
        #
        # emailrecover = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//input[@id = "identifierId"]')))
        # emailrecover.send_keys(recov)
        #
        # time.sleep(1)
        # nextB = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Siguiente"]')))
        # nextB.click()
        # time.sleep(5)

        logger.info("Logged Ok!")

        #Proteger tu cuenta
        try:
            ProtegeMsg = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Proteger tu cuenta")]')))
            if ProtegeMsg:
                driver.get("https://ads.google.com/um/Welcome/Home?a=1&authuser=0#oa")
                time.sleep(5)
                continue
            else:
                pass
        except:
            pass

        try:
            webMsg = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="www.example.com/libros"]')))
            if webMsg:
                web = "www.sport.es"
                webMsg.send_keys(web)
                time.sleep(2)
                continue
            else:
                pass
        except:
            pass

        try:
            boto = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@id="gwt-debug-about-page-tips-opt-in-radio-checkbox"]')))
            if boto:
                boto.click()
                time.sleep(2)
                continue
            else:
                pass
        except:
            pass

        try:
            continuar = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="goog-button-base-content"]')))
            if continuar:
                continuar.click()
                time.sleep(30)
                continue
            else:
                pass
        except:
            pass

        try:
            if Presu:
                Presu = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="aw-text umnb-e"]')))
                aldia = "10"
                Presu.send_keys(aldia)
                time.sleep(15)
                continue
            else:
                pass
        except:
            pass

        try:
            Guardar = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="goog-button-base-pos"] | //span[@id = "gwt-debug-budget-editor-save-button-content"]')))
            if Guardar:
                Guardar.click()
                time.sleep(5)
                continue
            else:
                pass
        except:
            pass

        try:
            Guardar2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(), "Guardar")] | //span[@id = "gwt-debug-keywords-editor-save-button-content"]')))
            if Guardar2:
                Guardar2.click()
                time.sleep(5)
                continue
            else:
                pass
        except:
            pass

        time.sleep(5)
        Titulo1Msg = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Hotel económico en Madrid"]')))
        Titulo1 = "d"
        Titulo1Msg.send_keys(Titulo1)
        time.sleep(1)

        Titulo2Msg = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Hoteles económicos en Madrid"]')))
        Titulo2 = "d"
        Titulo2Msg.send_keys(Titulo2)
        time.sleep(1)

        DescMsg = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//textarea[@class="umec-b"]')))
        Descrip = "d"
        DescMsg.send_keys(Descrip)
        time.sleep(1)

        Guardar3 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Guardar y continuar"]')))
        Guardar3.click()
        time.sleep(15)

        #facturacio
        Nombre = "Ramon Lloveras"
        NombreE = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="ORGANIZATION"]')))
        NombreE.send_keys(Nombre)
        time.sleep(2)

        Direccio = "Carrer Mestra Numancia "
        DireccioB = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="ADDRESS_LINE_1"]')))
        DireccioB.send_keys(Direccio)
        time.sleep(5)

        Direccio2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="ac-row ac-active active"]')))
        Direccio2.click()
        time.sleep(2)

        '''

        CP = "17252"
        CPB = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="POSTAL_CODE"]')))
        CPB.send_keys(CP)
        time.sleep(1)

        Ciutat = "Calonge"
        CiutatB = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="LOCALITY"]')))
        CiutatB.send_keys(Ciutat)
        time.sleep(1)

        '''

        ClickTarj = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(), "Añadir tarjeta de"]')))
        ClickTarj.click()
        time.sleep(2)

        ClickBanc = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(), "Añadir una cuenta bancaria"]')))
        ClickBanc.click()
        time.sleep(2)

        Titular = "Ramon Lloveras"
        TitularB = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="FIELD_ACCOUNT_HOLDER_NAME"]')))
        TitularB.send_keys(Titular)
        time.sleep(2)

        IBAN = "ES0901827402500201652281"
        CodigoIBAN = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="FIELD_IBAN"]')))
        CodigoIBAN.send_keys(IBAN)
        time.sleep(2)

        SWIFT = "BSCHESMG"
        SWIFTBic = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@name="FIELD_SWIFT_BANK_IDENTIFIER_CODE"]')))
        SWIFTBic.send_keys(SWIFT)
        time.sleep(2)

        Verificar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(), "Verificar"]')))
        Verificar.click()
        time.sleep(5)

        Confirmar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="b3-checkbox-check-hider"]')))
        Confirmar.click()
        time.sleep(2)

        Aceptar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(), "Aceptar"]')))
        Aceptar.click()
        time.sleep(3)

        Listo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[contains(text(), "Listo"]')))
        Listo.click()
        time.sleep(3)

        Acepto = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="b3-checkbox-check-hider"]')))
        Acepto.click()
        time.sleep(3)

        Finalizar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//span[text()="Finalizar y crear el anuncio"]')))
        Finalizar.click()
        time.sleep(6)


        driver.get("https://accounts.google.com/Logout")
        driver.delete_all_cookies()





#if count == len(gAccounts):
if True:
    print('\nAccounts have been removed from all gmail accounts')
    driver.quit()

else:
    print('\nSigning out of this account and jumping to the next one!',email)
    driver.get("https://accounts.google.com/Logout")
    driver.delete_all_cookies()
