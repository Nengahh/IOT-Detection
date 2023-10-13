import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import json
import cv2

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

pan = GPIO.PWM(18, 50) # pin 18 untuk pan
tilt = GPIO.PWM(24, 50) # pin 24 untuk tilt
buzzer = GPIO.PWM(25, 50) # pin 25 untuk buzzer
pan.start(0)
tilt.start(0)
buzzer.start(0)

camera = PiCamera()
camera.resolution = (400, 400) # set resolusi gambar menjadi 400x400
val_pan = -45 # posisi awal pan
val_tilt = -45 # posisi awal tilt
i = 45 # nilai penambahan rotasi
id_gambar = 1 # id gambar awal
nama_file = 'gambar.json' # nama file JSON untuk menyimpan data gambar

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

try:
    while True:
        pan.ChangeDutyCycle(2 + (val_pan/18))
        tilt.ChangeDutyCycle(2 + (val_tilt/18))
        time.sleep(1) # tunggu 1 detik untuk posisi stabil

        # ambil gambar
        nama_gambar = 'gambar' + time.strftime("%Y%m%d%H%M%S",time.localtime()) + '.jpg'
        camera.capture(nama_gambar)
        
        # deteksi wajah
        img = cv2.imread(nama_gambar)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) >= 2:
            buzzer.ChangeDutyCycle(50) # nyala buzzer
            time.sleep(0.5)
            buzzer.ChangeDutyCycle(0) # mati buzzer
        
        # simpan data gambar, rotasi, dan id gambar ke dalam file JSON
        data = {}
        data['id'] = id_gambar
        data['pan'] = val_pan
        data['tilt'] = val_tilt
        data['filename'] = nama_gambar # tambahkan nama file gambar ke dalam data
        with open(nama_file, 'a') as f:
            json.dump(data, f)
            f.write('\n')

        # increment id gambar dan rotasi
        id_gambar += 1
        val_pan += i
        if val_pan > 45:
            val_pan = -45
            val_tilt += i
            if val_tilt > 45:
                val_tilt = -45

except KeyboardInterrupt:
    pan.stop()
    tilt.stop()
    buzzer.stop()
    GPIO.cleanup()
