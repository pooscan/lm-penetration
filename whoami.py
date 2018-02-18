from supermo.core.whoami import whoami
url = "http://you.163.com"
res = whoami(url)
res.run()
cms = list(res.cms_list)
print(cms)