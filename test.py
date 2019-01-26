import urllib.request
try:
    contents = urllib.request.urlopen('http://localhost:3000/')
    print(contents.read().decode())
except:
    print('Nope')
