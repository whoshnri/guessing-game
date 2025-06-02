#### guessing game 
import random
import time
import sys
import pandas as pd


def verify(number, guess):
    #verifies the input and outputs booleans
    print("verifying.....")
    time.sleep(1)
    if number == guess:
        return True
    else: 
        return False

class Computer():
    def __init__(self):
        df = pd.DataFrame(columns=["number","picksNo","guessesNo",'prPicks','prGuess'])
        df.to_csv("dataset/guessing_game.csv" , index=False)
    
        data = pd.read_csv('dataset/guessing_game.csv')
    
        data["number"] = ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine']
        data["picksNo"] = [0 for x in range(9)]
        data["guessesNo"] = [0 for x in range(9)]
        total_row = {
            'number': 'Total',
            'picksNo': data['picksNo'].sum(),
            'guessesNo': data['guessesNo'].sum(),  # Or use a different logic like average or total cost
            'prPicks': '',
            'prGuess': ''
            }
        data = pd.concat([data, pd.DataFrame([total_row])], ignore_index=True)
        self.data = data
        # data.to_csv("dataset/guessing_game.csv" , index=False)

        self.pr_picks_list = []
        self.pr_guess_list = []

    #now the stage for the real analysis
    def pr(self, num, total):
        return round((num / total if (total > 0) and (num > 0) else 0),2)
        
    def calibrate(self):  
        total_picks = self.data.loc[self.data['number'] == 'Total', 'picksNo'].values[0]
        total_guesses = self.data.loc[self.data['number'] == 'Total', 'guessesNo'].values[0]
    
        for x in self.data.index[:-1]:
            self.data.at[x, 'prPicks'] = self.pr(self.data.at[x, 'picksNo'], total_picks)
            self.data.at[x, 'prGuess'] = self.pr(self.data.at[x, 'guessesNo'], total_guesses)
    
    #increments the data
    def picksNoIncrement(self, str_):
        self.data.loc[self.data['number'] == str_, "picksNo"] += 1
        self.data.loc[self.data['number'] == 'Total', 'picksNo'] = self.data['picksNo'][:-1].sum()  # update total
        self.calibrate()
        # data.to_csv("dataset/guessing_game.csv", index=False)
    
    def guessesNoIncrement(self, str_):
        self.data.loc[self.data['number'] == str_, "guessesNo"] += 1
        self.data.loc[self.data['number'] == 'Total', 'guessesNo'] = self.data['guessesNo'][:-1].sum()  # update total
        self.calibrate()
        # data.to_csv("dataset/guessing_game.csv", index=False)

    def showDataFrame(self):
        self.calibrate()
        self.updatePrLists()
        print(self.data)

    def checkMostProbableGuess(self):
        n = ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine']
        descending_list = [float(item) if item != '' else 0.0 for item in self.data['prGuess']]
        combined_dict = dict(zip(n, descending_list))
        return(combined_dict)
        

    def checkMostProbablePick(self):
        n = ['One','Two','Three','Four','Five','Six','Seven','Eight','Nine']
        descending_list = [float(item) if item != '' else 0.0 for item in self.data['prPicks']] 
        combined_dict = dict(zip(n, descending_list))
        return(combined_dict)

    def updatePrLists(self):
            pr_picks_dict = self.checkMostProbablePick()
            pr_guess_dict = self.checkMostProbableGuess()

            self.pr_picks_list = [[item,values] for item,values in pr_picks_dict.items()]
            self.pr_guess_list = [[item,values] for item,values in pr_guess_dict.items()]
            
            # self.pr_picks_list.sort(key=lambda x: x[1], reverse=False)
            # self.pr_guess_list.sort(key=lambda x: x[1], reverse=False)

    def gen(self, which):
        base = ['1','2','3','4','5','6','7','8','9']

        empty = [['One', 0.0], ['Two', 0.0], ['Three', 0.0], ['Four', 0.0], ['Five', 0.0], ['Six', 0.0], ['Seven', 0.0], ['Eight', 0.0], ['Nine', 0.0]]

        if which == 'picks':
            if self.pr_guess_list == empty:
                return random.choice(base)
            else:
                weighted = []
                for x in self.pr_guess_list:
                    num = getIndexing(x[0])
                    weighted.extend([num] * (10 - (round(x[1] * 10))))
                return random.choice(weighted)
        else:
            if self.pr_picks_list == empty:
                return random.choice(base)
            else:
                weighted = []
                for x in self.pr_picks_list:
                    num = getIndexing(x[0])
                    weighted.extend([num] * (2 + (round(x[1] * 10))))
                return random.choice(weighted)

            
