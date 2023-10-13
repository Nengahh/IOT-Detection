import cv2
import json
import os
from datetime import datetime


with open('data.json', 'r') as f:
    data = json.load(f)

with open('data2.json', 'r') as f1:
    data2 = json.load(f1)



# Mendapatkan tanggal dan waktu saat ini
now = datetime.now()

# Format tanggal sesuai dengan yang diinginkan
current_time = now.strftime("%Y-%m-%d")


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')

face_count = 0
face_no_mask = 0
face_with_mask = 0
nearby_face = 0

# Mengambil gambar dari folder static flash
img_folder = 'res'
img_names = os.listdir(img_folder)

for img_name in img_names:
    img_path = img_folder + '/' + img_name
    img = cv2.imread(img_path)

    # Konversi gambar ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # masih bisa di sesuwaikan
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Deteksi mata 
        eyes = eye_cascade.detectMultiScale(gray[y:y+h, x:x+w])

        # Deteksi hidung 
        noses = nose_cascade.detectMultiScale(gray[y:y+h, x:x+w])

        # Cek apakah hidung terdeteksi di bawah mata
        nose_detected = False
        for (nx, ny, nw, nh) in noses:
            if ny > y+h/2:
                nose_detected = True

        if nose_detected:
            # Jika hidung terdeteksi di bawah mata, artinya tidak menggunakan masker
            face_no_mask += 1
        else:
            # Jika hidung tidak terdeteksi di bawah mata, artinya menggunakan masker
            face_with_mask += 1

        # Tambahkan 1 pada variabel jumlah wajah yang terdeteksi
        face_count += 1


        # Cek lebih dari satu wajah yang terdeteksi
        if len(faces) >= 2:
            nearby_face += 1

        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2) #hanya testing melihat bounding box
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(img[y:y+h, x:x+w], (ex, ey), (ex+ew, ey+eh), (0, 0, 255), 2)
    cv2.imshow('frame', img)
    cv2.waitKey()
    cv2.destroyAllWindows()
 
# for item in data:
#     # ambil nama file dari atribut JSON
#     filename = item['filename']
#     # membuka file gambar menggunakan OpenCV
#     img = cv2.imread(filename)

# nyimpan nilai jumlah wajah yang menggunakan masker, tidak menggunakan masker, dan jumlah wajah yang terlalu dekat
# data = {
#     'face_with_mask': face_with_mask,
#     'face_no_mask': face_no_mask,
#     'nearby_face': nearby_face,
#     'face_count': face_count,
#     'current_time' : current_time,

# }


# data['results'].append({
#             'face_with_mask': face_with_mask,
#             'face_no_mask': face_no_mask,
#             'nearby_face': nearby_face,
#             'face_count': face_count,
#             'current_time': current_time
#         })


if current_time not in data:
    data[current_time] = {
        'Jumlah Penghuni': face_count,
        'Wajah Tanpa Masker': face_no_mask,
        'Berdekatan': nearby_face,
        'Wajah Masker': face_with_mask
    }
else:
    existing_data = data[current_time]
    existing_data['Jumlah Penghuni'] += face_count
    existing_data['Wajah Tanpa Masker'] += face_no_mask
    existing_data['Berdekatan'] += nearby_face
    existing_data['Wajah Masker'] += face_with_mask

    # Reset nilai variabel
face_count = 0
face_no_mask = 0
face_with_mask = 0
nearby_face = 0


with open('data.json', 'w') as json_file: #timpa data json, jika ingin meload data tiap iterasi 
    json.dump(data, json_file)
