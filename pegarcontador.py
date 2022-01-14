#===============================================#
#   CRIADO EM 27/12/2021 PRA AUTOMATIZAR A      #
#   CONFERENCIA DE CONTADORES DAS IMPRESSORAS   #
#===============================================#

# Web Scrapping
from selenium import webdriver
from bs4 import BeautifulSoup
import time
# Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

matriz = []                                             #Onde os retonos são listados, esse é o resultado final

dict = {'JF - CPD':(192,168,4,163), 'JF - RH':(192,168,4,100),
        'JF - Faturamento':(192,168,4,3),'JF - Logistica':(192,168,4.123),
        'JF - WMS':(192,168,4,102),'JF - Faturamento 2':(192,168,4,117),
        'GV - Reserva':(192,168,1,206),'GV - Fiscal':(192,168,1,105),
        'GV - Financeiro':(192,168,1,102),'GV - Tesouraria':(192,168,1,190),
        'Capim 1':(192,168,5,109),'GV - RH':(192,168,1,65),
        'Capim 3':(192,168,5,65),'Capim - Devolução':(192,168,5,62),
        'GV - Comercial':(192,168,1,71),'Capim 2':(192,168,5,110),
        'Capim - Doca':(192,168,5,107),'Capim - Jonilson':(192,168,5,112),
        'JF - Financeiro 2':(192,168,4,208)}

# Criando a lista de chaves
lista_impressoras = []                                  #Serve apenas pra facilitar o laço

# BUSCANDO DADOS NO BROWSER - AQUI COMEÇA O CODIGO
options = webdriver.ChromeOptions()                     #Relacionando a atribuição ao processo
options.add_argument("--headless")                      #--headless --> abrir em segundo plano
driver = webdriver.Chrome(chrome_options=options)       #Abrindo navegador
for k in dict:
        try:
                ip_raw = dict[k]                        #Obtendo o .value
                ip = str(ip_raw)                        #transformando o resultado em string
                ip = ip.replace(', ', '.')              #trocando a virgula por ponto
                lista_impressoras.append(k)             #Salvando o percurso
                #print(f'Equipamento: {k} IP:{ip}')     #Apenas checando retorno

                # BUSCANDO DADOS NO BROWSER
                url = 'http://'+str(ip)[1:-1]+'/general/information.html?kind=item'     #[1:-1] Corta os parenteses
                driver.get(url)
                time.sleep(1)

                # Encontrando a div pelo XPath
                div_mae = driver.find_element_by_xpath('//*[@id="mainContent"]')
                html_content = div_mae.get_attribute('outerHTML')
                soup = BeautifulSoup(html_content, 'html.parser')

                # Filtrando as classes dentro da div
                lista_serial = soup.find_all("div", attrs={"class": "items"})
                lista_contador = soup.find_all("div", attrs={"class": "contentsGroup"})

                # Filtrando a tabela dentro da classe e armazenando na lista
                # driver.close()
                dd_list = soup.find_all("dd")
                #print(f'Equipamento: {dd_list[0].get_text()}')                 #Checando campo
                #print(f'Serial: {dd_list[1].get_text()}')                      #Checando campo
                #print(f'Contador: {dd_list[5].get_text()}')                    #Checando campo
                retorno = []                                                    #Limpando lista
                retorno.append(dd_list[0].get_text())
                retorno.append(dd_list[1].get_text())
                retorno.append(ip[1:-1])
                retorno.append(dd_list[5].get_text())
                matriz.append(retorno)                                          #Adicionando lista na matriz de resultados
                print(f'Retorno: {retorno}')                                    #Checando campo
                print(f'Matriz: {matriz}\n')                                    #Checando campo
                time.sleep(2)
                driver.execute_script(f"window.open('{url}', '_blank')")        #Abrindo nova aba
                time.sleep(6)
        except:
                print(f'impressora {k} está inacessível\n')
                pass
driver.close()

#ENVIANDO EMAIL COM A MATRIZ
# Configurando conta
username = "ti.chuadistribuidora@gmail.com"
password = "ogwrdhyimhyakvmz"
mail_from = "ti.chuadistribuidora@gmail.com"
mail_to = "apoio.ti@chuasa.com"
mail_subject = "Test Subject"
mail_body = matriz

# Criando mensagem
print('Criando mensagem...')
mimemsg = MIMEMultipart()
mimemsg['From']=mail_from
mimemsg['To']=mail_to
mimemsg['Subject']=mail_subject
mimemsg.attach(MIMEText(mail_body, 'plain'))


# Enviando mensagem
print('Enviando mensagem...')
connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
connection.starttls()
connection.login(username,password)
connection.send_message(mimemsg)
connection.quit()
print('Mensagem enviada!')





