import cv2
import pytesseract
import numpy as np
from tkinter import Tk, Label, Button, filedialog, Text

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
point_list = []

class ImageScanner:
    def __init__(self, window):
        self.window = window
        window.title("이미지 텍스트 추출기")

        self.label = Label(window, text="이미지 선택")
        self.label.pack()

        self.select_button = Button(window, text="이미지 선택", command=self.select_image)
        self.select_button.pack()

        self.text_area = Text(window, height=15, width=50)
        self.text_area.pack()

    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.scan_image(file_path)

    def scan_image(self, image_path):
        global point_list
        point_list = []

        src_img = cv2.imread(image_path)
        cv2.namedWindow('Select Area')
        cv2.setMouseCallback('Select Area', self.mouse_handler, src_img)
        cv2.imshow('Select Area', src_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Extract text
        image = cv2.imread('text_save.jpg')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, lang='eng')
        self.text_area.delete(1.0, "end")
        self.text_area.insert("insert", text)

    def mouse_handler(self, event, x, y, flags, param):
        global point_list
        dst_img = param.copy()

        if event == cv2.EVENT_LBUTTONDOWN:
            point_list.append((x, y))

        if point_list:
            prev_point = None
            for point in point_list:
                cv2.circle(dst_img, point, 5, (255, 0, 255), cv2.FILLED)
                if prev_point:
                    cv2.line(dst_img, prev_point, point, (255, 0, 255), 3, cv2.LINE_AA)
                prev_point = point
            next_point = (x, y)
            cv2.line(dst_img, prev_point, next_point, (255, 0, 255), 3, cv2.LINE_AA)

        if len(point_list) == 4:
            self.show_result(param)
            next_point = point_list[0]
            cv2.line(dst_img, prev_point, next_point, (255, 0, 255), 3, cv2.LINE_AA)
            cv2.imshow('Select Area', dst_img)
            cv2.waitKey(0)

        cv2.imshow('Select Area', dst_img)

    def show_result(self, src_img):
        width = max(np.linalg.norm(np.array(point_list[1])-np.array(point_list[0])),
                    np.linalg.norm(np.array(point_list[2])-np.array(point_list[3])))
        height = max(np.linalg.norm(np.array(point_list[2])-np.array(point_list[1])),
                     np.linalg.norm(np.array(point_list[3])-np.array(point_list[0])))

        width, height = int(width), int(height)

        src = np.float32(point_list)
        dst = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

        matrix = cv2.getPerspectiveTransform(src, dst)
        result = cv2.warpPerspective(src_img, matrix, (width, height))
        cv2.imwrite('text_save.jpg', result)

root = Tk()
scanner = ImageScanner(root)
root.mainloop()