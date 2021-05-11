import os
import time
import numpy as np
from tkinter import *
from tkinter import ttk
from Loader import testing
from PIL import Image, ImageDraw


def clean():
    canvas.delete('all')
    draw.rectangle((0, 0, 350, 350), fill=(255, 255, 255, 0))
    predictLabel.config(text='')
    progressBar.stop()


def activate_paint(e):
    global x1, y1
    canvas.bind('<B1-Motion>', paint)
    x1, y1 = e.x, e.y


def paint(e):
    global x1, y1

    x2, y2 = e.x, e.y
    canvas.create_line((x1, y1, x2, y2), fill='black', width=10)

    draw.line((x1, y1, x2, y2), fill='black', width=10)
    x1, y1 = x2, y2


def save():
    num = 0
    is_not = True

    while is_not:

        if os.path.exists('img/temp/%s.png' % num):
            num += 1
        else:
            is_not = False

    filename = 'img/temp/%s.png' % num
    print(filename)
    image1.save(filename)


def model():
    filename = 'img/temp/temp.png'
    image1.save(filename)

    predict = testing(lang=switch_variable.get())

    classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    print('Digit ', np.argmax(predict[0]), '\n',
          'Accuracy ', predict[0][np.argmax(predict[0])], '\n', classes[np.argmax(predict[0])])

    txt = "Digit: {}\nAccuracy: {}%".format(classes[np.argmax(predict[0])],
                                            round(predict[0][np.argmax(predict[0])] * 100, 3))
    predictLabel.config(text=txt)


def prediction():
    for x in range(5):
        progressBar['value'] += 20
        middleFrame.update_idletasks()
        time.sleep(0.15)

    if progressBar['value'] == 100:
        model()


# Full Window
root = Tk()
root.configure(bg='black')
root.title('Digit Recognizer')
root.resizable(0, 0)
root.geometry('400x600')

icon = PhotoImage(file='img/icon/icon.png')
root.iconphoto(False, icon)

x1, y1 = None, None

# Layer 1
###############

switch_frame = Frame(root)
switch_frame.pack(anchor='e', padx=10, pady=10)

language = 'eng'

switch_variable = StringVar(value="eng")
eng_button = Radiobutton(switch_frame, text="English", variable=switch_variable, indicatoron=False, value="eng",
                         width=8)
ben_button = Radiobutton(switch_frame, text="Bengali", variable=switch_variable, indicatoron=False, value="ben",
                         width=8)

eng_button.pack(side="left")
ben_button.pack(side="left")

# Layer 2
###############

topFrame = Frame(root)
topFrame.config(bg='black')
topFrame.pack()

canvas = Canvas(topFrame, width=350, height=350, bg='white', bd=-2)
canvas.pack(padx=20, pady=10, anchor='c')
canvas.bind('<1>', activate_paint)

image1 = Image.new('RGB', (350, 350), 'white')
draw = ImageDraw.Draw(image1)

# Layer 3
###############

middleFrame = Frame(root, width=500, height=50)
middleFrame.config(bg='black')
middleFrame.pack(pady=10)

progressBar = ttk.Progressbar(middleFrame, orient=HORIZONTAL, length=380, mode='determinate')
progressBar.pack()

# Layer 4
###############

bottomFrame = Frame(root, width=400, height=100)
bottomFrame.config(bg='black')
bottomFrame.pack(padx=10, pady=10)

cleanButton = Button(bottomFrame, text='Clean', command=clean)
cleanButton.grid(row=0)

predictButton = Button(bottomFrame, text='Recognize', command=prediction)
predictButton.grid(row=0, column=1, padx=20)

saveButton = Button(bottomFrame, text=' Save ', command=save)
saveButton.grid(row=0, column=2)

predictLabel = Label(root, text='', bg='black', fg='white', font=('', 24))
predictLabel.pack(pady=15)

######################################
root.mainloop()
