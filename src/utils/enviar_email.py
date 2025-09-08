import smtplib
import os
from dotenv import load_dotenv
import glob
from email.message import EmailMessage
import mimetypes

load_dotenv()

#L
def enviar_para_email():
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
        
if __name__ == "__main__":
    enviar_para_email()