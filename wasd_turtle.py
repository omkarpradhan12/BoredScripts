import turtle as tu
import tkinter
import keyboard

root = tkinter.Tk()
root.geometry('2000x1000-5+40')
cv = tu.ScrolledCanvas(root, width=1500000, height=1500000)
cv.pack()


screen = tu.TurtleScreen(cv)
screen.screensize(1500000,1500000)
t = tu.RawTurtle(screen)

psize=1

t.pensize(psize)

screen.bgcolor('white')

t.pd()
t.lt(90)
while(True):
    if keyboard.is_pressed('w'):
        t.fd(1)
    if keyboard.is_pressed('a'):
        t.lt(5)
    if keyboard.is_pressed('s'):
        t.bk(1)
    if keyboard.is_pressed('d'):
        t.rt(5)
    if keyboard.is_pressed('up'):
        t.pu()
    if keyboard.is_pressed('down'):
        t.pd()
    if keyboard.is_pressed('q'):
        cv.postscript(file='f.ps',colormode='color')
        exit()
        break
    if keyboard.is_pressed('-'):
        if psize>0:
            psize-=1
        else:
            psize=0
        t.pensize(psize)
    if keyboard.is_pressed('+'):
        psize+=1
        t.pensize(psize)

    if keyboard.is_pressed('1'):
        t.color('black')
    if keyboard.is_pressed('2'):
        t.color('red')
    if keyboard.is_pressed('3'):
        t.color('blue')
    if keyboard.is_pressed('4'):
        t.color('green')
    if keyboard.is_pressed('5'):
        t.color('teal')
    if keyboard.is_pressed('6'):
        t.color('orange')

    if keyboard.is_pressed('e'):
        t.color('white')
    if keyboard.is_pressed('p'):
        t.color('black')


