import email
import imaplib
import os

EMAIL = 'alfredosalvador2010@gmail.com'
PASSWORD = 'Pass@123'
SERVER = 'imap.gmail.com'
attachment_dir = 'C:/Users/gamac/Desktop/Projects/EmailAutomation/'
boolEmail = 0

#Habilitar Pop3 e IMAP: https://mail.google.com/mail/u/0/#settings/fwdandpop

#Permitir aplicações menos seguras:  https://myaccount.google.com/lesssecureapps

# abriremos uma conexão com SSL com o servidor de emails
# logando e navegando para a inbox
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
# selecionamos a caixa de entrada neste caso
# mas qualquer outra caixa pode ser selecionada

def get_attachments(msg):
    for part in msg.walk():
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join(attachment_dir, fileName)
            with open(filePath, 'wb') as f:
                f.write(part.get_payload(decode=True))


# selecionamos a caixa de entrada neste caso
# mas qualquer outra caixa pode ser selecionada
mail.select('inbox')

# faremos uma busca com o critério ALL para pegar
# todos os emails da inbox, esta busca retorna
# o status da operação e uma lista com
# os ids dos emails

# status, data = mail.search(None, 'ALL')
status, data = mail.search(None, '(UNSEEN)')

# data é uma lista com ids em blocos de bytes separados
# por espaço neste formato: [b'1 2 3', b'4 5 6']
# então para separar os ids primeiramente criaremos
# uma lista vazia
mail_ids = []
# e em seguida iteramos pelo data separando os blocos
# de bytes e concatenando a lista resultante com nossa
# lista inicial
for block in data:
    # a função split chamada sem nenhum parâmetro
    # transforma texto ou bytes em listas usando como
    # ponto de divisão o espaço em branco:
    # b'1 2 3'.split() => [b'1', b'2', b'3']
    mail_ids += block.split()

# agora para cada id baixaremos o email
# e extrairemos seu conteúdo
for i in mail_ids:
    # Existe novos emails
    boolEmail = 1
    # a função fetch baixa o email passando id e o formato
    # em que você deseja que a mensagem venha
    status, data = mail.fetch(i, '(RFC822)')

    # data no formato '(RFC822)' vem em uma lista com a
    # tupla onde o conteúdo está e o byte de fechamento b')'
    # por isso vamos iterar pelo data extraindo a tupla
    for response_part in data:
        # se for a tupla a extraímos o conteúdo
        if isinstance(response_part, tuple):
            # o primeiro elemento da tupla é o cabeçalho
            # de formatação e o segundo elemento possuí o
            # conteúdo que queremos extrair
            message = email.message_from_bytes(response_part[1])

            # com o resultado conseguimos pegar as
            # informações de quem enviou o email e o assunto
            mail_from = message['from']
            mail_subject = message['subject']

            # agora para o texto do email precisamos de um
            # pouco mais de trabalho pois ele pode vir em texto puro
            # ou em multipart, se for texto puro é só ir para o
            # else e extraí-lo do payload, caso contrário temos que
            # separar o que é anexo e extrair somente o texto
            if message.is_multipart():
                mail_content = ''

                # no caso do multipart vem junto com o email
                # anexos e outras versões do mesmo email em
                # diferentes formatos como texto imagem e html
                # para isso vamos andar pelo payload do email
                for part in message.get_payload():

                    # Se tiver anexo extrai
                    if part.get_content_type() == 'multipart/alternative':
                        print("Anexo")
                        get_attachments(message)
                        # se o conteúdo for texto text/plain que é o
                    # texto puro nós extraímos
                    if part.get_content_type() == 'text/plain':
                        print("Texto")
                        mail_content += part.get_payload()
            else:
                print("Texto2")
                mail_content = message.get_payload()

            # por fim vamos mostrar na tela o resultado da extração
            print(f'From: {mail_from}')
            print(f'Subject: {mail_subject}')
            print(f'Content: {mail_content}')
            print('#####################################################################')

if boolEmail == 0:
    print("Não tem novos emails")

mail.close()