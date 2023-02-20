import time,random,sqlite3

conn = sqlite3.connect('scores.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('CREATE TABLE IF NOT EXISTS scores (username TEXT, score INTEGER)')

difficulty,players,hints,category,username=[0,0,0,0,0]

# all the words that will pop up for hangman
words = {
    'Animals': {
        'Easy': ['zebra', 'tiger', 'snake', 'shark', 'whale', 'otter', 'panda', 'koala', 'chimp', 'puppy', 'eagle', 'hippo', 'raven', 'stork', 'hyena', 'skunk', 'rhino', 'goose'],
        'Medium': ['panther', 'gazelle', 'penguin', 'buffalo', 'giraffe', 'elephant', 'octopus', 'chicken', 'jaguar', 'hamster', 'seagull', 'sparrow', 'badgers', 'kangaro',  'platypu', 'lobster', 'wallaby'],
        'Hard': ['crocodile', 'porcupine', 'rhinoceros', 'alligator', 'kangaroos', 'jellyfish', 'chameleons', 'hummingbird', 'butterfly', 'orangutans', 'dolphinews', 'porpoises', 'hippopotam', 'woodpecker', 'platypuses', 'cheetahs', 'anteaters', 'squirrels', 'flamingoes', 'chinchilla']
    },
    'Countries': {
        'Easy': ['japan', 'china', 'india', 'spain', 'italy', 'chile', 'kenya', 'egypt', 'nepal','sudan', 'nepal', 'yemen',  'libya', 'malta'],
        'Medium': ['belgium', 'morocco', 'ireland', 'germany', 'colombi', 'bahrain', 'pakistan', 'romania', 'mongolia', 'nigeria', 'denmark', 'haiti', 'oman', 'brazil', 'namibia', 'jamaica', 'thailand', 'india', 'kazakhs', 'mongoli'],
        'Hard':  ['zimbabwean', 'azerbaijan', 'czechoslov', 'bangladesh', 'guadeloupe', 'macedonian', 'mauritania', 'afghanista', 'micronesia', 'montserrat', 'vietnamese', 'azerbaijan', 'argentinia', 'kyrgyzstan']
    },
    'Fruits': {
        'Easy': ['grape', 'apple', 'mango', 'peach', 'melon', 'lemon', 'berry','olive', 'pears', 'grape', 'avoca', 'pears', 'dates', 'guava', 'pawpaw', 'prune'],
        'Medium': ['mangoes', 'apricot', 'avocado', 'coconut', 'kiwifruit', 'mangost', 'papayas', 'peaches', 'plumcot', 'soursop', 'bananas'],
        'Hard': ['blackberry', 'pomegranat', 'honeycrisp',  'persimmons', 'bloodorang', 'tamarillos', 'boysenberr', 'ackeefruit', 'watermelon', 'kiwiberrie',  'cantaloupe', 'clementine',  'guavafruit']}}


def hint(gussedletters,Secretword):
    # finds a letter thats part of the secret word and shows it
    valid_letters = [letter for letter in Secretword if letter not in gussedletters]
    gussed_letter=random.choice(valid_letters)
    print(f"Hint {gussed_letter} has been added!")
    gussedletters.append(gussed_letter)
    return gussed_letter

def play(difficulty,hints,category):
    global list,username
    # number of lives 
    Lives=6
    gussedletters=[]
    # number of hints per difficulty
    guesses={"Easy":3, "Medium":2, "Hard":1}
    if category ==0:
        category= random.choice(["Animals","Countries","Fruits"])
        print(f"No category selected. Choosing {category} instead.")
    if difficulty==0:
        difficulty=random.choice(["Easy","Medium","Hard"])
        print(f"No difficulty selected. Choosing {difficulty} instead.")
    word = words[category][difficulty]
    Secretword=random.choice(word).lower()
    length=len(Secretword)
    blanks=length*"_"
    # incase a costume hint is chosen in the main menue 
    if hints==0:
        guesses=guesses[difficulty]
    else:
        guesses=hints
    print("The Game has begun!")
    print("\nDuring any point of the game, you may type 'hint' in order to use any of your remaining hints!\n")
    print("During any point of the game, you may type the word!\n")
    print(f"You've got {guesses} hints!\n")
    print(f"the word has {length} letters!")
    
    # runs till the word is found or the player runs out of lives
    while Lives>=1:
        if blanks==Secretword:
            print(f"You got it right with {Lives} lives remaning!")
            time.sleep(3)
            # Score calculation
            score=Lives*100+hints*100
            if difficulty=="Hard":
                score+=1000
            elif difficulty=="Medium":
                score+=500
            print(f"{username} has completed {difficulty} difficulty having {guesses} hints available and having {Lives} lives remaining.\nOverall score: {score} points!")
            # Adds it to the database
            c.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))
            conn.commit()
            main()
        # prints the blanks including the found letters
        print(blanks)
        try:
            letterguess=str(input("\nGuess a letter:")).lower()
            # if there are hints avalible and the player would like to use them
            if letterguess=="hint" and guesses>0:
                guessedletter=hint(gussedletters,Secretword)
                positions = [i for i, letter in enumerate(Secretword) if letter in guessedletter]
                for i in positions:
                    blanks = blanks[:i] + guessedletter + blanks[i+1:]
                guesses-=1
                continue
            # if there are no hints available and the player would like to use them
            if letterguess=="hint" and guesses==0:
                print("\nyou've ran out of hints!:(")
                continue
            # incase the user guesses the word 
            if letterguess==Secretword:
                blanks=Secretword
                print("Congragulations! you've got it right!")
                continue
            # incorrect input
            elif len(letterguess)<1 or len(letterguess)>1:
                raise
            # repetition of guesses
            elif letterguess in gussedletters:
                print("you've already gussed this letter!")
                continue
        except:
            print("Thats not a valid input!")
            continue
        # guessed letter correctly
        if letterguess in Secretword:
            print(letterguess,"Is in the secret word!")
            positions = [i for i, letter in enumerate(Secretword) if letter in letterguess]
            for i in positions:
                blanks = blanks[:i] + letterguess + blanks[i+1:]
        else:
            print("thats not correct")
            Lives-=1
            print(f"You've got {Lives} Lives left!")
        gussedletters.append(letterguess)
    if Lives==0:
        print(f"The secret word was {Secretword}!!")
        
