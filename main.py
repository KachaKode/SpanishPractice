#  load up the word bank

tense_choices = []
chosen_tenses = []
accents = ["é", "í",  "ú",  "á", "ñ", "ó"]
#  ask user which tenses they would like to practice (display a lettered list)

#  randomly choose a word, then tense, then part of speech.  Display the english translation then give options:
#  a) View Spanish Infinitive
#  b) View English Example
#  c) View Spanish Example
#  Type correct conjugation to submit an answer

#  Let the user know if they were right or wrong and then display the english and spanish examples.

# Repeat

#  Need a way to remember which word/tense/part of speech combinations need more practice.

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









def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
