# -*- coding: utf-8 -*-

import requests, os, argparse, re
from bs4 import BeautifulSoup

parse = argparse.ArgumentParser()
parse.add_argument('-t', help='Judul Film', dest='title')
parse.add_argument('-r', help='Resolusi', dest='reso')
args = parse.parse_args()

judul = args.title
areso = args.reso

W  = '\033[0m'    # white (default)
R  = '\033[1;31m' # red
G  = '\033[1;32m' # green bold
O  = '\033[1;33m' # orange
B  = '\033[1;34m' # blue
P  = '\033[1;35m' # purple
C  = '\033[1;36m' # cyan
GR = '\033[1;37m' # gray

def banner(judul):
    os.system('clear')
    print(W)
    print("  ██╗     ██╗  ██╗██╗  ██╗██████╗  ██╗")
    print("  ██║     ██║ ██╔╝╚██╗██╔╝╚════██╗███║")
    print("  ██║     █████╔╝  ╚███╔╝  █████╔╝╚██║")
    print("  ██║     ██╔═██╗  ██╔██╗ ██╔═══╝  ██║")
    print("  ███████╗██║  ██╗██╔╝ ██╗███████╗ ██║")
    print("  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═╝")
    print(C)
    if not judul:
        print("  ════════════════════════════════════")
    else:
        print(f"  {judul}")
    print(W)

if not judul:
    banner('')
    judul = input(" Masukkan Judul : ")

lk21 = "https://lk21.xn--6frz82g/"
download = "http://dl.sharemydrive.xyz/"
# download = "http://dl.indexmovies.xyz/"

req = requests.get(lk21, params={"s":judul}).text
soup = BeautifulSoup(req, "html.parser")
link = soup.find_all('h2')[2]
try:
    judul = re.search(r'<a href="'+lk21+'(.*)/" rel="bookmark"', str(link)).group(1)
except AttributeError:
    judul = re.search(r'<a href="'+lk21+'(.*)/" rel="bookmark"', str(link))
try:
    banner(judul)
    dload = download + "get/" + judul
    verif = download + "verifying.php"
    data = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Accept":"*/*",
            "X-Requested-With":"XMLHttpRequest"}
    req = requests.post(verif, headers=data, params={"slug":judul}).text
    soup = BeautifulSoup(req, "html.parser")
    link = soup.find_all('a')
    if not areso:
        resolusi = ["360","480","720","1080"]
    else:
        resolusi = [areso]
    for reso in resolusi:
        ress = re.findall(r'btn-'+reso+'" href="(.*)" rel=', str(link))
        if len(ress) > 0:
            for down in ress:
                if 'cdn' in down:
                    print(C+"  "+reso+R+" : "+W+down.rsplit('" target', 1)[0])
                    print(C+"  "+reso+R+" : "+W+down.rsplit('"', 1)[-1])
                else:
                    print(C+"  "+reso+R+" : "+W+down)
        else:
            if areso:
                print(R+"  !! "+W+"Resolusi "+reso+" tidak ditemukan")
except:
    print(R+"  !! "+W+"Film tidak ditemukan")
print ("")