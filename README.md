# Şablon Eşleştirme İle Vidyodan Görüntü Tespiti

Bu proje, OpenCV kütüphanesi kullanılarak kullanıcının seçtiği bir şablon görüntüyü, şablon eşleştirme yöntemi ile vidyodan bu nesneyi tespit etmeye yarayan bir uygulamayı içerir. 

## Şablon Eşleştirme
Şablon eşleştirme, bir görüntünün şablon görüntüsüne (yama) uyan alanlarını bulmak için
kullanılan bir tekniktir. Yama bir dikdörtgen olmalı ama bu dikdörtgen tamamen alakalı
olamayabilir. İki temel bileşene ihtiyacımız var:
- Kaynak resim (I): Şablon resmine bir eşleşme bulmayı beklediğimiz resim
- Şablon resmi (T): Kaynak resimle karşılaştırılacak yama resmi
Eşleşen alanı belirlemek için şablon resmini kaydırarak kaynak resimle karşılaştırmamız gerekir.
Kaydırma ile yukarı aşağı sağa sola giderek eşleşmelere bakılır ve eşleşmenin iyi mi kötü mü
olduğuna dair temsili bir metrik hesaplanır.

**Temel Mantık:**
- Şablon görüntü alınır ve gri tona çevrilir
- Şablon bulunacağı vide okunur ve frame frame alınır.
- frame gri tona çevrilir
-  `match_template()` fonksyonu ile şablon eşleştirme yapılır
-  `match_template_draw()` fonksiyonu ile bulunan eşleştirmeler frame görüntüye sarı dikdörtgen ile çizilir
-  frame görüntüsü ekrana yansıtılır
-  Eğer herhangi bir eşleşme yoksa video devam eder ancak eşleşme varsa eşleşme görsterilir ve vidyo duraklatılır bunu da `paused` değişkeniyle sağlar
-  `q` tuşuna basıldığında uygulama sonlandırılır.

**Avantajları:**
- Uygulaması kolaydır
- Karmaşık ön işleme süreci ve eğitim gerekmez
- Kullanıcı tanımlı bir ROI üzerinden tespit yapmak mümkündür

**Dezavantajları:**
- Şablonun açısı veya boyutu değişirse algılaması zordur
- Şablon ve görüntü arasında zıtlıklar fazla ise doğru algılayamayabilir
- Şablon ile bazı nesneler benzer ise yanlış tespit yapabilir

## Şablon Eşleştirme ile Vidyodan Görüntü Bulma Uygulaması

Aşağıda Python kodu ve açıklamaları yer almaktadır.

```python
import cv2
import numpy as np

class TemplateMatching:
    def __init__(self, img):
        # Şablon resmi (gri tonlamalı) ve boyutları alınır
        self.template = img
        self.w, self.h = self.template.shape[::-1]
        self.paused = False  # Video duraklatma kontrolü

    def match_template(self, image):
        # Template matching işlemi yapılır (eşleşme skorları elde edilir)
        res = cv2.matchTemplate(image, self.template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Eşik değeri: 0.8 ve üzeri benzerlik kabul edilir
        self.loc = np.where(res >= threshold)  # Eşik üzerindeki koordinatlar bulunur
        self.tump = zip(*self.loc[::-1])  # (x, y) şeklinde noktalar
        self.tump_size = len(list(self.tump))  # Kaç eşleşme bulunduğu sayılır

    def match_template_draw(self, w, h):
        # Eşleşen tüm bölgelerin üzerine dikdörtgen çizilir
        for pt in zip(*self.loc[::-1]):
            cv2.rectangle(self.frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    def main(self):
        video = cv2.VideoCapture('video01.mp4')  # Video dosyası açılır

        while True:
            if not self.paused:
                ret, self.frame = video.read()  # Yeni kare alınır
                if not ret:
                    break  # Video sona erdiyse döngüden çık
                frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)  # Gri tonlamaya dönüştürülür
                self.match_template(frame_gray)  # Şablon eşleştirme yapılır
                self.match_template_draw(self.w, self.h)  # Eşleşen bölgeler çizilir

            cv2.imshow('Detected', self.frame)  # Kare ekrana gösterilir

            if self.tump_size != 0:
                self.paused = True  # Nesne bulunduysa video duraklatılır

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break  # 'q' tuşuna basılırsa çıkılır

if __name__ == '__main__':
    template = cv2.imread('foto_sablon.jpg', 0)  # Şablon görüntüsü (gri) yüklenir
    proses = TemplateMatching(template)  # TemplateMatching nesnesi oluşturulur
    proses.main()  # Uygulama başlatılır

```
## Parametre Detayları

### 1. `threshold`
- Eşleşmenin kabul edilmesi için gereken benzerlik eşiğini belirtir.

## Etkileyen Faktörler
- Şablon ile İçinde arama yapılacak görüntü boyutu farklı ise eşleşme başarısız olabilir
- Şablon görüntünün açısı ile görüntü açısı feklı ise eşleşme başarısız olabilir
- Şablon görüntü ile görüntü arasındaki Tonlama zıtlıkları benzerlik oranını düşürebilir
- Görüntüde şablonla benzer görüntüler varsa yanlış eşleştirme yapabilir yani arka plan karmaşıklığı olumsuz etkiler

## Sonuç 
Bu proje, OpenCV'nin Şablon eşleştirme yöntemi ile şablon görüntüyü vidyoda bulmamızı sağlar. 
`threshold` parametresinin düzgün belirlenmesi hangi eşleştirmenin gösterilmesi gerektiği konusunda önemli rol oynar.
Bu proje, şablon eşleştirme yöntemini öğrenmek isteyenler için temel düzeyde anlaşılır ve uygulaması kolay bir başlangıçtır. Görüntü işleme konusuna giriş yapmak, temel kavramları öğrenmek ve pratik yapmak için uygundur.
Ancak, şablon eşleştirme yönteminin bazı kısıtları bulunduğundan, daha karmaşık ve dinamik senaryolarda daha gelişmiş algoritmalar tercih edilebilir.


