import subprocess
import os
import requests as r
from bs4 import BeautifulSoup
import argparse


def downloadrepos(language):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--nrepos', type=int, required=False, default=100)
    args = parser.parse_args()
    numrepos = args.nrepos
    repos = 'target'
    repos2 = '/home/zuoqin/volatility/target'
    if not os.path.isdir(repos):
        os.makedirs(repos)
    result = r.get('https://github.com/trending/{}?since=daily'.format(language))
    soup = BeautifulSoup(result.text)
    for city in soup.find_all('h1', {'class': 'h3 lh-condensed'}):
        if numrepos <= 0:
            break
        numrepos = numrepos - 1
        path = city.a['href'].split('/')
        if not os.path.isdir(os.path.join(repos, path[len(path) - 2])):
            os.makedirs(os.path.join(repos, path[len(path) - 2]))
        thepath = os.path.join(repos, path[len(path) - 2], path[len(path) - 1])
        thepath2 = os.path.join(repos2, path[len(path) - 2], path[len(path) - 1])
        print('Consither: ', thepath)
        if not os.path.isdir(thepath) and not os.path.isdir(thepath2):
            # Huawei proxy connection
            #subprocess.run(['wget', 'https://github.com' + city.a['href'] + '/archive/master.zip'],
            #               cwd=os.path.join(repos, path[len(path) - 2]))
            #subprocess.run(['unzip', '-o', 'master.zip', '-d', os.path.abspath(thepath2)],
            #               cwd=thepath2)
            #print('Work with: ', thepath2)
            # Normal connection
            subprocess.run(['git', 'clone', 'https://github.com' + city.a['href'] + '.git'],
                           cwd=os.path.join(repos, path[len(path) - 2]))


if __name__ == "__main__":
    for lang in ['go', 'java', 'clojure', 'scala', 'javascript', 'python', 'haskell', 'c', 'cpp', 'c#', 'erlang', 'f#', 'r', 'ruby', 'kotlin', 'typescript', 'elixir']:
        downloadrepos(lang)
