# coding=utf-8

#
# * RECODE? OKE GAK MASSALAH
# * TAPI YA JANGAN DI JUAL KONTOL
#

############################################################
# Name           : Moonton Account Checker                 #
# File           : proxy.py                              #
# Author         : DulLah                                  #
# Github         : https://github.com/dz-id                #
# Facebook       : https://www.facebook.com/dulahz         #
# Telegram       : https://t.me/DulLah                     #
# Python version : 3.7++                                   #
############################################################

import requests, os, shutil
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor

try: shutil.rmtree(
    'get_proxy/__pycache__'
  )
except: pass

proxy_list = []
valid_proxy = []

def prox():
  print('''
[1] Ambil proxy dari situs (free-proxy-list.com)
[2] Ambil proxy dari situs (free-proxy-list.net)[\033[92mDisarankan\033[0m]
[3] Dari file
  ''')
  ask = int(
    input(
      '[?] Chose: '
    )
  )
  if ask == 1:
    return proxy_com(
    )
  elif ask == 2:
    return proxy_net(
    )
  elif ask == 3:
    return from_file(
    )
  else:
    exit(
      '\n[!] Goblokk ajg, elu butaa yaaa?'
    )

def proxy_checker(prox):
  try:
    global valid_proxy
    if requests.get(
       'http://ip.ml.youngjoygame.com:30220/myip',
          verify=False,
          proxies=prox,
          timeout=10
        ).status_code == 200:
      valid_proxy.append(
        prox
      )
    print(
      end='\r[+] Ditemukan (%s) proxy valid.'%(
        len(
          valid_proxy
        )
      ),
      flush=True
    )
  except: pass

def proxy_com():
  limit = int(
    input(
      '[?] Limit (ex: 100): '
    )
  )
  count = 1
  stop = False
  url = 'https://free-proxy-list.com?page=%s' %(
    str(
      count
    )
  )
  while 1:
    try:
      found = False
      r = requests.get(
        url,
        headers={'user-agent':'chrome'}
      ).text
      soup = bs(
        r,
        'html.parser'
      )
      for x in soup.find_all('a'):
        if x.has_attr(
          'alt'
        ) == True:
          proxy = (
            x['alt']
          )
          found = True
          proxy_list.append({
            'http':'http://'+proxy.strip(),
            'https':'https://'+proxy.strip()
          }) if len(
            proxy.strip().split(':')
          ) == 2 else None
          print(
            end='\r[+] Mengambil (%s) proxy.'%(
              len(proxy_list)
            ),
            flush=True
          )
          if len(
            proxy_list
          ) == limit or len(
            proxy_list
          ) > limit:
            stop = True
            break
      if found == False:
        print(
          '\n[!] Hanya bisa mengambil (%s) proxy' %(
            str(
              len(
                proxy_list
              )
            )
          )
        )
        break
      elif stop == False:
        count+=1
        url = 'https://free-proxy-list.com?page=%s' %(
          str(
            count
          )
        )
      else:
        break
    except: pass
  if len(
    proxy_list
  ) != 0:
    print(
      '\n[*] Mencari proxy valid'
    )
    with ThreadPoolExecutor(
      max_workers=50
      ) as thread:
      [
        thread.submit(
          proxy_checker,(
            prox
          )
        ) for prox in proxy_list
      ]
    if len(
      valid_proxy
    ) != 0:
      print(
        '\n'
      )
      return valid_proxy
    else: exit(
      '[!] Maaf tidak ada proxy yang valid silahkan coba lagi :('
    )
  else: exit(
    '[!] Maaf proxy tidak ada :('
  )

def proxy_net():
  print(
    '[*] Mencari proxy valid'
  )
  r = requests.get(
    'https://free-proxy-list.net/',
    headers={'user-agent':'chrome'}
  ).text
  soup = bs(
    r,
    'html.parser'
  )
  proxs = soup.find(
    'textarea'
  ).text.split(
    '\n'
  )
  [
    proxy_list.append({
      'http':'http://'+e.strip(),
      'https':'https://'+e.strip()
    }) if len(
      e.strip(
      ).split(
        ':'
      )
    ) == 2 else None for e in proxs
  ]
  if len(
    proxy_list
  ) != 0:
    with ThreadPoolExecutor(
      max_workers=50
      ) as thread:
      [
        thread.submit(
          proxy_checker,(
            prox
          )
        ) for prox in proxy_list
      ]
    if len(
      valid_proxy
    ) != 0:
      print(
        '\n'
      )
      return valid_proxy
    else: exit(
      '[!] Maaf tidak ada proxy yang valid silahkan coba lagi :('
    )
  else: exit(
    '[!] Maaf proxy tidak ada :('
  )

def from_file():
  print(
    '\n[!] Pemisah ip:port ex: 10.1.3:8080'
  )
  list = input(
    '[?] List proxy (ex: proxy.txt): '
  )
  if os.path.exists(
    list
  ):
    for data in open(
      list,
      'r',
      encoding='utf-8'
    ).readlines(
      ):
      prox = data.strip(
      ).split(
        ':'
      )
      try:
        if prox[0] and prox[1]:
          proxy_list.append({
            'http': 'http://'+data.strip(),
            'https': 'https://'+data.strip(),
          })
      except: pass
    if len(
      proxy_list
    ) != 0:
      print(
        '[*] Total (%s) proxy' %(
          str(
            len(
              proxy_list
            )
          )
        )
      )
      print(
        '[*] Mencari proxy valid'
      )
      with ThreadPoolExecutor(
        max_workers=50
      ) as thread:
        [
          thread.submit(
            proxy_checker,(
              prox
            )
          ) for prox in proxy_list
        ]
      if len(
        valid_proxy
      ) != 0:
        print(
          '\n'
        )
        return valid_proxy
      else: exit(
        '[!] Maaf tidak ada proxy yang valid silahkan coba lagi :('
      )
    else: exit(
      '[!] Maaf proxy tidak ada :('
    )
  else: exit(
    '[!] File tidak ditemukan "{0}"'.format(
      list
    )
  )