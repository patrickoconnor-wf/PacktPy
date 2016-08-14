#!/usr/bin/env python

import json
import os
import sys
import traceback

import requests
from bs4 import BeautifulSoup

url = 'https://www.packtpub.com/packt/offers/free-learning'


def getLoginDetails():
    email = os.getenv('PACKT_EMAIL', None)
    password = os.getenv('PACKT_PASSWORD', None)
    if not (email and password):
        raise Exception('Either the email or the password doesn\'t exist.')
    return {
        'email': email,
        'password': password,
        'op': 'Login',
        'form_id': 'packt_user_login_form',
        'form_build_id': ''
    }


def getHeaders():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 ' +
        '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }


def main():
    book_link = None
    headers = getHeaders()
    login_details = getLoginDetails()
    session = requests.Session()
    res = session.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    form = soup.find('form', id='packt-user-login-form')
    if form is None:
        print "Could not find login form"
        exit(1)
    login_details['form_build_id'] = form.find('input', attrs={'name': 'form_build_id'}).get("value")

    # session.headers.update({'content-type': 'application/x-www-form-urlencoded'})
    res = session.post(url, headers=headers, data=login_details)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        book_link = soup.select('.twelve-days-claim')[0].get('href')
        if book_link is None:
            raise Exception('Could not find claim button')
    except Exception:
        traceback.print_exc()
        exit(1)
    # print book_link

    res = session.get('https://packtpub.com' + book_link)
    soup = BeautifulSoup(res.text, "html.parser")
    print 'https://packtpub.com' + book_link

if __name__ == '__main__':
    main()
