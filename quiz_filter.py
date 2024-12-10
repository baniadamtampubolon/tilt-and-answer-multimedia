import cv2
import mediapipe as mp
import random
import time
import math

# Inisialisasi MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Fungsi untuk menghitung sudut antara tiga titik
# Menggunakan koordinat landmark untuk mendeteksi kemiringan kepala
def calculate_angle(point1, point2, point3):
    dx1, dy1 = point1.x - point2.x, point1.y - point2.y
    dx2, dy2 = point3.x - point2.x, point3.y - point2.y
    angle = math.degrees(math.atan2(dy2, dx2) - math.atan2(dy1, dx1))
    return angle

# Fungsi untuk mendeteksi kemiringan kepala (tilt)
def detect_head_movement(landmarks):
    left_ear = landmarks[234]  # Landmark di sekitar telinga kiri
    right_ear = landmarks[454]  # Landmark di sekitar telinga kanan
    nose_tip = landmarks[1]  # Landmark ujung hidung

    # Hitung sudut antara hidung dan kedua telinga
    angle = calculate_angle(left_ear, nose_tip, right_ear)

    # Threshold untuk menentukan kemiringan
    if angle > 10:  # Kepala miring ke kanan
        return "Right"
    elif angle < -10:  # Kepala miring ke kiri
        return "Left"
    else:  # Tidak ada kemiringan
        return "None"

# Pertanyaan dan jawaban
questions = [
    {"question": "quiz-question/q2.png", "correct": "Right", "wrong": "Left"},
    {"question": "quiz-question/q3.png", "correct": "Right", "wrong": "Left"},
    {"question": "quiz-question/q4.png", "correct": "Left", "wrong": "Right"}
]

# Fungsi untuk menjalankan kuis
def run_quiz():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera tidak dapat diakses.")
        return

    score = 0  # Jumlah jawaban benar
    total_questions = len(questions)
    start_time = time.time()
    time_limit = 60  # Waktu total untuk kuis

    question_index = 0  # Indeks pertanyaan saat ini

    while cap.isOpened():
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= time_limit:
            print(f"Waktu habis! Skor akhir Anda: {score}/{total_questions}")
            break

        question = questions[question_index]
        print(f"Menampilkan pertanyaan dari: {question['question']}")
        print(f"Kanan untuk '{question['correct']}', Kiri untuk '{question['wrong']}'")

        answered = False

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Tidak dapat membaca frame dari kamera.")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    movement_detected = detect_head_movement(face_landmarks.landmark)

                    # Koordinat rambut untuk menempatkan gambar
                    nose = face_landmarks.landmark[1]
                    forehead_y_offset = 0.15  # Offset ke atas untuk area rambut
                    h, w, _ = frame.shape
                    nose_x, nose_y = int(nose.x * w), int((nose.y - forehead_y_offset) * h)

                    # Tampilkan gambar pertanyaan di atas rambut
                    question_image = cv2.imread(question['question'])
                    if question_image is not None:
                        question_image = cv2.resize(question_image, (150, 100))  # Sesuaikan ukuran gambar
                        img_h, img_w, _ = question_image.shape

                        # Koordinat untuk menggambar gambar pertanyaan
                        x1, y1 = nose_x - img_w // 2, nose_y - img_h
                        x2, y2 = x1 + img_w, y1 + img_h

                        # Pastikan koordinat dalam batas frame
                        if x1 >= 0 and y1 >= 0 and x2 <= w and y2 <= h:
                            frame[y1:y2, x1:x2] = question_image

                    # Cek apakah kepala digoyangkan ke kanan atau kiri
                    if movement_detected in ["Right", "Left"] and not answered:
                        answered = True
                        if movement_detected == question["correct"]:
                            score += 1
                            feedback = "Jawaban Benar!"
                        else:
                            feedback = "Jawaban Salah!"

                        # Tampilkan umpan balik di layar
                        cv2.putText(frame, feedback, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        question_index = (question_index + 1) % total_questions
                        break

            # Menampilkan skor dan waktu yang tersisa
            remaining_time = time_limit - int(elapsed_time)
            cv2.putText(frame, f"Sisa waktu: {remaining_time}s", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"Skor: {score}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            cv2.imshow('Quiz Filter', frame)

            # Keluar jika 'q' ditekan
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_quiz()
