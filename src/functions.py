import lib_chromedriver
import time
import os 
import pandas as pd
import pandas.io.formats.excel


def extrai_dados_vagas(*, driver, timeout=60):
    # para garantir o carregamento da tela
    lib_chromedriver.wait_ready_state(driver=driver)

    # ids pagina
    id_grid = "pfolio"
    id_desc_vaga = "boxVaga"

    # scripts
    script_qtd_vagas = f'return document.getElementById("{id_grid}").children.length'
    script_desc_vaga_nome = f'return document.getElementById("{id_desc_vaga}").children[0].innerText'
    script_desc_vaga_descricao = f'return document.getElementById("{id_desc_vaga}").children[1].innerText'

    # pega a quantidade de vagas disponiveis na grid da pág
    grid_qtd_vagas = lib_chromedriver.wait_execute_script(
        driver=driver,
        script=script_qtd_vagas,
        timeout=timeout
    )

    # caso não consiga pegar a quantidade de vagas
    if grid_qtd_vagas < 0:
        print("Erro pegando a quantidade de vagas!")
        return -1

    # cria um list para armazenar os dados das vagas
    dados = []

    # percorre as vagas
    for id_vaga in range(1, grid_qtd_vagas):

        # cria um dict para armazenar os dados da vaga
        dados_da_vaga = dict()

        # xpaths
        xpath_local_vaga = "//*[@id='pfolio']/div[{id_vaga}]/div/p[1]"
        xpath_click_desc_vaga = f"//*[@id='pfolio']/div[{id_vaga}]/div/p[2]/a"

        timer = Timer(timeout)
        while timer.not_expired:
            try:
                # pega o local da vaga
                dados_da_vaga['local_vaga'] = None

                # deixei comentado os cod abaixo pois estava ocorrendo um bug que não estava pegando o valor via xpath :(
                # local_vaga = driver.find_element_by_xpath(xpath_local_vaga) 
                # dados_da_vaga['local_vaga'] = local_vaga

                # clica para ver as descrições da vaga
                driver.find_element_by_xpath(xpath_click_desc_vaga).click()
                break
            except:
                lib_chromedriver.wait_ready_state(driver=driver)
                continue

        # se o timeout expirar
        if timer.expired:
            print("Timeout expirou ao tentar acessar os detalhes da vaga!")
            return -2

        timer = Timer(timeout)
        while timer.not_expired:
            try:
                # pega o nome da vaga
                nome_vaga = lib_chromedriver.wait_execute_script(
                    driver=driver,
                    script=script_desc_vaga_nome
                )
                
                # pega a descrição da vaga
                desc_vaga = lib_chromedriver.wait_execute_script(
                    driver=driver,
                    script=script_desc_vaga_descricao
                )
            except:
                lib_chromedriver.wait_ready_state(driver=driver)
                time.sleep(2)
                continue

            break

        # se o timeout expirar
        if timer.expired:
            print("Timeout expirou ao tentar pegar os detalhes da vaga!")
            return -3
        
        # adiciona ao dict
        dados_da_vaga["nome_vaga"] = nome_vaga
        dados_da_vaga["desc_vaga"] = desc_vaga

        # adiciona o dict ao list de dados
        dados.append(dados_da_vaga)

        # volta a página
        driver.execute_script("window.history.go(-1)")

        # aguarda carregamento
        lib_chromedriver.wait_ready_state(driver=driver)

    return dados


def formata_dados_planilha(*, dados):

    # cria um list de cada coluna para armazenar os dados
    col_nome = ['NOME DA VAGA']
    col_local = ['LOCAL DA VAGA']
    col_desc_vaga = ['DESCRIÇÃO DA VAGA']

    # adiciona as inforamções recebidos ao list de cada coluna
    for dado in dados:
        col_nome.append(dado.get('nome_vaga'))
        col_local.append(dado.get('local_vaga'))
        col_desc_vaga.append(dado.get('desc_vaga'))

    # retorna o dict formatado
    return {
        'A': col_nome, 
        'B': col_local,
        'C': col_desc_vaga
    }

 
def get_xlsx_from_json(*, json, xls_name='default.xlsx', sheet_name='main', create_special_column=False, overwrite=True):
    """
    Get XLS From Json
    Objective:
        transform json in xlsx
    return in success:
        return name file as success
    return in error:
        -1, this file cant overwrite
        raise Exception, because the path is not valid or not is find
    """

    # If overwrite is False, Check if alread exists file with this xls_name
    if not overwrite and os.path.isfile(xls_name):
        return -1

    # Transform json (dict) in Dataframe
    df = pd.DataFrame(json) 

    # If create_special_column exists, create empty column with 'create_special_column' value
    if create_special_column and type(create_special_column) == str:
        df[str(create_special_column)] = pd.Series(dtype=str)

    # Change default style of pandas header
    pandas.io.formats.excel.ExcelFormatter.header_style = pandas.io.formats.excel.ExcelFormatter.header_style = {
        "font": {"bold": True, "color": '#f1faee'},
        "borders": {
            "top": "thin",
            "right": "thin",
            "bottom": "thin",
            "left": "thin",
        },
        "alignment": {"horizontal": "center", "vertical": "vcenter"},
        "fill": {"fgColor": "#1d3557", "patternType": "solid"}
    }

    # Initialize excelWriter in pandas, with xlsxwriter lib
    writer = pd.ExcelWriter(xls_name, engine="xlsxwriter")
    wb = writer.book

    # Transform Dataframe to excel, remove index and transform all NaN values as null
    df.to_excel(writer, sheet_name=sheet_name, index=False, na_rep='')

    # Define Basic cell style
    basic_cell = wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})

    # Define basic stripped cell style
    stripped_basic_cell = wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#f1faee'})

    # Define warning cell style, its is used in specials columns
    warning_cell = wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#e7a4aa'})

    # Loop in all columns in Dataframe for set column styles
    for column in df:
        # Get max length of chars in current column
        column_length = max(df[column].astype(str).map(len).max(), len(column))

        # Get idx of current column name
        col_idx = df.columns.get_loc(column)

        # Set column width
        writer.sheets[sheet_name].set_column(col_idx, col_idx, column_length + 10)

        # If create_special_column exists, create a conditional formatting for NaN values in this column
        if (create_special_column and type(create_special_column) == str) and column == create_special_column:
            writer.sheets[sheet_name].conditional_format(1, col_idx, len(df), col_idx, {
                'type': 'cell',
                'criteria': 'equal to',
                'value': '""',
                'format': warning_cell
            })

    # Loop in all rows in Dataframe for set row styles
    for row in range(0, len(df)+1, 2):
        # Define stripped style, and set this row height
        writer.sheets[sheet_name].set_row(row, 25, stripped_basic_cell)

        # Define stripped style, and set this row height
        writer.sheets[sheet_name].set_row(row+1, 25, basic_cell)

    # Save excel
    writer.save()

    # Return name of the xlsx
    return xls_name


class Timer:
    def __init__(self, duration=10):
        self.duration = float(duration)
        self.start = time.perf_counter()

    def reset(self):
        self.start = time.perf_counter()

    def explode(self):
        self.duration = 0

    def increment(self, increment=0):
        self.duration += increment

    @property
    def not_expired(self):
        # duration == -1 means dev wants a infinite loop/Timer
        if self.duration == -1:
            return True
        return False if time.perf_counter() - self.start > self.duration else True

    @property
    def expired(self):
        return not self.not_expired

    @property
    def at(self):
        return time.perf_counter() - self.start

