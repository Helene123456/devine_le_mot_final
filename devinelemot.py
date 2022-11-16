from flask import Flask, render_template, request

import sqlite3 as sql

from random import randint

 

app= Flask("fghjklm")

 

#integrer html des deux premières pages

@app.route ("/")

def page_garde ():

    return render_template ("p_garde.html")

 

@app.route ("/if3/")

def page_regles ():

    return render_template ("p_regles.html")




word_to_guess = None

user_letters = []

 

def cacher(word):

    display = ""

    for n in word :

        if n in user_letters :

            display += n

        else:

            display += "?"

 

    return display

 

def compute_error():

    errors = 0

    for letter in user_letters:

        if letter not in word_to_guess[1]:

            errors += 1

    return errors




@app.route("/game", methods=['POST', 'GET'])

def word():

    global word_to_guess

    global user_letters

 

    if request.method == 'POST':

        letter = request.form['lettre_joueur']

        if len(letter) == 1 and letter not in user_letters :

            user_letters.append(letter)

              

        else :

            if len(letter) != 1 :

                message= "Introduis UNE lettre à la fois ;-)"

            else :

                message= "Cette lettre a déjà été introduite."

            display = cacher(word_to_guess[1])

            errors = compute_error()

            lost_message = "PERDU!"[:errors]

       

            return render_template("formulaire_test.html", word=display, letters=user_letters, message=message, lost=lost_message)

        #que une à la fois

 

    if word_to_guess == None:

        #print ("peu importe")

        connection = sql.connect("mots_def.sqlite")

        cursor = connection.cursor()

        query = f"SELECT * FROM mots_et_def"

        cursor.execute(query)

 

        words = cursor.fetchall()  # word ou db result

        connection.close()

 

        index = randint(0, len(words)-1) # word ou db result

        word_to_guess = words[index] # word ou db result

 

       

 

    display = cacher(word_to_guess[1])

    errors = compute_error()

    lost_message = "PERDU!"[:errors]

   

    if display == word_to_guess[1] :

        word = word_to_guess # ! on le sauvegarde !

        word_to_guess = None

        display=""

        lost_message = ""

        user_letters = []

 

        return render_template("gagne.html", rep=word[1], definition=word[2])

   

    if lost_message == "PERDU!":

        word = word_to_guess # ! on le sauvegarde !

        word_to_guess=None

        lost_message = ""

        display = ""

        user_letters = []

   

        return render_template("perdu.html", rep=word[1])

 

       

       

 

    return render_template("formulaire_test.html", word=display, letters=user_letters, lost=lost_message)

 

#------------------------------------------------------------------------------------------------------------------------#

 

#------

 

app.run()