import turtle as tu
import tkinter

root = tkinter.Tk()
root.geometry('500x500-5+40') #added by me
cv = tu.ScrolledCanvas(root, width=900, height=900)
cv.pack()

letters = list("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split())
morse = list(" .- / -... / -.-. / -.. / . / ..-. / --. / .... / .. / .--- / -.- / .-.. / -- / -. / --- / .--. / --.- / .-. / ... / - / ..- / ...- / .-- / -..- / -.-- / --..".split('/'))

letters_to_morse = dict(zip(letters,[x.replace(" ","") for x in morse]))

letters_to_morse

bind = {'.':2,"-":30}

screen = tu.TurtleScreen(cv)
screen.screensize(2000,1500) #added by me
t = tu.RawTurtle(screen)


t.pensize(10)
t.ht()

for i in "GITHUB":
    for j in letters_to_morse[i]:
        t.pd()
        t.fd(bind[j])
        t.pu()
        t.fd(20)
        t.pd()
    t.pu()
    t.fd(50)
root.mainloop()
