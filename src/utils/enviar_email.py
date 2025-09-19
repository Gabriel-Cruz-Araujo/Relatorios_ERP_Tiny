import smtplib
import os
from dotenv import load_dotenv
import glob
from email.message import EmailMessage
import mimetypes
from datetime import datetime

load_dotenv()
data_hoje = datetime.now().strftime("%d-%m-%Y")
#L
def enviar_para_email():
    """
    Código para o envio do email com 
    as planilha em anexo.
    
    """
    
    lista_arquivos = glob.glob("C:/Users/equip/Documents/dev/planilhas/contatos_trabalhados_diario/*")
    ultimo_arquivo_dowload = max(lista_arquivos, key=os.path.getmtime)
    
    remetente = os.getenv("EMAIL") #coloque aqui o email que ira enviar o arquivo.
    destinatarios = ['gabrielindolfinho14@gmail.com'] #Coloque aqui o email da pessoa para ser enviada.
    assunto = 'RELATÓRIO DE CLIENTES TRABALHADOS NO DIA ANTERIOR'
    mensagem = """
    Relatório de clientes trabalhados no dia anterior.
    
    Att,
    """
    
    senha = os.getenv("SENHA_DE_APLICATIVO")
    anexo = ultimo_arquivo_dowload
    
    msg = EmailMessage()
    msg['From'] = remetente
    msg['To'] = destinatarios
    msg['Subject'] = assunto
    msg.set_content(mensagem)
    
    
    mime_type, _ = mimetypes.guess_type(anexo)
    mime_type, mime_subtype = mime_type.split('/')
    
    with open(anexo, 'rb') as arquivo:
        msg.add_attachment(arquivo.read(), maintype=mime_type, subtype=mime_subtype, filename=anexo)    
        
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
        email.login(remetente, senha)
        email.send_message(msg)

def enviar_para_email_relatorio_vendedor():
    """
    Código para o envio do email com 
    as planilha dos relatorios dos clientes com os vendedores.
    
    """
    pasta = ("C:/Users/equip/Documents/relatorios/relatorio_vendedores*")
    lista_arquivos = glob.glob(os.path.join(pasta, "*"))
    arquivos = sorted(lista_arquivos, key=os.path.getmtime, reverse=True)
    arquivos_para_enviar = arquivos[:3]
    
    
    remetente = os.getenv("EMAIL") #coloque aqui o email que ira enviar o arquivo.
    destinatarios = ['gabrielindolfinho14@gmail.com'] #Coloque aqui o email da pessoa para ser enviada.
    assunto = f'RELATÓRIO DE CLIENTES - {data_hoje}'
    mensagem = """
    Relatório de clientes de cada vendedor.
    
    Att,
    """
    
    senha = os.getenv("SENHA_DE_APLICATIVO")
    anexo = arquivos_para_enviar
    
    msg = EmailMessage()
    msg['From'] = remetente
    msg['To'] = destinatarios
    msg['Subject'] = assunto
    msg.set_content(mensagem)
    
    
    for anexo in arquivos_para_enviar:
        mime_type, _ = mimetypes.guess_type(anexo)
        if mime_type is None:
            mime_type = 'application/octet-stream' 
        mime_type, mime_subtype = mime_type.split('/')
        
        with open(anexo, 'rb') as arquivo:
            msg.add_attachment(
                arquivo.read(),
                maintype=mime_type,
                subtype=mime_subtype,
                filename=os.path.basename(anexo)
            )
    
    # Envia o email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
        email.login(remetente, senha)
        email.send_message(msg)
        print("Email enviado com sucesso!")

if __name__ == "__main__":
    enviar_para_email_relatorio_vendedor()