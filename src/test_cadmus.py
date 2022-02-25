import lib_chromedriver
import gvars
import functions
import json

# envia_email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def extrai_dados():
    # pega url e abre o chrome
    url = gvars.url_cadmus
    driver = lib_chromedriver.abrir_chrome()

    # acessa a url
    driver.get(url)

    # aguarda carregamento da pagina
    lib_chromedriver.wait_ready_state(driver=driver)

    # faz a extração dos dados
    dados_vagas = functions.extrai_dados_vagas(
        driver=driver
    )

    # valida retorno da extração dos dados
    if isinstance(dados_vagas, int) and dados_vagas < 0:
        print("Erro extraindo dados das vagas!")
        return -1

    return dados_vagas


def gera_relatorio(*, dados_relatorio):
    print(f"dados_relatorio ->\n\t{json.dumps(dados_relatorio, indent=2)}")    

    # formata os dados para criar o xlsx
    dados_formatados = functions.formata_dados_planilha(dados=dados_relatorio)

    # criar planilha de saida
    get_xlsx_from_json_resultado = functions.get_xlsx_from_json(
        json = dados_formatados,
        xls_name = gvars.xlsx_name,
        sheet_name="Resultados"
    ) # Criando a planilha

    # valida retorno
    if type(get_xlsx_from_json_resultado) == str:
        print(f"# ==== Planilha foi criada com sucesso no caminho {get_xlsx_from_json_resultado}")
        return get_xlsx_from_json_resultado
    elif get_xlsx_from_json_resultado == -1:
        print(f"# [RPAReset] ==== Planilha não foi criada pois já existe!")
        return -1
    else:
        return -3


def envia_email(*, email_from, password_email, email_to, subject, body, path_file):
    # envio de email
    try:
        print("Inicio envio de email")
        
        msg = MIMEMultipart()
        msg['From'] =  email_from

        msg['To'] = email_to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        attachment = open(path_file,'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % path_file)

        msg.attach(part)
        attachment.close()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(email_from, password_email)
        text = msg.as_string()

        server.sendmail(email_from, email_to, text)
        server.quit()

        print('\nEmail enviado com sucesso!')
    except Exception as e:
        print(f"{e}\nErro ao enviar email")
        return -1
        
    return 1

    
def main():
    dados_extraidos = extrai_dados()
    # dados_extraidos = gvars.mocked_dados_extraidos # teste

    if isinstance(dados_extraidos, int) and dados_extraidos < 0:
        print("Erro realizando a extração dos dados...")
        return

    path_relatorio = gera_relatorio(dados_relatorio=dados_extraidos)
    if isinstance(path_relatorio, int) and path_relatorio < 0:
        print("Erro gerando realtório de vagas...")
        return

    remetente_email = 'robot@cadmus.com'
    senha_remetente = None
    receber_email = ['feliperamosroque@gmail.com']

    envia_email(
        email_from=remetente_email,
        password_email=senha_remetente,
        email_to=receber_email,
        subject="Relatório analítico de vagas abertas - Cadmus",
        body="Segue em anexo relatório de vagas abertas da Cadmus\nPor gentileza não responder este email.",
        path_file=path_relatorio
    )

    if envia_email < 0:
        print("Erro enviando email...")
        return


# executar main
main()