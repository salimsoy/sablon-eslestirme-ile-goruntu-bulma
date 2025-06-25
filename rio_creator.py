import cv2

class RioCreator:
    def __init__(self, path):
        self.path = path
        self.paused = False
    

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            r = cv2.selectROI("select the area", param)
    
            self.cropped_image = param[int(r[1]):int(r[1]+r[3]), 
                                  int(r[0]):int(r[0]+r[2])]
        
            self.paused = True
            cv2.imshow('Detected', self.cropped_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def main(self):
        cap = cv2.VideoCapture(self.path)
        while True:
            if not self.paused:
                ret, frame = cap.read()
                if not ret:
                    break
        
                cv2.imshow('Detected', frame)
                cv2.setMouseCallback('Detected', self.click_event, frame)
            else:
                break
        
            
            if cv2.waitKey(30) & 0xFF == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()
