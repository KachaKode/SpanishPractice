import random

#  This program is intended to help the user practice spanish verb conjugations for different tenses and parts of speech

#  load up the word bank
f = open('data.txt', 'r',  encoding='utf-8')
dataContent = f.read()
firstOpenInd = dataContent.index("{")
dataContent = dataContent[firstOpenInd:]
data = eval(dataContent)

#create list of tenses
chosen_tenses = []

correct, trials = 0, 0


#function to filter out the practice pairs that are not relevant for the user's chosen tense
def filterPracticePairs():
    return [x for x in wordTensePairs2Practice if x['tense'] in chosen_tenses]

#function to, based on whether or not it's time to do a practice round, get
# the next challenge word and it's associated info
def getInfo(choice):
    # this is a regular round, choose challenge word at random
    if choice % 2 == 0 or len(filteredPractice) == 0:
        randWord = random.choice(words)
        randTense = random.choice(chosen_tenses)
        partsOfSpeech = list(data[randWord][randTense].keys())
        randPartOfSpeech = random.choice(partsOfSpeech)
        translation = data[randWord][randTense][randPartOfSpeech]["translation"]
        answer_raw = data[randWord][randTense][randPartOfSpeech]["conjugation"]
        answer = removeAccents(answer_raw.lower())
        reverse_chosen = reverse()
        return randWord, randTense, randPartOfSpeech,translation, answer, reverse_chosen
    else:
        #this is a practice round, choose challenge word from
        # collection of words that user previously had trouble with
        practice = random.choice(filteredPractice)
        wordTensePairs2Practice.remove(practice)
        filteredPractice.remove(practice)
        savePracticeFile()

        randWord = practice["word"]
        randTense = practice["tense"]
        randPartOfSpeech = practice["partOS"]
        translation = practice["prompt"]
        answer = practice["answer"]
        reverse_chosen = practice["reversal"]
        return randWord, randTense, randPartOfSpeech,translation, answer, reverse_chosen

#  function to update the 'turns' variable.  This variable keeps
#  track of whether the current round is a practice round or a regular round
def updateTurns():
    global turns
    if practiceOn:
        turns += 1

# function to save the collection of words the user had trouble with to a file for long term storage
def savePracticeFile():
    f = open("practice.txt", "w")
    f.write(f"{wordTensePairs2Practice}")
    f.close()

#function to load the collection of words the user had trouble with into memory
def loadPracticeFile():
    try:
        f = open("practice.txt", 'r')
        ret = eval(f.read())
        f.close()
        return ret
    except FileNotFoundError:
        return []

# function to remove the accents in words from the data file so that
# the user doesn't have to worry about typing them when they anser the challenge questions
def removeAccents(word):
    accents = [("é", "e"), ("í", "i"), ("ú", "u"), ("á", "a"), ("ñ", "n"), ("ó", "o")]
    for acc in accents:
        word = word.replace(acc[0], acc[1])
    return word

#  Function to check if the user's submitted answer was right or wrong
def checkSubmission(submission, answer):
    # in case they included "yo" or "el" or "ella" etc.  we'll get rid of that because we don't need it
    submission2 = ""
    try:
        firstSpaceInd = submission.index(" ")
        submission2 = submission[firstSpaceInd:]
    except:
        pass

    # check if there is a "/" present in the answer
    if "/" in answer:
    # split by / first, then split by spaces.  Then put the first element with the second and third eleement for ans1 and ans2
        option1, option2 = tuple(answer.split("/"))
        option1s = option1.split(" ")
        for stemLen in range(1, len(option1s)):
            stem = " ".join(option1s[:stemLen])
            option1 = " ".join(option1s[stemLen:])

            ans1 = f"{stem} {option1}"
            ans2 = f"{stem} {option2}"

            if submission == ans1.lower() or submission == ans2.lower():
                return True

    #check if answer contains parenthesees
    if "(" in answer:
        parts = answer.split("(")
        ans1 = parts[0].strip()
        ans2 = parts[1].replace(")", "")
        if submission == ans1 or submission == ans2:
            return True
    return submission2 == answer or submission == answer.lower()

