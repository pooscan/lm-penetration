# coding=utf-8
import hashlib,sys
from urllib.parse import urlparse

def md5_url(url):
    a = str(url).encode('utf-8')
    return hashlib.md5(a).hexdigest()[8:-8]

# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except Exception as e:
        return e
# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

