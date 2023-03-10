import turtle as tu
import tkinter

root = tkinter.Tk()
root.geometry('500x500-5+40') #added by me
cv = tu.ScrolledCanvas(root, width=1500000, height=1500000)
cv.pack()

letters = list("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split())
morse = list(" .- / -... / -.-. / -.. / . / ..-. / --. / .... / .. / .--- / -.- / .-.. / -- / -. / --- / .--. / --.- / .-. / ... / - / ..- / ...- / .-- / -..- / -.-- / --..".split('/'))

letters_to_morse = dict(zip(letters,[x.replace(" ","") for x in morse]))

letters_to_morse

bind = {'.':2,"-":30}

screen = tu.TurtleScreen(cv)
screen.screensize(1500000,1500000) #added by me
t = tu.RawTurtle(screen)


t.pensize(10)
t.ht()

for i in "OMKAR is panda".upper():
    if i !=" ":
        for j in letters_to_morse[i]:
            t.pd()
            t.fd(bind[j])
            t.pu()
            t.fd(20)
            t.pd()
        print(i)
    if i==" ":
        t.pd()
        t.lt(90)
        t.fd(20)
        t.bk(20)
        t.rt(90)
    t.pu()
    t.fd(50)
root.mainloop()