# get a list of all verbs and tenses
words = list(data.keys())
firstWord = words[0]
tense_choices = list(data[firstWord].keys())



#  ask user which tenses they would like to practice (display a lettered list)
print("Which tenses do you want to practice right now? (Input comma separated list of numbers)")
choiceNum = 1
for tense in tense_choices:
    print(f"{choiceNum}.  {tense}")
    choiceNum += 1
user_tenses = input("").split(",")

print("Choose Mode:")
print("a)  English Prompts & Spanish Answers")
print("b)  Spanish Prompts & English Answers")
print("c)  Both")
choice = input("")

# lambda functino that will determine if each round will be asking
# the user to translate English to Spanish or Spanish to English
reverse = {"a":lambda: False, "b":lambda: True, "c": lambda: random.choice([True, False])}[choice.lower()]

print("Run with practice?:")
print("a)  Yes")
print("b)  No")
choice = input("")

#determine if user wants to run the system with the practice feature activated
practiceOn = 'a' == choice.lower() or 'y' == choice.lower() or 'yes' == choice.lower()

#  get a list of the user's desired tenses they want to practice
for choice in user_tenses:
    chosen_tenses.append(tense_choices[int(choice) - 1])

#load the practice file and filter out the practice that doesn't correspond to the tenses the user wants to practice
wordTensePairs2Practice = loadPracticeFile()
filteredPractice = filterPracticePairs()

#set the turns variable to 0.  This means that the first round will be a regular round
turns = 0



#Each iteration of this loop will be a round in which a new challenge word is chosen for the user,
# either randomly or based on words they struggled with in the past
while True:
    # update the round type and get the challenge word and associated info
    updateTurns()
    randWord, randTense, randPartOfSpeech,translation, answer, reverse_chosen = getInfo(turns)
    partsOfSpeech = list(data[randWord][randTense].keys())

    engEx = data[randWord][randTense][randPartOfSpeech]["english example"]
    spEx = data[randWord][randTense][randPartOfSpeech]["spanish example"]

    #  variable to keep track of how many incorrect attempts the user had this round
    incorrect = 0

    #each iteration of this loop will be an attempt for the user to
    # either translate the challenge word correctly or ask the system for clues (or the answer itself)
    while True:
        # inform the user of their current score
        print(f"Score: {  {True: lambda: 0, False: lambda : round(correct*100/trials, 2)}[trials == 0]()  }% of {trials} trials")

        # English to Spanish round
        if not reverse_chosen:
            print(f"Please Translate:  {translation}  \n")
        #Spanish to English round
        else:
            print(f"Please Translate:  {answer} \n")

        #Display Menu Choices to User
        print("Type correct conjugation to submit an answer or choose from below:")
        print("a) View Spanish Infinitive")
        print("b) View English Example")
        print("c) View Spanish Example")
        print("d) View Tense")

        #interpret the menu choice and respond with the appropriate action
        submission = input("").lower().strip().replace(")", "")
        #User wants to view the spanish infinitive
        if submission == "a":
            print(f"{randWord}")

        # User wants to view the english example (probably to get more context concerning the tense or part of
        # speech if it's an English to Spanish round, or to just get the answer because they gave up during a
        # Spanish to English round)
        elif submission == "b":
            print(f"{engEx}")

        # User wants to view the spanish example (probably to get more context concerning the tense or part of
        #         # speech if it's a Spanish to English round, or to just get the answer because they gave up during a
        #         # English to Spanish round)
        elif submission == "c":
            print(f"{spEx}")

        #  User wants to see the tense of the word
        elif submission == "d":
            print(f"{randTense}")

        #  It's currently a spanish to english round and the user's answer needs to be checked.
        elif not reverse_chosen and checkSubmission(submission, answer): #submission in answer:
            correct += 1
            trials += 1
            print("Correct!!!")
            print(f"Eng Example: {engEx}")
            print(f"Sp Example: {spEx}")
            print("\n")
            break

        # it's currently an English to Spanish round and the user's answer needs to be checked
        elif reverse_chosen and checkSubmission(submission, translation): #submission in answer:
            correct += 1
            trials += 1
            print("Correct!!!")
            print(f"Eng Example: {engEx}")
            print(f"Sp Example: {spEx}")
            print("\n")

            break
        else:
            # means the user's answer was incorrect
            trials += 1
            incorrect += 1
            print("Incorrect, please try again.")

            #  User hit the max number of times they can get the answer incorrect before the word is added for practice
            if incorrect == 3:
                #  now add every part of speech option for that word tense pair to the list for practice and
                #  then save to the file
                print("Adding to practice...  continue please")
                for partOS in partsOfSpeech:
                    trans = data[randWord][randTense][partOS]["translation"]
                    ans_raw = data[randWord][randTense][partOS]["conjugation"]
                    ans = removeAccents(ans_raw.lower())
                    for _ in range(2):
                        newPractice = {"prompt":trans, "tense":randTense, "word":randWord,
                                        "answer":ans,  "partOS":partOS, "reversal":reverse_chosen}
                        wordTensePairs2Practice.append(newPractice)
                        filteredPractice.append(newPractice)
                savePracticeFile()






