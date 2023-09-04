import re
import time
import requests
import bs4


def get_tieba_link():
    url='https://tieba.baidu.com/f/like/mylike?&pn='
    page=1
    links=[]
    while True:
        try:
            r=requests.get(url+str(page),headers=Header)
            r.raise_for_status()
            soup=bs4.BeautifulSoup(r.text,'lxml')
            for i in soup.select('table tr>td:first-child>a'):
                links.append({'href': 'https://tieba.baidu.com/'+i.get('href'), 'name': i.string})
            page+=1
            if '下一页' not in str(soup):
                break
        except requests.exceptions.RequestException as e:
            print(e)
            break
    return links


def tieba_qiandao():
    links=get_tieba_link()
    for link in links:
        r=requests.get(link['href'],headers=Header)
        tbs=re.compile(r"'tbs': \"(.*?)\"").search(r.text).group(1)
        if not tbs:
            print(f"获取{link['name']}吧tbs失败")
            continue
        param={'ie':'utf-8','kw':link['name'],'tbs':tbs}
        r=requests.post('https://tieba.baidu.com/sign/add',data=param,headers=Header)
        if r.json()['no']==0:
            print(f"{link['name']}吧签到成功")
        else:
            print(f"{link['name']}吧签到失败，原因：{r.json()['error']}")
        time.sleep(1)


if __name__ == '__main__':
    Header = {
            'cookie': '',
        }
    tieba_qiandao()