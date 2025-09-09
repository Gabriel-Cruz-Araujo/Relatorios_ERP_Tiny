# 📊 Relatórios ERP Tiny

Automação inteligente para integração entre **Tiny ERP**, **Kommo CRM** e e-mail corporativo.  
O sistema realiza **extração, transformação e carga (ETL)** dos dados via API, gera relatórios de clientes por vendedor e envia automaticamente para os gerentes.  

---

## ✨ Funcionalidades
- 🔄 Integração com a API do **Tiny ERP** para coleta de dados.
- 🧹 Processamento e refinamento dos dados (ETL).
- 📑 Geração de relatórios de clientes por vendedor.
- 📧 Envio automático de relatórios por e-mail para os gerentes.
- ⚡ Menu interativo para facilitar o uso.

---

## 🚀 Tecnologias Utilizadas
- **Python 3.10+**
- [Pandas](https://pandas.pydata.org/) → manipulação de dados  
- [Requests](https://docs.python-requests.org/) → integração com APIs  
- [Yagmail](https://github.com/kootenpv/yagmail) → envio de e-mails  
- [Dotenv](https://pypi.org/project/python-dotenv/) → gerenciamento de variáveis de ambiente  

---

## 📂 Estrutura do Projeto
```
Relatorios_ERP_Tiny/
│── src/
│ ├── api/ # Pasta com os códigos de chamada a apis.
│ ├── ETL/ # Pasta com o código do ETL. 
│ ├── output/ # Pasta de saida das planilhas.
│ ├── relatorios/ # Pasta com o código para gerar o relatório de clientes.
│ ├── robos/ # Pasta com o código dos robôs do selenium.
│ ├── utils/ # Pasta com funções que são reultilizaveis.
│ └── src/ # Funções utilitárias
├── main.py # Arquivo principal 
├── README.md # Documentação
└── requirements.txt # Bibliotecas ultilizadas no projeto.
```
---

## ⚙️ Configuração do Ambiente

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Gabriel-Cruz-Araujo/Relatorios_ERP_Tiny.git
   cd Relatorios_ERP_Tiny/Relatórios
   ```
2. **Crie e ative um ambiente virtual***
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure suas variáveis de ambiente**
   ```.env
   TOKEN_API_TINY = "seu_token_aqui"
   ID_VENDEDOR_V = "id_vendedor"
   ID_VENDEDOR_K = "id_vendedor"
   ID_VENDEDOR_G = "id_vendedor"
    
   KOMMO_USERNAME = "seu_usuario"
   KOMMO_PASSWORD = "sua_senha"
   KOMMO_URL_RELATORIOS_DIA = "sua_url"
   
   EMAIL = "seu_email"
   SENHA_DE_APLICATIVO = "sua_senha_app"
   
   PASTA_CAMINHO_RELATORIO_VENDEDOR = "caminho_para_salvar_relatorios"
   
   ```
### ▶️ Como Usar

Execute o projeto com:
   ```bash
   python main.py
   ```
Um menu interativo será exibido para escolher entre:

- Relatório por vendedor
- Relatório de clientes trabalhados no dia anterior

---

## 📧 Envio Automático de Relatórios

Após a execução, o sistema:

- Consulta os dados no Tiny ERP.

- Gera relatórios no formato Excel.

- Envia automaticamente para os e-mails dos gerentes cadastrados.

---

## 🛡️ Segurança
  **⚠️ Atenção: nunca compartilhe o arquivo .env com credenciais reais. ⚠️** 
  
  **O arquivo .env já está no .gitignore.** 
  
  **⚠️ Tokens e senhas devem ser mantidos fora do versionamento. ⚠️** 
  
  **Revogue imediatamente credenciais que tenham sido expostas.** 

## 👨‍💻 Autor

Desenvolvido por [Gabriel Cruz Araujo](https://github.com/Gabriel-Cruz-Araujo)

Engenheiro de Software | Data & Automation Enthusiast
