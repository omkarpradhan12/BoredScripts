from winsound import Beep

letters = list("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split())
morse = list(" .- / -... / -.-. / -.. / . / ..-. / --. / .... / .. / .--- / -.- / .-.. / -- / -. / --- / .--. / --.- / .-. / ... / - / ..- / ...- / .-- / -..- / -.-- / --..".split('/'))

letters_to_morse = dict(zip(letters,[x.replace(" ","") for x in morse]))

letters_to_morse

beeper = {".":400,"-":800}

def morsemaker(message):
    cipher = ""
    for letter in message.upper():
        if letter in [l for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]:
            for beep in letters_to_morse[letter]:
                Beep(1000,beeper[beep])
                cipher+=beep
            cipher+=" "
            Beep(3000,200)
        if letter==" ":
            Beep(5000,1000)
            cipher+="/"
        else:
            cipher+=''
    return cipher

morse_to_letters = dict(zip([x.replace(" ","") for x in morse],letters))

def morsedecoder(cipher):
    message = ""
    for morse in cipher.split("/"):
        for bep in morse.split():
            message+=morse_to_letters[bep]
        message+=" "
    
    return message


morsemaker("Bhiow,sdfsdfsdf")