def difficulty_choice():
    # option to choose difficulty
    while True:
        print("========================================")
        print("|        Choose Difficulty Level       |")
        print("========================================")
        print("| 1. Easy (5 letter words, 6 guesses)  |")
        print("| 2. Medium (7 letter words, 4 guesses)|")
        print("| 3. Hard (10 letter words, 2 guesses) |")
        print("| 4. Back to Main Menu                 |")
        print("========================================")
        playerschoice=input("Enter your choice: ")
        # makes sure the input is correct
        if playerschoice.isdigit() and int(playerschoice) in [1,2,3,4]:
            break
        else:
            print("Please pick a digit between 1-4!")
            time.sleep(2)
    playerschoice=int(playerschoice)
    if playerschoice==1:
        return("Easy")
    
    elif playerschoice==2:
        return("Medium")
    elif playerschoice==3:
        return("Hard")
    elif playerschoice==4:
        main()
        

def hint_choice():
    # option to choose hint difficulty level
    while True:
        print("==================================")
        print("|          Hint System           |")
        print("==================================")
        print("| 1. Easy (2 hints per game)     |")
        print("| 2. Medium (1 hint per game)    |")
        print("| 3. Hard (no hints)             |")
        print("| 4. Back to Main Menu           |")
        print("==================================")
        playerschoice=input("Enter your choice: ")
        # makes sure the input is correct
        if playerschoice.isdigit() and int(playerschoice) in [1,2,3,4]:
            break
        else:
            print("Please pick a digit between 1-4!")
            time.sleep(2)
    playerschoice=int(playerschoice)
    if playerschoice==1:
        return(2)
    elif playerschoice==2:
        return(1)
    elif playerschoice==3:
        return(0)
    elif playerschoice==4:
        main()

