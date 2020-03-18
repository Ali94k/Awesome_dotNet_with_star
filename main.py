import re
import requests
import json
from requests.auth import HTTPBasicAuth

with open('README.md') as f:
    lines = f.readlines()

i = 1

with open('withStart.md', 'w') as f:
    f.writelines('|repo|star Count|\n')
    f.writelines('|---|---|\n')

    for line in lines:
        if line.startswith('* ['):
            s = line.index('](')
            e = line.index(')', s)
            url = line[s+2:e]
            if url.startswith('https://github.com/') or url.startswith('http://github.com/'):
                try:
                    i = i+1
                    if i == 10:
                        break
                    os = url.index('//github.com/')+len('//github.com/')
                    oe = url.index('/', os)
                    owner = url[os:oe]
                    proj = url[oe+1:]
                    repo ='https://api.github.com/repos/'+owner+'/'+proj
                    print('https://api.github.com/repos/'+owner+'/'+proj)
                    r = requests.get(
                        'https://api.github.com/repos/'+owner+'/'+proj, auth=HTTPBasicAuth('', ''))
                    if(r.ok):
                        repoItem = json.loads(r.text or r.content)
                        print("created: " + repoItem["created_at"])
                        print("stargazers count " + str(repoItem["stargazers_count"]))
                        f.writelines('|' + repo + '|'+str(repoItem["stargazers_count"])+'|\n')
                    else:
                        print('not ok')
                    print(i, end=' ')
                    print(url)

                except Exception as ex:
                    print(ex)
                    print('     error ' +url)
        elif line.startswith('#'):
            print(line)
            f.writelines(line+'\n')
            f.writelines('|repo|star Count|\n')
            f.writelines('|---|---|\n')
