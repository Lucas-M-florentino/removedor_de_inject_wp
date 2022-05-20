import os
import shutil
from time import sleep
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

host = 'smtp.gmail.com'
port = 587
user = 'lucas.mmflorentino@gmail.com'
password = 'LuC@S_1998'
server = smtplib.SMTP(host, port)

#TEMPO = 10800
TEMPO = 60
NIVEL = "./"

def sendemail(sites):
    
    if len(sites) > 0:
        
        server.ehlo()
        server.starttls()
        server.login(user, password)
        texto = "Sites com arquivos inject encontrados:\n"
        for i in sites:
            texto = texto + i + "\n"
        msg = MIMEMultipart()
        msg['From'] = user
        msg['To'] = 'lucas.florentino2014@gmail.com'
        msg['Subject'] = 'Infection Found'
        msg.attach(MIMEText('Infection'))
        server.sendmail(msg['From'], msg['To'], texto)
        server.quit()

def executaLimpeza():
    print("Iniciando limpeza")
    print(os.listdir(NIVEL))
    # varrer arquivos das pastas dos sites
    pasta = os.listdir(NIVEL+'var/www/')
    # nome dos sites personalizados para serem pulados na verificação
    sitespersonalizados = ['domumimobiliaria.com.br','consultoriocostalourenco.com.br','armazemdopapelrp.com.br','jaciaraadvogada.com.br']
    conteudosCorretos = ['wordfence-waf.php','.user.ini','.htaccess', 'index.php', 'license.txt', 'readme.html', 'wp-activate.php', 'wp-admin', 'wp-blog-header.php', 'wp-comments-post.php', 'wp-config-sample.php', 'wp-content', 'wp-cron.php', 'wp-includes', 'wp-links-opml.php', 'wp-load.php', 'wp-login.php', 'wp-mail.php', 'wp-settings.php', 'wp-signup.php', 'wp-trackback.php', 'xmlrpc.php']

    injectarq = ['']
    injectpast = ['']
    injectap = ['']
    sitesdesinfectados = ['']
    for site in pasta:
        if site not in sitespersonalizados and site.find('.net') != -1 or site.find('.org') != -1 or site.find('.com') != -1:
            contpasta = os.listdir(NIVEL+'var/www/' + site+'/htdocs/')
            contsite = os.listdir(NIVEL+'var/www/' + site+'/')
            if 'wp-config.php' in contsite:
                print("site wordpress .... "+site)
                for cont in contpasta:

                    if cont not in conteudosCorretos and cont.find('.htaccess') == -1 and cont.find('index') == -1:
                        if cont.find('.') != -1:
                            injectarq.append(NIVEL+'var/www/' + site+'/htdocs/' + cont)
                        else:
                            injectpast.append(NIVEL+'var/www/' + site+'/htdocs/' + cont)
                        if site not in sitesdesinfectados:
                            sitesdesinfectados.append(site)
            elif 'ee-config.php' in contsite:
                print("site ExpressionEngine .... "+site)
                apontamento = True
                injectapaux = ['']
                for cont in contpasta:
                    if os.path.isdir(NIVEL+'var/www/' + site+'/htdocs/' + cont):
                        print('Site personalizado')
                        apontamento = False
                        break
                    if cont.find('index') == -1:
                        injectapaux.append(NIVEL+'var/www/' + site+'/htdocs/' + cont)
                if not apontamento:
                    if len(injectapaux) > 1:
                        injectapaux.clear()
                else:
                    if len(injectapaux) > 1:
                        injectapaux.pop(0)
                        injectap = injectap + injectapaux
                        if site not in sitesdesinfectados:
                            sitesdesinfectados.append(site)

    if injectarq[0] == '':
        injectarq.pop(0)
    while len(injectarq) > 0:
        os.remove(injectarq[0])
        injectarq.pop(0)

    if injectpast[0] == '':
        injectpast.pop(0)
    while len(injectpast) > 0:
        shutil.rmtree(injectpast[0])
        injectpast.pop(0)
    if injectap[0] == '':
        injectap.pop(0)
    while len(injectap) > 0:
        os.remove(injectap[0])
        injectap.pop(0)
    
    return sitesdesinfectados
    

def main(argv):
    print(len(argv))
    
    if len(argv) == 1:
        print(argv[0])
        if argv[0] == 'start':
            cont = TEMPO
            while True:
                if cont == TEMPO:
                    sites = executaLimpeza()
                    if sites != ['']:
                        sendemail(sites)
                    cont = 0
                sleep(1)
                cont += 1
    else:
        
        cont = 10800
        while True:
            if cont == 10800:
                sites = executaLimpeza()
                if sites != ['']:
                    sendemail(sites)
                cont = 0
            sleep(1)
            cont += 1

if __name__ == "__main__":

    main(sys.argv[1:])
