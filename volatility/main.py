# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import re
import argparse
import logging
import statistics
import requests
import json
import shutil
from datetime import datetime
from multiprocessing.dummy import Pool

logging.basicConfig(level=logging.WARNING)


def calculate(dir, index):
    result = subprocess.run(['git', '--git-dir', dir + '/.git', 'log',
                             '--reverse',
                             '--format=short',
                             '--stat=1000', '--stat-name-width=950'],
                            stdout=subprocess.PIPE)
    # Alternative solution
    # cmd = 'git --git-dir {}/.git log --reverse --format=short --stat=1000'\
    # ' --stat-name-width=950 > out/out_file{}.txt'.format(dir, index)
    # os.system(cmd)
    # f = open('out/out_file' + str(index) + '.txt', "r")
    # data = f.read()
    # f.close()

    try:
        data = result.stdout.decode("utf-8")
    except Exception:
        try:
            data = result.stdout.decode("latin-1")
        except Exception:
            with open('files_out3.txt', 'a+') as the_file:
                the_file.write(dir + '\n')
            return {'files': {}, 'commits': 0}

    return parse(data)


def find_next_commit(pos1, input):
    pos2 = input.find('commit ', pos1)
    if pos2 < 0 or pos2 < pos1:
        return -1
    pos1 = pos2
    pos2 = input.find('Author: ', pos1)
    pos2 = input.find('\n', pos2+1)
    pos2 = pos2 + 2
    pos1 = input.find('\n', pos2+1)
    while pos1 - pos2 > 3 and pos1 >= 0 and pos2 >= 0:
        pos1 = pos1 + 1
        pos2 = pos1
        pos1 = input.find('\n', pos2)
    if pos2 < 0:
        return pos2
    pos1 = pos2 + 1
    return pos1


def parse_file(file):
    f = open(file, "rb")
    data = f.read().decode("UTF-8")
    f.close()
    return parse(data)


def parse(input):
    files = {}
    line = ''
    num = 1
    pos1 = find_next_commit(0, input)
    if pos1 >= 0:
        logging.info('Commit: {}'.format(num))
    num = num + 1
    while(pos1 < len(input) and pos1 >= 0):
        pos2 = input.find('|', pos1)
        pos3 = input.find('\n', pos1)
        line = input[pos1:pos3]
        if 'changed,' in line or line[0:6] == 'commit':
            if input.find('commit', pos1+1) > 0:
                pos1 = find_next_commit(pos1, input)
                logging.info('Commit: {}'.format(num))
                num = num + 1
                continue
            else:
                if line[0:6] == 'commit':
                    logging.info('Commit: {}'.format(num))
                break
        else:
            file = input[pos1:pos2].strip()
            if "=>" in file:
                f = file.split("=>")
                if f[0] in files:
                    prev = files[f[0]]
                    del files[f[0]]
                    files[f[1]] = prev
                    res = re.findall(r'\d+', input[pos2 + 1:pos3])
                    if int(res[0]) > 0:
                        files[f[1]] = prev + 1
            else:
                if file in files:
                    files[file] = files[file] + 1
                else:
                    files[file] = 1
        pos1 = pos3 + 1
    return {'files': files, 'commits': num}


def get_repo_detail(link, token):
    if link[-1:] == '/':
        link = link[:-1]
    if link[-7:] == '-master':
        link = link[:-7]

    print('https://api.github.com/repos{}'.format(link))
    r = requests.get('https://api.github.com/repos{}'.format(link),
                     headers={'Content-Type': 'application/json',
                              'Authorization': 'token {}'.format(token)})
    data = r.json()
    return data['created_at'], data['size'], data['stargazers_count'],\
        data['language'], data['forks_count'], data['open_issues_count'],\
        data['subscribers_count']


def calculate_folder(params):
    folder = params['folder']
    token = params['token']
    print(folder)
    try:
        data = calculate(folder, params['index'])
        if data['commits'] == 0:
            return {'folder': ' ', 'value': 0, 'mu': 0}
        else:
            print('Commits: ', data['commits'])
    except Exception:
        with open('files_out3.txt', 'a+') as the_file:
            the_file.write(folder + '\n')
            return {'folder': folder, 'value': 0, 'mu': 0}
    vals = list(data['files'].values())
    if len(vals) < 2:
        return {'folder': folder, 'value': -111, 'mu': 0}
    vals.sort(reverse=True)
    calcmax = max(vals)
    cnt = len(vals)
    X = []
    p = []
    sum1 = 0
    sum2 = 0
    mean = statistics.mean([x for x in vals])
    for i in range(cnt):
        p.append(vals[i])
        X.append(i/cnt)
        sum1 = sum1 + i/cnt * vals[i]/calcmax
        sum2 = sum2 + vals[i]/calcmax
    for i in range(cnt):
        sum1 = sum1 + (X[i] - mean) * (X[i] - mean) * p[i]

    import re
    if folder[-1] == '/':
        folder = folder[:-1]
    arr = [m.start() for m in re.finditer('/', folder)]
    print('Index: ', params['index'])
    mu = statistics.stdev(vals)/mean
    try:
        created_at, size, stars, language, forks, \
          open_issues, subscribers = get_repo_detail(folder[arr[-2]:], token)
    except Exception:
        return {'folder': folder, 'mean': mean, 'mu': mu}
    return {'folder': folder, 'mean': mean, 'mu': mu,
            'created': created_at, 'size': size, 'stars': stars,
            'forks': forks,
            'issues': open_issues, 'subscribers': subscribers,
            'language': language}


def run_application():
    dirs = []
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--path', type=str, required=False, default='')
    parser.add_argument('--recursive', type=str, required=False,
                        default='False')
    parser.add_argument('--token', type=str, required=False, default='')
    args = parser.parse_args()
    token = args.token
    folder = args.path
    recursive = args.recursive
    if recursive == 'True':
        recursive = True
    else:
        recursive = False

    if len(folder) <= 0:
        print('Missing --path parameter')
        return -1

    if recursive:
        for f in os.scandir(folder):
            if f.is_dir:
                found = False
                for d in os.scandir(f.path):
                    if d.is_dir:
                        dirs.append(d.path)
                        found = True
                if not found:
                    shutil.rmtree(f.path)
    else:
        dirs = [folder]
    dirs.sort()
    pool = Pool(17)
    data = [{'folder': x, 'index': i, 'token': token}
            for i, x in enumerate(dirs)]
    results = pool.map(calculate_folder, data)

    pool.close()
    pool.join()
    return results


if __name__ == "__main__":
    dt = datetime.utcnow()
    res = run_application()
    with open('output.json', 'w') as outfile:
        json.dump(res, outfile)
    print('Started: ', dt, '   Finished: ', datetime.utcnow())
