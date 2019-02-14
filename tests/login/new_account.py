import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import random
import string
import time
import datetime
import json

gAccounts = []
count = 0

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)


#driver = webdriver.Firefox()

with open("googlenoves.txt") as tf:

    for line in tf:
        gAccounts = line.split()
        email = gAccounts[0]
        passw = gAccounts[1]
        recov = gAccounts[2]

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