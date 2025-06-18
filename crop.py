'''
획득한 이미지의 전처리과정
측정 부위 수동으로 크롭 진행
'''
import cv2
import os
import numpy as np

image_folder = r'C:\Users\박영욱\OneDrive\바탕 화면\preprocessing\taeyeon\Picture\L_2'
output_folder = os.path.join(image_folder, 'crops')
os.makedirs(output_folder, exist_ok=True)

CROP_WIDTH = 180 
CROP_HEIGHT = 256

image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))])
crop_count = 0

def load_image_unicode(path):
    stream = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(stream, cv2.IMREAD_COLOR)

def draw_box_on_image(img, center):
    cx, cy = center
    x1 = max(0, cx - CROP_WIDTH // 2)
    y1 = max(0, cy - CROP_HEIGHT // 2)
    x2 = min(x1 + CROP_WIDTH, img.shape[1])
    y2 = min(y1 + CROP_HEIGHT, img.shape[0])
    img_copy = img.copy()
    cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return img_copy

for i, file in enumerate(image_files):
    img_path = os.path.join(image_folder, file)
    current_img = load_image_unicode(img_path)

    if current_img is None:
        print(f"이미지 로드 실패: {img_path}")
        continue

    print(f"[{i+1}/{len(image_files)}] {file}")
    box_center = (current_img.shape[1] // 2, current_img.shape[0] // 2)
    drag_start = None
    drawing = False

    def mouse_callback(event, x, y, flags, param):
        global box_center, drag_start, drawing, display_img  

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            drag_start = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            temp_center = ((drag_start[0] + x) // 2, (drag_start[1] + y) // 2)
            display_img = draw_box_on_image(current_img, temp_center)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            box_center = ((drag_start[0] + x) // 2, (drag_start[1] + y) // 2)
            display_img = draw_box_on_image(current_img, box_center)

    display_img = draw_box_on_image(current_img, box_center)

    cv2.namedWindow("Crop Tool")
    cv2.setMouseCallback("Crop Tool", mouse_callback)

    while True:
        cv2.imshow("Crop Tool", display_img)
        key = cv2.waitKey(1)

        if key == 13:  # Enter → crop 저장
            cx, cy = box_center
            x1 = max(0, cx - CROP_WIDTH // 2)
            y1 = max(0, cy - CROP_HEIGHT // 2)
            x2 = min(x1 + CROP_WIDTH, current_img.shape[1])
            y2 = min(y1 + CROP_HEIGHT, current_img.shape[0])
            crop = current_img[y1:y2, x1:x2]
            save_path = os.path.join(output_folder, f"crop_{crop_count+1}.png")
            cv2.imencode('.png', crop)[1].tofile(save_path)
            print(f"✅ Saved: {save_path}")
            crop_count += 1

        # N과 ESC 눌러 각 역할 진행
        elif key == ord('n') or key == ord('N'):  
            print("➡️ 다음 이미지로 이동")
            break

        elif key == 27:  
            print("⛔ 중단됨")
            exit()

    cv2.destroyAllWindows()
