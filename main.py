import cv2
import numpy as np


class TemplateMatching:
    def __init__(self, img):
        self.template = img
        self.w, self.h = self.template.shape[::-1]
        self.paused = False
    
    def match_template(self, image):
        res = cv2.matchTemplate(image, self.template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        self.loc = np.where(res >= threshold)
        self.tump = zip(*self.loc[::-1])
        self.tump_size = len(list(self.tump))
        
    def match_template_draw(self, w, h):
        for pt in zip(*self.loc[::-1]):
            cv2.rectangle(self.frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
        

    def main(self):
        video = cv2.VideoCapture('video01.mp4')
        
        while True:
            if not self.paused:
                ret, self.frame = video.read()
                frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                self.match_template(frame_gray)
                self.match_template_draw(self.w, self.h)
    

            cv2.imshow('Detected', self.frame)
    
            if self.tump_size != 0:
                self.paused = True
        
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == '__main__':
    template = cv2.imread('foto_sablon.jpg', 0)
    proses = TemplateMatching(template)
    proses.main()
    