import cv2
import mediapipe as mp
import numpy as np
import time
import random
import os

# Inisialisasi MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Fungsi untuk mendeteksi kemiringan kepala
def detect_head_movement_with_angle(left_eye, right_eye):
    left_eye_center = (left_eye[0], left_eye[1])
    right_eye_center = (right_eye[0], right_eye[1])

    delta_x = right_eye_center[0] - left_eye_center[0]
    delta_y = right_eye_center[1] - left_eye_center[1]

    # Hitung sudut menggunakan formula kemiringan
    angle = np.arctan2(delta_y, delta_x)
    angle = np.degrees(angle)

    # Threshold untuk mendeteksi kemiringan
    if angle > 10:
        return "Right", angle
    elif angle < -10:
        return "Left", angle
    else:
        return "Straight", angle

def overlay_image_with_alpha(frame, img, x1, y1, x2, y2):
    if img.shape[2] == 4:  # Gambar dengan transparansi
        alpha_channel = img[:, :, 3]  # Saluran alfa
        rgb_channels = img[:, :, :3]  # Saluran RGB

        for c in range(3):  # Untuk setiap saluran warna
            frame[y1:y2, x1:x2, c] = frame[y1:y2, x1:x2, c] * (1 - alpha_channel / 255.0) + \
                                     rgb_channels[:, :, c] * (alpha_channel / 255.0)
    else:
        # Jika gambar tidak transparan, langsung tempel
        frame[y1:y2, x1:x2] = img

def show_score_image(score):
    # Tentukan path untuk gambar skor
    score_images_path = "hasil"
    score_image_file = f"{score_images_path}/skor{score}.png"

    # Cek apakah gambar ada
    if os.path.exists(score_image_file):
        score_img = cv2.imread(score_image_file)
        if score_img is not None:
            cv2.imshow("Your Score", score_img)
            cv2.waitKey(0)  # Tunggu hingga pengguna menekan tombol apapun
            cv2.destroyAllWindows()

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera tidak dapat diakses.")
        return

    print("Mulai mendeteksi kemiringan kepala...")

    # Path ke folder gambar pertanyaan
    question_images_path = "quiz-question"
    question_images = [f"{question_images_path}/q{i}.png" for i in range(1, 6)]

    current_question = 0
    score = 0
    prev_state = "Straight"
    question_start_time = time.time()
    is_shuffling = False
    shuffle_start_time = None
    selected_question = None

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
                # Landmark untuk mata kiri dan mata kanan
                left_eye_landmark = face_landmarks.landmark[159]
                right_eye_landmark = face_landmarks.landmark[386]

                # Landmark untuk hidung sebagai referensi area rambut
                nose_landmark = face_landmarks.landmark[1]

                # Koordinat mata dan hidung dalam piksel
                h, w, _ = frame.shape
                left_eye = (int(left_eye_landmark.x * w), int(left_eye_landmark.y * h))
                right_eye = (int(right_eye_landmark.x * w), int(right_eye_landmark.y * h))
                nose_x, nose_y = int(nose_landmark.x * w), int((nose_landmark.y - 0.15) * h)

                # Deteksi kemiringan berdasarkan mata
                movement_detected, angle = detect_head_movement_with_angle(left_eye, right_eye)

                if movement_detected == "Straight" and current_question < len(question_images):
                    if not is_shuffling and selected_question is None:
                        is_shuffling = True
                        shuffle_start_time = time.time()

                    if is_shuffling:
                        if time.time() - shuffle_start_time < 2.0:
                            shuffle_index = random.randint(0, len(question_images) - 1)
                            shuffle_img = cv2.imread(question_images[shuffle_index], cv2.IMREAD_UNCHANGED)
                            shuffle_img_resized = cv2.resize(shuffle_img, (300, 200))
                            x1, y1 = nose_x - shuffle_img_resized.shape[1] // 2, nose_y - shuffle_img_resized.shape[0]
                            x2, y2 = x1 + shuffle_img_resized.shape[1], y1 + shuffle_img_resized.shape[0]

                            if x1 >= 0 and y1 >= 0 and x2 <= w and y2 <= h:
                                overlay_image_with_alpha(frame, shuffle_img_resized, x1, y1, x2, y2)
                        else:
                            is_shuffling = False
                            selected_question = question_images[current_question]

                    if selected_question:
                        question_img = cv2.imread(selected_question, cv2.IMREAD_UNCHANGED)
                        question_img_resized = cv2.resize(question_img, (300, 200))
                        x1, y1 = nose_x - question_img_resized.shape[1] // 2, nose_y - question_img_resized.shape[0]
                        x2, y2 = x1 + question_img_resized.shape[1], y1 + question_img_resized.shape[0]

                        if x1 >= 0 and y1 >= 0 and x2 <= w and y2 <= h:
                            overlay_image_with_alpha(frame, question_img_resized, x1, y1, x2, y2)

                if movement_detected != "Straight" and movement_detected != prev_state and selected_question:
                    user_answer = "YES" if movement_detected == "Right" else "NO"

                    correct_answers = ["NO", "NO", "YES", "YES", "NO"]
                    if user_answer == correct_answers[current_question]:
                        score += 1

                    current_question += 1
                    question_start_time = time.time()
                    selected_question = None

                prev_state = movement_detected

        # Menampilkan skor setelah semua pertanyaan dijawab
        if current_question >= len(question_images):
            cv2.putText(frame, f"Final Score: {score}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            if current_question == len(question_images):
                show_score_image(score)  # Tampilkan gambar skor

        cv2.imshow('Head Movement Quiz', frame)

        if current_question >= len(question_images) or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
    print(f"Quiz Selesai! Skor akhir Anda: {score}/{len(question_images)}")

if __name__ == "__main__":
    main()
