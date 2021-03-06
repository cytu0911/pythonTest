__author__ = 'cytu'
import sys
reload(__import__('sys')).setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import re

url = 'http://www.zhihu.com'
loginURL = 'http://www.zhihu.com/login/email'
messageURL = 'http://www.zhihu.com/inbox/post'

headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36',
    "Referer": "http://www.zhihu.com/",
    'Host': 'www.zhihu.com',
}

login_data = {
    'email': 'tuchengyu404@gmail.com',        # your email
    'password': 'tcy3841276',     # your password
    'remember_me': "true",
}

message_data = {
    'content': 'hello'
}

session = requests.session()


def create_cookies():
    if os.path.exists('cookiefile'):
        with open('cookiefile') as f:
            cookie = json.load(f)
        session.cookies.update(cookie)
        req1 = session.get(url, headers=headers)
        #
        #with open('zhihu.html', 'w') as f:
         #   f.write(req1.content)
    else:
        req = session.get(url, headers=headers)
        # print req.text

        soup = BeautifulSoup(req.text, "html.parser")
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')

        login_data['_xsrf'] = xsrf

        timestamp = int(time.time() * 1000)
        captchaURL = 'http://www.zhihu.com/captcha.gif?=' + str(timestamp)
        print captchaURL

        with open('zhihucaptcha.gif', 'wb') as f:
            captchaREQ = session.get(captchaURL)
            f.write(captchaREQ.content)
        loginCaptcha = raw_input('input captcha:\n').strip()
        login_data['captcha'] = loginCaptcha
        # print data
        loginREQ = session.post(loginURL,  headers=headers, data=login_data)  # post return json
        print loginREQ.content

        with open('cookiefile', 'wb') as f:
            json.dump(session.cookies.get_dict(), f)


def post_message(urls):
    for i in urls:
        profile_page = session.get(i, headers=headers)
        with open('temp.html', 'wb') as f:
            f.write(profile_page.content)
        soup = BeautifulSoup(profile_page.text, "html.parser")
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
        member_id = soup.find('button', {'data-follow': 'm:button'}).get('data-id')
        message_data['_xsrf'] = xsrf
        message_data['member_id'] = member_id
        response = session.post(messageURL, headers=headers, data=message_data)
        print response

def get_follers(user_url):
    #follower_page = session.get(url, headers=headers)
    #soup = BeautifulSoup(follower_page.content, 'html.parser')
    #userNode = soup.findAll('a', {'class': 'zu-top-nav-userinfo'})
    #urlName = url 
    #for x in userNode:
     #   urlName = urlName + x['href']
      #  print urlName

    user_page = session.get(user_url+ '/followees', headers=headers)
    soup_user = BeautifulSoup(user_page.content, 'html.parser')
    #with open('zhihu.html', 'w') as f:
          #  f.write(user_page.content)
    followees = soup_user.findAll('div', {'class':'zm-list-content-medium'})

    urllist = []
    for followee in followees:
        #print followee.h2.a['href']
        urllist.append( followee.h2.a['href'] )
    #print followees    
    #print user_page.content

    
def get_allfollers(user_url):
    follower_page = session.get(user_url, headers=headers)
    soup = BeautifulSoup(follower_page.content, 'html.parser')
    followers = soup.findAll('a', {'class': 'zm-item-link-avatar'})
    followers_num = int(soup.find("div", {'class': 'zm-profile-side-following zg-clear'}).find_all("a")[1].strong.string)
    # print followers_num
    follerows_list = []  # store all followers' url
    cnt = 0
    for i in xrange((followers_num - 1) / 20 + 1):
        cnt += 1
        if cnt > 5:
            break
        if i is 0:
            user_list = soup.find_all("h2", {'class': 'zm-list-content-title'})
            for tmp in user_list:
                follerows_list.append(tmp.a['href'])
        else:
            post_url = 'http://www.zhihu.com/node/ProfileFolloweesListV2'
            _xsrf = soup.find('input', {'name': '_xsrf'})['value']
            offset = i * 20
            hash_id = re.findall('hash_id&quot;: &quot;(.*)&quot;},', follower_page.content)[0]
            # print hash_id
            # print _xsrf
            params = json.dumps({'offset': offset, 'order_by': 'created', 'hash_id': hash_id})
            follower_data = {
                '_xsrf': _xsrf,
                'method': 'next',
                'params': params
            }
            r_post = session.post(post_url, data=follower_data, headers=headers)
            # print r_post.text
            followee_list = r_post.json()['msg']
            for j in xrange(min(followers_num - i * 20, 20)):
                followee_soup = BeautifulSoup(followee_list[j])
                user_link = followee_soup.find('h2', class_='zm-list-content-title').a['href']
                follerows_list.append(user_link)
    for i in follerows_list:
        print i
    return follerows_list

if __name__ == '__main__':
    # print '23333'
    create_cookies()
    #urls = get_allfollers('http://www.zhihu.com/people/tu-cheng-yu')
    follers = get_follers('http://www.zhihu.com/people/tu-cheng-yu')
    print follers
    #post_message(urls)
