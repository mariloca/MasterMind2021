import helper
import collections

def guessloop(num,lower,upper,attempt):
	#Data preparation
	secret=helper.randomnumbergenerate(num,lower,upper) #Generate random number in a list
	#print(secret)
	#answerdict=convertlisttodict(secret)
	answerdict=list(secret)
	repeatdict=collections.Counter(secret)
	score=100
	deductpoint=int(score/attempt) #score of each attempt
	print("*****************************************\nAre you ready? Let's get started!")
	hint=input("Do you want to see the Hint? Please enter Y or N: ")

	while True:
		guess=input("Please enter your guess: ")

		try: #Try-except step to catch input error
			guessint=int(guess) #Check if 'guess' is a valid number input
			guesslist=[]
			for i in str(guess):
				guesslist.append(i)
			#guessdict=convertlisttodict(guesslist)
			#guessdict=guesslist
			#Create a copy of the 'repeatdict' dictionary
			repeatdictcopy=dict()
			for key,value in repeatdict.items():
				repeatdictcopy.add(key,value)

			#Compare the guessdict and answerdict
			compareresult=compareloop(num, guessint, answerdict, guesslist, repeatdictcopy)
			print('tag')
			if compareresult==1:
				break
			else:
				if hint=="Y": showhint(secret, guessint)
				attempt=attempt-1
				score=int(score-deductpoint)
				print("You have", attempt, "guesses left.\n===================================")
				if attempt==0: break #game over
		except:
			helper.printred("Invalid input. Please enter a number.")

	return score


'''
def convertlisttodict(numlist):
	i=0
	numdict = dict()
	for number in numlist:
		#numdict.key=i
		#numdict.value=number
		numdict[i]=number
		#numdict.add(numdict.key, numdict.value)
		i=i+1
	return numdict


def repeattimedict(numlist): #stores number as keys, number repeat times as values
	i=0
	repeatdict = dict()
	for number in numlist:
		#repeatdict.key=numlist[i]
		#repeatdict.value=numlist.count(numlist[i])
		#repeatdict.add(repeatdict.key, repeatdict.value)
		repeatdict[numlist[i]]=numlist.count(numlist[i])
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
		returnresult=1
	else:
		print("Guess number:", guessint, "Correct number:", almost, "Correct position:", bingo)
	return returnresult


def showhint(answerlist, guessnumber): #convert answerlist to integer
	answerlist = int("".join(answerlist))
	if guessnumber>answerlist:
		print("Hint: Your guess is bigger than the answer.")
	elif guessnumber<answerlist:
		print("Hint: Your guess is smaller than the answer.")

#ss=guessloop(4,0,7,10)
#print(ss)
