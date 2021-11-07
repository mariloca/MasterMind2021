import loop
import helper

def defaultsetting():
	digit=4
	lower=0
	upper=7
	attempt=10
	return (digit, lower, upper, attempt)

player=input("----------Welcome to MasterMind Game-----------\nWhat's your name?")

print("Hi,", player, "! Below is the Main Menu:")
instru='''-------------------Main Menu-------------------
In this Mastermind game, you are playing against the computer.
You must guess the right number combinations within 10 attempts to win the game.
Game default setting: 10 attempts to guess a four number combinations from 0~7.
You can always change the difficulty of the game by yourself!
------------------------------------------------
Here are the options you can do during the game:
1.Start a new game ---Enter: "s"
2.Change the game difficulty ---Enter:"c"
3.Reset the game to default setting ---Enter:"r"
4.View your game score ---Enter: "v"
5.Exit the game ---Enter: "e"
6.See the menu ---Enter: "m"
------------------------------------------------
	'''
helper.printbold(instru)
digit,lower,upper,attempt=defaultsetting()
score_list=[]
while True:
	option=input("What would you like to do? Enter:")

	if option=='s': #start a new game
		#start guessloop here
		score=loop.guessloop(digit,lower,upper,attempt)
		if score>0:
			helper.printgreen("Bingo! You got it!")
		elif score==0:
			helper.printred("You have reached the guess limits.")
		score_list.append(score)
	elif option=="c": #change difficulty
		digit=int(input("Enter the number digits: "))
		lower=int(input("Enter the number the random number generator starts: "))
		upper=int(input("Enter the number the random number generator ends: "))
		attempt=int(input("Enter guess times: "))
	elif option=='r': #reset game
		digit,lower,upper,attempt=defaultsetting()
	elif option=='v': #show scoreboard, keep the past scores
		s=player + ", your scores are:" + str(score_list)
		helper.printpurple(s)
	elif option=='e':	#exit the game
		s="See you next time," + player + "!"
		helper.printpurple(s)
		break
	elif option=='m':
		helper.printbold(instru)
	else:
		helper.printred("Invalid input. Please enter again!")
