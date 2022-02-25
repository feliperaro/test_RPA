import time
import os
import gvars
import json

# web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


def abrir_chrome():
    
    """
    Função abrir_chrome:
    
    Entrada:
        
    Retornos: 
        driver                        # Sucesso ao abrir o chrome.
    """

    chrome = True
    while chrome:
        path_idchrome = gvars.path_idchrome
        session_id, ip_pag = False, False
        if os.path.isfile(path_idchrome):
            with open(path_idchrome, "r") as f:
                processados = f.read()
                try:
                    ip_pag, session_id = processados.replace('"', "").split(" ")
                except:
                    pass
        
        if not session_id:
            path_driver = gvars.path_driver
            global driver
            driver = webdriver.Chrome(executable_path=path_driver)
            driver.maximize_window()

            url = driver.command_executor._url
            session_id = driver.session_id
            endereco = str(url) + " " + str(session_id)
            chrome = False
            with open(path_idchrome, "w") as f:
                json.dump(endereco, f)
            return driver
        else:
            driver = attach_to_session(ip_pag, session_id)
            
            try:
                for handle in driver.window_handles:
                    driver.switch_to.window(handle)
                    break
                return driver
            except: 
                path_idchrome = gvars.path_idchrome
                with open(path_idchrome, "w") as f:
                    json.dump("", f)


def attach_to_session(executor_url, session_id):
    try:
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.close()
        driver.session_id = session_id
        driver.implicitly_wait(0) # seconds
        return driver
    except:
        pass


def wait_execute_script(driver, script,*, timeout = 30):
    """
    Entradas:
        driver (obj) : Instância do chrome
        script (str) : script a ser executado
        timeout (int) : tentar executar por quanto tempo?
    """
    
    # se o script nao tiver retorno, 
    if script[:6] != "return":
        script = f"return {script}"
        
    # salva a hora que começou o loop
    time_begin = int(round(time.time() * 1000))
    while True: #loop infinito
        # se o loop já rodou por mais que 'timeout', retorna -1
        time_now = int(round(time.time() * 1000))
        if ((time_now - time_begin)/1000 >= timeout):
            return -1
            
        try:
            r = driver.execute_script(script)
            r = 1 if r is None else r
            return r
        except:
            time.sleep(1)


def wait_ready_state(*,driver, timeout = 60) :
    '''
    Descrição:
        Função para verificar o Ready State da página
    Inputs:
        driver (obj)          : Objeto do ChromeDriver
        timeout (int)         : Segundos para TimeOut
    Outputs:
         1 (int) : Retorno bem sucedido
        -1 (int) : Erro
    '''
    ind_timeout = 0
    element_founded = False
    ready_state = ""
    while ind_timeout <= timeout and element_founded != True:
        try:
            ready_state = driver.execute_script("return document.readyState")
            if ready_state == "complete" :
                element_founded = True
        except:
            time.sleep(1)
            ind_timeout += 1
    if ind_timeout > timeout :
        return -1
    return 1