def categories_choice():
    # option to chosse what category of words
    while True:
        print("==================================")
        print("|         Word Categories        |")
        print("==================================")
        print("| 1. Animals                     |")
        print("| 2. Countries                   |")
        print("| 3. Fruits                      |")
        print("| 4. Back to Main Menu           |")
        print("==================================")
        playerschoice=input("Enter your choice: ")
        # makes sure the input is correct
        if playerschoice.isdigit() and int(playerschoice) in [1,2,3,4]:
            break
        else:
            print("Please pick a digit between 1-4!")
            time.sleep(2)
    playerschoice=int(playerschoice)
    if playerschoice==1:
        return("Animals")
    elif playerschoice==2:
        return("Countries")
    elif playerschoice==3:
        return("Fruits")
    elif playerschoice==4:
        main()


def scoreboard():
    # option to show or clear the score board
    while True:
        print("==================================")
        print("|      High Score Tracking       |")
        print("==================================")
        print("| 1. View High Scores            |")
        print("| 2. Clear High Scores           |")
        print("| 3. Back to Main Menu           |")
        print("==================================")
        playerschoice=input("Enter your choice: ")
        # makes sure the input is correct
        if playerschoice.isdigit() and int(playerschoice) in [1,2,3]:
            break
        else:
            print("Please pick a digit between 1-4!")
            time.sleep(2)
    playerschoice=int(playerschoice)
    if playerschoice==1:
        # Retrieve the scores from the database and display them
        c.execute('SELECT * FROM scores ORDER BY score DESC')
        sorted_items = c.fetchall()
        if sorted_items:
            print("Leaderboard:")
            for rank, (username, score) in enumerate(sorted_items, start=1):
                print(f"{rank}. {username}: {score}")
        else:
            print("no one has played yet!")
    elif playerschoice==2:
        # deletes the score board data
        c.execute('DELETE FROM scores')
        conn.commit()
        print("Leaderboard has been cleared!\n")
    elif playerschoice==3:
        main()

def main():
    # shows main menue and checks to see if the username is taken
    global difficulty,hints,category,username
    while True:
        username = input("Please enter your name: ")
        rand_num = str(random.randint(0, 9999)).zfill(4)
        username=(f"{username}#{rand_num}")
        c.execute('SELECT * FROM scores WHERE username=?', (username,))
        result = c.fetchone()
        if result is not None or username=='':
            print("Sorry, that username is unavailable. Please choose another.")
            username=0
            continue
        break
    
    print(f"Hello, {username}!")
    while True:
        print("==================================")
        print("|       Welcome to Hangman!      |")
        print("==================================")
        print("| 1. Play Game                  |")
        print("| 2. Choose Difficulty Level    |")
        print("| 3. Hint System                |")
        print("| 4. Word Categories            |")
        print("| 5. High Score Tracking        |")
        print("| 6. Exit                       |")
        print("==================================")
        # checks to see if input is correct
        try:
            playerschoice=int(input("Enter your choice: "))
            if playerschoice not in [1,2,3,4,5,6]:
                raise 
        except:
            print("Please pick a digit between 1-7!")
            time.sleep(2)
            continue
        if playerschoice==1:
            play(difficulty,hints,category)
        elif playerschoice==2:
            difficulty=difficulty_choice()
            print(f"\nDifficulty {difficulty} has been chosen!\n")
        elif playerschoice==3:
            hints=hint_choice()
            print(f"\n{hints} hints has been given!\n")
        elif playerschoice==4:
            category=categories_choice()
            print(f"\n{category} category has been chosen!\n")
        elif playerschoice==5:
            scoreboard()
        elif playerschoice==6:
            break
main()
conn.close()
