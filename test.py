import cv2
import mediapipe as mp
import numpy as np
import time
import random

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

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera tidak dapat diakses.")
        return

    print("Mulai mendeteksi kemiringan kepala...")

    questions = [
        {"question": "Apakah 2 + 2 = 4?", "answer": "YES"},
        {"question": "Apakah matahari terbit di barat?", "answer": "NO"},
        {"question": "Apakah Python adalah bahasa pemrograman?", "answer": "YES"},
        {"question": "Apakah ikan bisa terbang?", "answer": "NO"},
        {"question": "Apakah bulan lebih besar dari bumi?", "answer": "NO"}
    ]

    current_question = 0
    score = 0
    prev_state = "Straight"
    is_shuffling = False
    shuffle_start_time = None
    show_question = False

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
                left_eye_landmark = face_landmarks.landmark[159]  # Landmark tengah mata kiri
                right_eye_landmark = face_landmarks.landmark[386]  # Landmark tengah mata kanan

                # Koordinat mata dalam piksel
                h, w, _ = frame.shape
                left_eye = (int(left_eye_landmark.x * w), int(left_eye_landmark.y * h))
                right_eye = (int(right_eye_landmark.x * w), int(right_eye_landmark.y * h))

                # Deteksi kemiringan berdasarkan mata
                movement_detected, angle = detect_head_movement_with_angle(left_eye, right_eye)

                # Jika kepala lurus dan tidak sedang mengacak pertanyaan
                if movement_detected == "Straight" and current_question < len(questions):
                    if not is_shuffling and not show_question:
                        is_shuffling = True
                        shuffle_start_time = time.time()
                        random.shuffle(questions)

                    if is_shuffling and time.time() - shuffle_start_time < 2.0:  # Animasi pengacakan selama 2 detik
                        shuffle_index = random.randint(0, len(questions) - 1)
                        shuffle_text = questions[shuffle_index]["question"]
                        cv2.putText(frame, f"Shuffling: {shuffle_text}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                    elif is_shuffling:
                        is_shuffling = False
                        show_question = True

                    if show_question:
                        question = questions[current_question]["question"]
                        cv2.putText(frame, f"Question {current_question + 1}: {question}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Deteksi jawaban jika kepala miring
                if movement_detected != "Straight" and movement_detected != prev_state and current_question < len(questions):
                    user_answer = "YES" if movement_detected == "Right" else "NO"

                    if user_answer == questions[current_question]["answer"]:
                        score += 1

                    current_question += 1
                    show_question = False

                prev_state = movement_detected

        # Tampilkan skor dan status
        cv2.putText(frame, f"Score: {score}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        if current_question >= len(questions):
            cv2.putText(frame, "Quiz Finished!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Head Movement Quiz', frame)

        if current_question >= len(questions) or cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Quiz Selesai! Skor akhir Anda: {score}/{len(questions)}")

if __name__ == "__main__":
    main()
