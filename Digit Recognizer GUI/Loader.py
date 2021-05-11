import cv2
from keras.models import load_model


def testing(lang):

    """
        This method loads the models of english and bengali depending
        on which one is select through the method parameter.
    """

    img = cv2.imread('img/temp/temp.png', 0)
    img = cv2.bitwise_not(img)
    img = cv2.resize(img, (28, 28)).reshape(1, 28, 28, 1).astype('float32')
    img /= 255.0

    print(lang + 't')

    if lang == 'eng':
        model = load_model('models/E_D_9944.h5')
    elif lang == 'ben':
        model = load_model('models/numtabd.h5')

    predict = model.predict(img)
    return predict
