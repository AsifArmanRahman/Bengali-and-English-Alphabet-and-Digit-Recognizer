import os
import cv2
import time
import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw
from tensorflow.keras.models import load_model


def image_load():
    img = cv2.imread('img/temp/temp.png', 0)
    img = cv2.bitwise_not(img)
    img = cv2.resize(img, (28, 28)).reshape(1, 28, 28, 1).astype('float32')
    img /= 255.0

    return img


def prediction(language, type):
    model = None

    if language == 'eng':
        if type == 'alphabet':
            model = load_model('models/output/E_A.h5')
        elif type == 'digit':
            model = load_model('models/output/E_D.h5')

    elif language == 'ben':
        if type == 'alphabet':
            model = load_model('models/output/B_A.h5')
        elif type == 'digit':
            model = load_model('models/output/B_D.h5')

    predict = model.predict(image_load())

    return predict


class App:
    def __init__(self):
        # Full Window
        self.root = Tk()
        self.root.configure(bg='black')
        self.root.title('Handwritten Alphabet and Digit Recognizer')
        self.root.resizable(0, 0)
        self.root.geometry('400x630')

        icon = PhotoImage(file='img/icon/icon.png')
        self.root.iconphoto(False, icon)

        self.x1, self.y1 = None, None
        self.x2, self.y2 = None, None

        # Layer 1
        ###############

        self.switch_frame1 = Frame(self.root)
        self.switch_frame1.pack(anchor='e', padx=10, pady=10)

        self.switch_variable1 = StringVar(value="eng")
        self.eng_button = Radiobutton(self.switch_frame1, text="English", variable=self.switch_variable1,
                                      indicatoron=False, value="eng", width=8)
        self.ben_button = Radiobutton(self.switch_frame1, text="Bengali", variable=self.switch_variable1,
                                      indicatoron=False, value="ben", width=8)

        self.eng_button.pack(side="left")
        self.ben_button.pack(side="left")

        # Layer 1 - 1
        ###############

        self.switch_frame2 = Frame(self.root)
        self.switch_frame2.pack(anchor='w', padx=10, pady=0)

        self.switch_variable2 = StringVar(value="alphabet")
        self.alpha_button = Radiobutton(self.switch_frame2, text="Alphabet", variable=self.switch_variable2,
                                        indicatoron=False, value="alphabet", width=8)
        self.digit_button = Radiobutton(self.switch_frame2, text="Digit", variable=self.switch_variable2,
                                        indicatoron=False, value="digit", width=8)

        self.alpha_button.pack(side="left")
        self.digit_button.pack(side="left")

        # Layer 2
        ###############

        self.topFrame = Frame(self.root)
        self.topFrame.config(bg='black')
        self.topFrame.pack()

        self.canvas = Canvas(self.topFrame, width=350, height=350, bg='white', bd=-2)
        self.canvas.pack(padx=20, pady=10, anchor='c')
        self.canvas.bind('<1>', self.activate_paint)

        self.image1 = Image.new('RGB', (350, 350), 'white')
        self.draw = ImageDraw.Draw(self.image1)

        # Layer 3
        ###############

        self.middleFrame = Frame(self.root, width=500, height=50)
        self.middleFrame.config(bg='black')
        self.middleFrame.pack(pady=10)

        self.progressBar = ttk.Progressbar(self.middleFrame, orient=HORIZONTAL, length=380, mode='determinate')
        self.progressBar.pack()

        # Layer 4
        ###############

        self.bottomFrame = Frame(self.root, width=400, height=100)
        self.bottomFrame.config(bg='black')
        self.bottomFrame.pack(padx=10, pady=10)

        self.cleanButton = Button(self.bottomFrame, text='Clean', command=self.clean)
        self.cleanButton.grid(row=0)

        self.predictButton = Button(self.bottomFrame, text='Recognize', command=self.predict)
        self.predictButton.grid(row=0, column=1, padx=20)

        self.saveButton = Button(self.bottomFrame, text=' Save ', command=self.save)
        self.saveButton.grid(row=0, column=2)

        self.predictLabel = Label(self.root, text='', bg='black', fg='white', font=('', 24))
        self.predictLabel.pack(pady=15)

        ######################################
        self.root.mainloop()

    def clean(self):
        self.canvas.delete('all')
        self.draw.rectangle((0, 0, 350, 350), fill=(255, 255, 255, 0))
        self.predictLabel.config(text='')
        self.progressBar.stop()

    def activate_paint(self, e):
        self.canvas.bind('<B1-Motion>', self.paint)
        self.x1, self.y1 = e.x, e.y

    def paint(self, e):
        self.x2, self.y2 = e.x, e.y
        self.canvas.create_line((self.x1, self.y1, self.x2, self.y2), fill='black', width=10)
        self.draw.line((self.x1, self.y1, self.x2, self.y2), fill='black', width=10)
        self.x1, self.y1 = self.x2, self.y2

    def save(self):
        num = 0
        is_not = True

        while is_not:

            if os.path.exists('img/temp/%s.png' % num):
                num += 1
            else:
                is_not = False

        filename = 'img/temp/%s.png' % num
        print(filename)
        self.image1.save(filename)

    def model(self):
        filename = 'img/temp/temp.png'
        self.image1.save(filename)

        predict = prediction(self.switch_variable1.get(), self.switch_variable2.get())

        if self.switch_variable2.get() == 'digit':
            if self.switch_variable1.get() == 'eng':
                classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

            elif self.switch_variable1.get() == 'ben':
                classes = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯']

        elif self.switch_variable2.get() == 'alphabet':
            if self.switch_variable1.get() == 'eng':
                classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            elif self.switch_variable1.get() == 'ben':
                classes = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'অ', 'আ', 'ই', 'ঈ', 'উ', 'ঊ', 'ঋ', 'এ',
                           'ঐ', 'ও', 'ঔ', 'ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ', 'ট', 'ঠ', 'ড', 'ঢ', 'ণ',
                           'ত', 'থ', 'দ', 'ধ', 'ন', 'প', 'ফ', 'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ', 'স', 'হ', 'ড়',
                           'ঢ়', 'য়', 'ৎ', 'ং', 'ঃ', ' ঁ']

        print('Digit', np.argmax(predict[0]), '\nAccuracy', predict[0][np.argmax(predict[0])],
              classes[np.argmax(predict[0])])

        txt = "Digit: {}\nAccuracy: {}%".format(classes[np.argmax(predict[0])],
                                                round(predict[0][np.argmax(predict[0])] * 100, 3))
        self.predictLabel.config(text=txt)

    def predict(self):
        for x in range(5):
            self.progressBar['value'] += 20
            self.middleFrame.update_idletasks()
            time.sleep(0.15)

        if self.progressBar['value'] == 100:
            self.model()


app = App()
