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


class dictionary(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value


#https://www.geeksforgeeks.org/print-colors-python-terminal/
def printred(prt): print("\033[91m {}\033[00m" .format(prt))
def printgreen(prt): print("\033[92m {}\033[00m" .format(prt))
def printyellow(prt): print("\033[93m {}\033[00m" .format(prt))
def printlightpurple(prt): print("\033[94m {}\033[00m" .format(prt))
def printpurple(prt): print("\033[95m {}\033[00m" .format(prt))
def printcyan(prt): print("\033[96m {}\033[00m" .format(prt))
def printlightgray(prt): print("\033[97m {}\033[00m" .format(prt))
def printblack(prt): print("\033[98m {}\033[00m" .format(prt))
def printorange(prt): print("\033[43m {}\033[00m" .format(prt))
def printbold(prt): print("\033[01m {}\033[00m" .format(prt))
