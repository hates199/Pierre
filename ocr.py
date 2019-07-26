from PIL import Image
import pytesseract
import cv2
import os

def ocr_core(filename, option="thresh", sel_lang="eng"):
    """
    This function will handle the core OCR processing of images.
    """
    # "C:\Users\body\Desktop\flask_tesseract\images\img (1).jpg"
    print(filename)
    image = cv2.imread("C:\\Users\\body\\Desktop\\Pierre\\app\\static\\uploads\\"+filename)

    # print(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if option == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    elif option == "blur":
        gray = cv2.medianBlur(gray, 3)

    cv2.imwrite(filename, gray)
    new_lang = sel_lang[0] if len(sel_lang) == 1 else '+'.join(sel_lang)
    text = pytesseract.image_to_string(Image.open(filename), lang=new_lang)
    os.remove(filename)
    
    return text