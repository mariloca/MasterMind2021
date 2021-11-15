import rand
from helpers import dictionary
import collections

def defaultsetting():
	digit=4
	lower=0
	upper=7
	attempt=10
	return (digit, lower, upper, attempt)


def guessloop(secret,guess,score):
	'''Need to know current attempt'''
	answerdict=convertlisttodict(secret)
	#repeatdict=repeattimedict(secret)
	repeatdict=collections.Counter(secret)
	while True:
		#Try-except step to catch input error
		guessint=int(guess) #Check if 'guess' is a valid number input
		guesslist=[]
		for i in str(guess):
			guesslist.append(i)
		guessdict=convertlisttodict(guesslist)
		#Create a copy of the 'repeatdict' dictionary
		#repeatdictcopy=dictionary()
		repeatdictcopy=dict()
		for key,value in repeatdict.items():
			repeatdictcopy[key]=value
			#repeatdictcopy.add(key,value)

		#Compare the guessdict and answerdict
		compareresult=compareloop(4, guessint, answerdict, guessdict, repeatdictcopy)

		if compareresult[0]==1:
			break
		else:
			score-=10
			break
	return score, compareresult



def convertlisttodict(numlist):
	#i=0
	#numdict = dictionary()
	numdict = dict()
	'''
	for number in numlist:
		numdict.key=i
		numdict.value=number
		#numdict.add(numdict.key, numdict.value)
		i=i+1
	'''
	for i in range(0,len(numlist)):
		numdict[i]=numlist[i]
	return numdict

'''
# use collections.Counter
def repeattimedict(numlist): #stores number as keys, number repeat times as values
	#i=0
	#repeatdict = dictionary()
	repeatdict = dict()

	for number in numlist:
		repeatdict.key=numlist[i]
		repeatdict.value=numlist.count(numlist[i])
		repeatdict.add(repeatdict.key, repeatdict.value)
		i=i+1
	return repeatdict
'''

def compareloop(num, guessint, answerdict, guessdict, repeatdictcopy):
	idx=0
	bingo=0  #correct position
	almost=0 #correct number
	wrong=0 #wrong guess
	returnresult=0
	for idx in range(0,num):
		#Check if the guess number has any digits at the correct position
		if guessdict[idx]==answerdict[idx]:
			bingo=bingo+1
		#Check if the guess number has any correct digits
		if guessdict[idx] in repeatdictcopy.keys():
			if repeatdictcopy[guessdict[idx]]>0:
				almost=almost+1
				repeatdictcopy[guessdict[idx]]=repeatdictcopy[guessdict[idx]]-1
		else:
			wrong=wrong+1
	if bingo==num:
		returnresult=1 #bingo
	else:# wrong guess
		print("Guess number:", guessint, "Correct number:", almost, "Correct position:", bingo)

	return returnresult, almost, bingo
