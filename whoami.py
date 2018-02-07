from supermo.core.whoami import whoami
url = "https://www.5djbb.com"
res = whoami(url)
res.run()
cms = list(res.cms_list)
print(cms)