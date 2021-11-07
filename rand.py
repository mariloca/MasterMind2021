import urllib.request, urllib.error, urllib.parse


def randomnumbergenerate(num, min, max):
    """Returns a randomly ordered list of the integers between min and max"""
    if checkquota() < 1:
        raise Exception("Your www.random.org quota has already run out.")
    requestparam = buildrequestparameterNR(num, min, max)
    request = urllib.request.Request(requestparam)
    request.add_header('User-Agent', 'randomwrapy/0.1 very alpha')
    opener = urllib.request.build_opener()
    numlist = opener.open(request).read()
    #decode the byte to unicode
    newlist=numlist.decode()
    return newlist.split()
    

#helper
def buildrequestparameterNR(num, min, max):
    randomorg = 'https://www.random.org/integers/?num='
    vanilla = '&col=1&base=10&format=plain&rnd=new'
    params = str(num) + '&min=' + str(min) + '&max=' + str(max)
    return randomorg + params + vanilla


def checkquota():
    request = urllib.request.Request("https://www.random.org/quota/?format=plain")
    request.add_header('User-Agent', 'randomwrapy/0.1 very alpha')
    opener = urllib.request.build_opener()
    quota = opener.open(request).read()
    return int(quota)

def reportquota():
    request = urllib.request.Request("https://www.random.org/quota/?format=plain")
    request.add_header('User-Agent', 'randomwrapy/0.1 very alpha')
    opener = urllib.request.build_opener()
    quota = opener.open(request).read()
    print("This IP address has", quota, "bits left. Visit http://www.random.org/quota for more information.")    
    
    
