import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
point_list=[]
image_path = "C:\\logy\\text.jpg" #스캔할 이미지 경로 입력(절대경로)
src_img = cv2.imread(image_path)

COLOR=(255,0,255) # 핑크
THICKNESS = 3
drawing = False # 선을 그릴지 여부

def mouse_handler(event,x,y,flags,param):
    global drawing
    dst_img=src_img.copy()
    
    if event == cv2.EVENT_LBUTTONDOWN:#마우스 왼쪽 버튼 down
        drawing = True #선을그리기 시작
        point_list.append((x,y))
        
    if drawing :
        prev_point = None # 직선의 시작점
        first_point = 1
        for point in point_list:
            cv2.circle(dst_img,point,5,COLOR,cv2.FILLED)
            if prev_point:
                cv2.line(dst_img,prev_point,point,COLOR,THICKNESS,cv2.LINE_AA)
            prev_point = point 
        next_point=(x,y)
        cv2.line(dst_img,prev_point,next_point,COLOR,THICKNESS,cv2.LINE_AA)
        
    if len(point_list)==4:
        show_result()# 결과 출력
        next_point = point_list[0] #깔끔한 선정리를 위해 첫점, 끝점 연결
        cv2.line(src_img,prev_point,next_point,COLOR,THICKNESS,cv2.LINE_AA)
    cv2.imshow('img',dst_img)   
    
def show_result():
    
    width, height = 530, 710 # 가로 세로 크기 설정

    src = np.float32(point_list)
    dst = np.array([[0,0],[width,0],[width,height],[0,height]],dtype=np.float32)
    # 좌상, 우상, 우하, 좌하(시계방향으로 4지점 정의)
    
    matrix = cv2.getPerspectiveTransform(src,dst)# matrix 얻어오기
    result = cv2.warpPerspective(src_img,matrix,(width,height)) #행렬값 적용후 결과 
    cv2.imwrite('text_save.jpg',result,)#스캔한 이미지 저장
    
cv2.namedWindow('img')
cv2.setMouseCallback('img',mouse_handler)
cv2.imshow('img',src_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 스캔한 이미지 등록
image = cv2.imread('text_save.jpg')

# 이미지 전처리를 위해 흑백으로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 이미지에서 텍스트 추출
text = pytesseract.image_to_string(gray, lang='eng')

# 추출한 텍스트 출력
print(text)