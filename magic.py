#!/usr/bin/env python3


# -------------------------------------------------
# Author: Jhonathan Davi A.K.A jh00nbr
# E-mail: jdavi@insightsecurity.com.br
# Insightl4b: lab.insightsecurity.com.br
# jh00nbr: http://jhonathandavi.com.br
# Github: github.com/jh00nbr
# Twitter @jh00nbr
# -------------------------------------------------

import requests
import random
import sys

papel_ativos = ['AALR3','ABCB4','ABEV3','ADHM3','AFLT3','AGRO3','AHEB3','ALPA3','ALSC3','ALUP11','AMAR3','ANIM3','ARZZ3','ATOM3','AZEV3']
papel_all_cookies = {}

configs = {'dir_files' : 'papel_files/'}

def load_random_useragent():
    uas = []
    with open("user-agents.txt", 'r') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[0:-1-0])
    random.shuffle(uas)
    useragent_return = random.choice(uas)
    return useragent_return

def wFile(r, dir_files, file_name):
    handle = open(dir_files + file_name, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:  
            handle.write(chunk)
    handle.close()

    return True

def get_cookies_virgem():
    ''' Esta função obtem os novos cookies da página '''
    data = {'cookie':'', 'headers': ''}
    try:
        headers = {'User-Agent' : load_random_useragent()}
        req = requests.get("http://fundamentus.com.br/index.php", headers=headers)
        cookie = req.cookies['PHPSESSID']   
        data = {'cookie' : cookie, 'headers': req.request.headers}
    except Exception as e:
        data = {'cookie':'', 'headers':''}

    return data

def set_cookie_papel(papel, cookie):
    ''' Esta funçao cria um dicionario das ações com seus cookies exclusivos '''
    papel_all_cookies[papel] = cookie
    return True

def set_cookies_balanceHistoric(papel, SSID): # SSID = Cookie
    ''' Esta função atrela um cookie a uma determinada ação '''
    headers = {'User-Agent' : load_random_useragent(), 
            'Cookie':'PHPSESSID={SSID}'.format(SSID=SSID),
            'Referer':'http://fundamentus.com.br/detalhes.php?papel={papel}'.format(papel=papel)}
    try:        
        r = requests.get('http://fundamentus.com.br/balancos.php?papel={papel}&tipo=1'.format(papel=papel), headers=headers)
    except Exception as e:
        return "Error in requests [Set cookies balance Historic]"

def download_papel(papel, SSID):
    try:
        headers = {'User-Agent': load_random_useragent()}
        r = requests.get("http://fundamentus.com.br/planilhas.php?SID={SSID}".format(SSID=SSID), headers=headers, stream=True)      
        file_name = papel + "_" + r.headers['Content-Disposition'].split('filename=')[1] # Original output -> attachment; filename=bal_VITALYZE.zip - Output: [PAPEL]_bal_VITALYZE.zip

        wFile(r, configs['dir_files'], file_name)
        
    except Exception as e:
        return "Error in request - [Download Papel]"

def main():
    for papel in papel_ativos:
        print("[+] Obtendo cookies - Papel: [{papel}]".format(papel=papel), end='\r', flush=True)
        if get_cookies_virgem()['cookie']:
            cookie = get_cookies_virgem()['cookie']
            set_cookie_papel(papel, cookie)

    for papel, SSID in zip(papel_all_cookies.keys(), papel_all_cookies.values()):
        print("[+] Definindo cookies - Papel: [{papel}]".format(papel=papel), end='\r', flush=True)
        set_cookies_balanceHistoric(papel,SSID)

    for papel, SSID in zip(papel_all_cookies.keys(), papel_all_cookies.values()):
        print("[+] Baixando arquivos zips - Papel: [{papel}]".format(papel=papel), end='\r', flush=True)
        download_papel(papel,SSID)
       
if __name__ == '__main__':
    main()
    
    
