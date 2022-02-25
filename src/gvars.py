import os


# paths 
working_directory = os.getcwd()
path_idchrome = r"C:\chromedriver\id_chrome.json"
path_driver = r"C:\chromedriver\chromedriver.exe"
xlsx_name = rf'{working_directory}\\relatorio_vagas\\resultado.xlsx'

# ========== WEB ================= #
url_cadmus = "https://cadmus.com.br/vagas-tecnologia/"

mocked_dados_extraidos = [
    {
        'nome_vaga': 'Analista de Sistemas Sênior',
        'local_vaga' : 'Morumbi - SP',
        'desc_vaga': '• Conhecimento avançado em UML; • Experiência linguagem Java; • Experiência com frameworks Java como Spring, Springboot, Hibernate, Junit, Angular; • Experiência com Servidores de aplicação Jboss, Tomcat, Jetty; • Experiência com Oracle; • Experiência com Integração Continua e Entrega Continua; • Experiência com ferramenta Git; • Experiência com monolíticos e microsserviços;'
    }, 
    {
        'nome_vaga': 'Analista de Infraestrutura Bilingue',
        'local_vaga' : 'Morumbi - SP', 
        'desc_vaga': 'Experiência com Linux - avançado; Inglês- avançado para conversação;'
    },
    {
        'nome_vaga': 'Analista de Teste',
        'local_vaga' : 'Morumbi - SP',
        'desc_vaga': 'Requisitos: Avaliação de requisitos de testes. Definição de estratégia de testes. Planejamento de testes. Execução de testes funcional. Monitoramento e reporte de testes. Verificações em especificações de requisitos de sistemas / software.'
    },
    {
        'nome_vaga': 'Analista Jurídico Pl II',
        'local_vaga' : 'Morumbi - SP', 
        'desc_vaga': 'Responsabilidades: Triagem das notificações emitidas por órgãos e direcionamento às áreas de atuação. Follow up com áreas de atuação para encerramento das obrigações no sistema com base em evidências. Suporte nas demandar administrativas como elaboração de relatórios. Atas e apresentações. Dar suporte às lojas para acessar o sistema Archer e outros. Formação: Formado ou cursando Direito'
    }, 
    {
        'nome_vaga': 'Analista BI',
        'local_vaga' : 'Morumbi - SP', 
        'desc_vaga': 'Skills da vaga: - QlikView; - QlikSense; - Tableau; - Power BI; - Looker; - Superset; - Kibana. Analista de Dados/BI Skills da vaga: - Banco de Dados (DML/DDL) - SQL Server - Modelagem de Dados Relacional e Multidimensional. - ETL e automação (Integration Services) - BI (Cubos OLAP) - Git - Queries SQL, bancos relacionais e conhecimento de ecossistema Hadoop.'
    }, 
    {
        'nome_vaga': 'Tech Lead - Mobile',
        'local_vaga' : 'Morumbi - SP', 
        'desc_vaga': 'Tech Lead, com experiencia com Mobile Nativo + Android + Ios'
    }
]