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

## 2. Yöntem

## Vidyodan rio seçip  Şablon Eşleştirme ile vidyoda bulma


### `rio_creator.py`
- Kullanıcının video üzerinde fare ile bir bölge seçmesini sağlar.
- Seçilen bölge `cropped_image` kaydedilir.
- Seçim yapıldıktan sonra video duraklatılır ve seçilen görüntü gösterilir.

Aşağıda Python kodu ve açıklamaları yer almaktadır.

```python
import cv2

# ROI seçimi yapan sınıf
class RioCreator:
    def __init__(self, path):
        self.path = path            # Video dosyasının yolu
        self.paused = False         # Seçim sonrası videoyu durdurmak için kontrol bayrağı

    # Fare tıklama olayı için callback fonksiyonu
    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # Sol tıklama olursa:
            # Kullanıcıdan ROI (seçim kutusu) alınır
            r = cv2.selectROI("Rioyu secici", param)

            # Seçilen alan kırpılır (y1:y2, x1:x2)
            self.cropped_image = param[int(r[1]):int(r[1]+r[3]), 
                                       int(r[0]):int(r[0]+r[2])]

            # Durum bayrağı duraklatılır
            self.paused = True

            # Seçilen ROI gösterilir
            cv2.imshow('RİO', self.cropped_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()  # Seçim pencereleri kapatılır

    # Ana çalışma fonksiyonu: video oynatma + tıklamayla ROI seçimi
    def main(self):
        cap = cv2.VideoCapture(self.path)  # Video dosyasını aç

        while True:
            if not self.paused:
                ret, frame = cap.read()  # Yeni kareyi oku
                if not ret:
                    break  # Video bittiğinde çık

                # Kareyi ekranda göster
                cv2.imshow('video', frame)

                # Her kare için fare tıklama olayını kontrol et
                cv2.setMouseCallback('video', self.click_event, frame)
            else:
                break  # Eğer kullanıcı ROI seçtiyse döngüden çık

            # ESC tuşuna basılırsa çık
            if cv2.waitKey(30) & 0xFF == 27:
                break

        # Kaynaklar serbest bırakılır
        cap.release()
        cv2.destroyAllWindows()

```
### `main_1.py`
`rio_creator.py` dosyasındaki RioCreator sınıfı kullanılarak RIO seçimi yapılır. RIO seçimi yapıldıktan sonra RIO görselini daha önceden açıklamış ve yazmış olduğumuz şablon eşitleme kodunda şablon görüntü olarak veriyoruz.

Aşağıda Python kodu ve açıklamaları yer almaktadır.
```python
import cv2
import numpy as np
from rio_creator import RioCreator  # ROI seçimi yapan sınıfı içe aktar

# Şablon eşleştirme sınıfı
class TemplateMatching:
    def __init__(self, img):
        self.template = img  # ROI'den alınan şablon resmi (grayscale)
        self.w, self.h = self.template.shape[::-1]  # Genişlik ve yükseklik (şablon)
        self.paused = False  # Video durdurulmuş mu bilgisi

    # Şablonu video karesinde arayan fonksiyon
    def match_template(self, image):
        # Template Matching algoritması uygulanır
        res = cv2.matchTemplate(image, self.template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Eşik değer
        self.loc = np.where(res >= threshold)  # Eşik üzerindeki koordinatlar
        self.tump = list(zip(*self.loc[::-1]))  # Koordinatları (x, y) olarak al
        self.tump_size = len(self.tump)  # Kaç eşleşme bulundu

    # Eşleşen yerleri çizimle gösteren fonksiyon
    def match_template_draw(self, w, h):
        for pt in self.tump:  # Tüm eşleşmeler üzerinde dön
            # Eşleşme kutularını çizer
            cv2.rectangle(self.frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    # Ana döngü
    def main(self):
        video = cv2.VideoCapture('video01.mp4')  # Videoyu aç
        
        while True:
            if not self.paused:
                ret, self.frame = video.read()  # Kareyi oku
                if not ret:
                    break

                # Gri tona dönüştür (eşleştirme için gereklidir)
                frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

                # Eşleştirme işlemi yap
                self.match_template(frame_gray)

                # Eşleşmeleri çiz
                self.match_template_draw(self.w, self.h)

            # Sonuç görüntüsünü göster
            cv2.imshow('Detected', self.frame)

            # Eşleşme bulunduysa durdur
            if self.tump_size != 0:
                self.paused = True

            # 'q' tuşuna basılırsa çık
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

# Ana uygulama
if __name__ == '__main__':
    path = 'video01.mp4'

    # ROI seçimi için RioCreator sınıfı kullanılır
    proses_rio = RioCreator(path)
    proses_rio.main()  # ROI kullanıcı tarafından seçilir

    # Seçilen ROI görüntüsünü griye dönüştür
    gray_img = cv2.cvtColor(proses_rio.cropped_image, cv2.COLOR_BGR2GRAY)

    # TemplateMatching sınıfına gri şablonu ver
    proses = TemplateMatching(gray_img)

    # Eşleştirme işlemini başlat
    proses.main()

```