def getIndexing(num):
    #this function uhm, turns a string (One - Nine)into a number 
    dict_pilot = {
        'One' : '1',
        'Two' : '2',
        'Three' : '3',
        'Four' : '4',
        'Five' : '5',
        'Six' : '6',
        'Seven' : '7',
        'Eight' : '8',
        'Nine' : '9'
    }
    for item, value in dict_pilot.items():
        if item == num:
            return value
        


def delay(num):
    #this is the delay for the computer when it is guessing an input
    print("Guessing........")
    time.sleep(num)

def delay2(num):
    #this is the delay for the computer when generating a number
    print("Generating........")
    time.sleep(num)
    print("Generated!")

def game_start_delay():
    #this delays the start with a countdown
    print("Game starts in....3")
    time.sleep(1)
    sys.stdout.write("\033[F\033[K")
    print("Game starts in....2")
    time.sleep(1)  
    sys.stdout.write("\033[F\033[K")
    print("Game starts in....1")
    time.sleep(1)
    
def game_user():
    win = False
    count = 5 #number of tries
    #generates the number for the round
    number = gen()
    #a little delay for some interactivity
    delay2(4)
    # incase input is not a number
    guess = input("\nGuess a number from 1-9 : ")
    while guess not in ['1','2','3','4','5','6','7','8','9']:
        print("That is not a number!")
        guess = input("\nGuess a number from 1-9 : ")      
    #check
    win = verify(number , guess)
    #loop to verify the inputs over and over, print loss reports and end the round after 5 tries
    while win == False:
        count -= 1
        comp.guessesNoIncrement(int(getIndexing(number)))
        if count > 1:
            print(f"Naaaaah! {random.choice(["Wrong guess\n","Thats not it"])}.....You have {count} guesses left")
            #error proofing the input, again
            guess = input("\nGuess a number from 1-9 : ")
            while guess not in ['1','2','3','4','5','6','7','8','9']:
                print("That is not a number!")
                guess = input("\nGuess a number from 1-9 : ")
            win = verify(number , guess) 
        elif count == 1:
            print(f"Naaah! Thats not it!\nYou have {count} guess left")
            #final error proofing
            guess = input("\nGuess a number from 1-9 : ")
            while guess not in ['1','2','3','4','5','6','7','8','9']:
                print("That is not a number!")
                guess = input("\nGuess a number from 1-9 : ")
            win = verify(number , guess)
        else: 
            print("You are out of Guesses\nRound lost!")
            return -1

    #if correct
    print("Correct Guess")
    return 1


def game_comp():
    win = False
    count = 5 #trials for comp
    number = input("\nEnter a number from 1-9 for the Computer to guess: ")
    #verify input is within the guessing treshold
    if number in ["1","2",'3','4','5','6','7','8','9']:
        guess = comp.gen()
        #fun delay
        delay(3)
        print(f"Guess ---- {guess}")
        win = verify(number , guess)
        #guessing loop till trials are over or till correct input is recieved
        while win == False:
            count -= 1
            if count > 1:
                guess = comp.gen()
                print(f"Computer has {count} guesses left\n")
                delay(3)
                print(f"Guess ---- {guess}")
                win = verify(number , guess)
            elif count == 1:
                guess = comp.gen()
                print(f"Computer has {count} guess left\n")
                delay(3)
                print(f"Guess ---- {guess}")
                win = verify(number , guess)
            else: 
                print("Computer is out of guesses\nRound lost!")
                return -1
        print("Computer got it right!")
        comp.picksNoIncrement(int(getIndexing(number)))
        return 1
    else:
        #recursion block incase number recieved is outside the guessing treshold
        print("Input is out of range!\nLets try that again, shall we?")
        game_comp()

def game():
    #name field for player
    username = input("What is your name: ")
    rules = """
    ##### Rules and Pre-notes ####
    1. Guesses outside the range count as a loss
    2. The computer guesses are not aided
    3. This was made by Henry as an assignment
    4. Enjoy :)
    """
    #print the rules before the game starts
    print(rules)
    #game start delay lol
    game_start_delay()
    #this variable makes then  game start sorta
    replay = True
    #initial scores
    user = 0
    comp = 0
    #loop statemets with gameplay conditions
    while user not in [3,-3 ] and comp not in [3,-3 ] and replay == True:
        a = game_user()
        user += a
        print(f"{username} - [{user}] : [{comp}] - Computer")
        b = game_comp()
        comp += b
        print(f"{username} - [{user}] : [{comp}] - Computer")
        replay = input(f"Another Round, {username}?[y/n]: ")
        if replay.lower() in ["y",'yes'] and user not in [3,-3 ] and comp not in [3,-3 ] :
            replay = True
        else:
            replay = False
            print("\nYou opted out!\n")
    #On opt-out or game end, this is printed to display final scores
    print(f"{"#"*10}Final Scores{"#"*10}")
    print(f"{username} - [{user}] : [{comp}] - Computer")
    print("Game Over!")