#  Let the user know if they were right or wrong and then display the english and spanish examples.

# Repeat

#  Need a way to remember which word/tense/part of speech combinations need more practice.
#  Need a way to add or view hints/info about a conjugation.


# sample of the input data file
'''
Format:
{"ser": {
  "present Indicative tense": {
    "I": {"conjugation": "soy", "translation": "I am", "spanish example": "Soy estudiante", "english example":"I am a student"},
    "you": {"conjugation": "eres", "translation": "you are", "spanish example": "Eres inteligente", "english example":"You are intelligent"},
    "he": {"conjugation": "es", "translation": "he is", "spanish example": "Él es alto", "english example":"He is tall"},
    "we": {"conjugation": "somos", "translation": "we are", "spanish example": "Somos amigos", "english example":"We are friends"},
    "they": {"conjugation": "son", "translation": "they are", "spanish example": "Ellos son hermanos", "english example":"They are siblings"}
  },
  "present perfect tense": {
    "I": {"conjugation": "he sido", "translation": "I have been", "spanish example": "He sido feliz", "english example":"I have been happy"},
    "you": {"conjugation": "has sido", "translation": "you have been", "spanish example": "Has sido generoso", "english example":"You have been generous"},
    "he": {"conjugation": "ha sido", "translation": "he has been", "spanish example": "Él ha sido paciente", "english example":"He has been patient"},
    "we": {"conjugation": "hemos sido", "translation": "we have been", "spanish example": "Hemos sido amigos desde la infancia", "english example":"We have been friends since childhood"},
    "they": {"conjugation": "han sido", "translation": "they have been", "spanish example": "Ellos han sido exitosos en su carrera", "english example":"They have been successful in their career"}
  },
  "present subjunctive tense": {
    "I": {"conjugation": "sea", "translation": "I am", "spanish example": "Espero que sea posible", "english example":"I hope it is possible"},
    "you": {"conjugation": "seas", "translation": "you are", "spanish example": "Es importante que seas honesto", "english example":"It is important that you are honest"},
    "he": {"conjugation": "sea", "translation": "he is", "spanish example": "No creo que sea justo", "english example":"I don't think he is fair"},
    "we": {"conjugation": "seamos", "translation": "we are", "spanish example": "Espero que seamos amigos por mucho tiempo", "english example":"I hope we are friends for a long time"},
    "they": {"conjugation": "sean", "translation": "they are", "spanish example": "Es probable que sean felices juntos", "english example":"They are likely to be happy together"}
  },
  "preterite tense": {
    "I": {"conjugation": "fui", "translation": "I was/went", "spanish example": "Fui al cine anoche", "english example":"I went to the cinema last night"},
    "you": {"conjugation": "fuiste", "translation": "you were/went", "spanish example": "¿Fuiste a la fiesta?", "english example":"Were you at the party?"},
    "he": {"conjugation": "fue", "translation": "he was/went", "spanish example": "Él fue al supermercado", "english example":"He went to the supermarket"},
    "we": {"conjugation": "fuimos", "translation": "we were/went", "spanish example": "Fuimos de vacaciones el verano pasado", "english example":"We went on vacation last summer"},
    "they": {"conjugation": "fueron", "translation": "they were/went", "spanish example": "Ellos fueron al concierto", "english example":"They went to the concert"}
  },
  "past perfect tense": {
    "I": {"conjugation": "había sido", "translation": "I had been", "spanish example": "Antes de eso, ya había sido profesor", "english example":"Before that, I had already been a teacher"},
    "you": {"conjugation": "habías sido", "translation": "you had been", "spanish example": "Me dijiste que ya habías sido presidente", "english example":"You told me that you had already been president"},
    "he": {"conjugation": "había sido", "translation": "he had been", "spanish example": "Él había sido un gran líder", "english example":"He had been a great leader"},
    "we": {"conjugation": "habíamos sido", "translation": "we had been", "spanish example": "Ya habíamos sido socios en el pasado", "english example":"We had already been partners in the past"},
    "they": {"conjugation": "habían sido", "translation": "they had been", "spanish example": "Ellos habían sido buenos amigos por mucho tiempo", "english example":"They had been good friends for a long time"}
  },
  "past subjunctive tense": {
    "I": {"conjugation": "fuera/fuese", "translation": "I had been/were", "spanish example": "Ojalá que fuera posible", "english example":"I wish it were possible"},
    "you": {"conjugation": "fueras/fueses", "translation": "you had been/were", "spanish example": "Si tú fueras más valiente, lo harías", "english example":"If you were braver, you would do it"},
    "he": {"conjugation": "fuera/fuese", "translation": "he had been/were", "spanish example": "No creía que él fuera honesto", "english example":"I didn't believe he was honest"},
    "we": {"conjugation": "fuéramos/fuésemos", "translation": "we had been/were", "spanish example": "Si fuéramos más ricos, viajaríamos más", "english example":"If we were richer, we would travel more"},
    "they": {"conjugation": "fueran/fuesen", "translation": "they had been/were", "spanish example": "Era improbable que fueran exitosos", "english example":"It was unlikely that they were successful"}
  },
  "past imperfect tense": {
    "I": {"conjugation": "era", "translation": "I used to be", "spanish example": "Cuando era joven, era muy tímido", "english example":"When I was young, I used to be very shy"},
    "you": {"conjugation": "eras", "translation": "you used to be", "spanish example": "De niño, eras muy travieso", "english example":"As a child, you used to be very mischievous"},
    "he": {"conjugation": "era", "translation": "he used to be", "spanish example": "Mi abuelo era un gran músico", "english example":"My grandfather used to be a great musician"},
    "we": {"conjugation": "éramos", "translation": "we used to be", "spanish example": "Antes, éramos vecinos", "english example":"Before, we used to be neighbors"},
    "they": {"conjugation": "eran", "translation": "they used to be", "spanish example": "Mis padres eran muy trabajadores", "english example":"My parents used to be very hardworking"}
  },
  "future tense": {
    "I": {"conjugation": "seré", "translation": "I will be", "spanish example": "En el futuro, seré arquitecto", "english example":"In the future, I will be an architect"},
    "you": {"conjugation": "serás", "translation": "you will be", "spanish example": "¿Serás mi compañero de viaje?", "english example":"Will you be my travel companion?"},
    "he": {"conjugation": "será", "translation": "he will be", "spanish example": "Él será famoso algún día", "english example":"He will be famous someday"},
    "we": {"conjugation": "seremos", "translation": "we will be", "spanish example": "Seremos vecinos en el futuro", "english example":"We will be neighbors in the future"},
    "they": {"conjugation": "serán", "translation": "they will be", "spanish example": "Ellos serán grandes profesionales", "english example":"They will be great professionals"}
  }
}}



'''
