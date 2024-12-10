import cv2
import mediapipe as mp
import numpy as np
import math

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

    count_right = 0
    count_left = 0
    prev_state = "Straight"

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

                # Hitung kemiringan
                if movement_detected != prev_state and movement_detected != "Straight":
                    if movement_detected == "Right":
                        count_right += 1
                    elif movement_detected == "Left":
                        count_left += 1

                prev_state = movement_detected

                # Visualisasi status kemiringan dan jumlah hitungan
                cv2.putText(frame, f"Right Count: {count_right}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Left Count: {count_left}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Current: {movement_detected}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow('Head Movement Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total kemiringan ke kanan: {count_right}")
    print(f"Total kemiringan ke kiri: {count_left}")

if __name__ == "__main__":
    main()
