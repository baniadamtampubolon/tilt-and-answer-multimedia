import cv2
import mediapipe as mp
import math

# Inisialisasi MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Fungsi untuk menghitung sudut antara tiga titik
def calculate_angle(point1, point2, point3):
    dx1, dy1 = point1.x - point2.x, point1.y - point2.y
    dx2, dy2 = point3.x - point2.x, point3.y - point2.y
    angle = math.degrees(math.atan2(dy2, dx2) - math.atan2(dy1, dx1))
    return angle

# Fungsi untuk mendeteksi kemiringan kepala
def detect_head_movement(landmarks, initial_angle):
    left_ear = landmarks[234]  # Landmark di sekitar telinga kiri
    right_ear = landmarks[454]  # Landmark di sekitar telinga kanan
    nose_tip = landmarks[1]  # Landmark ujung hidung

    # Hitung sudut antara hidung dan kedua telinga
    angle = calculate_angle(left_ear, nose_tip, right_ear)
    relative_angle = angle - initial_angle

    # Threshold untuk menentukan kemiringan (sensitivitas rendah)
    if relative_angle > 28:  # Kepala miring ke kanan
        return "Right", relative_angle
    elif relative_angle < -200:  # Kepala miring ke kiri
        return "Left", relative_angle
    else:  # Kepala lurus
        return "Straight", relative_angle

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera tidak dapat diakses.")
        return

    print("Kalibrasi posisi kepala lurus. Harap tetap diam.")
    initial_angle = None

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
                if initial_angle is None:
                    # Kalibrasi sudut awal
                    left_ear = face_landmarks.landmark[234]
                    right_ear = face_landmarks.landmark[454]
                    nose_tip = face_landmarks.landmark[1]
                    initial_angle = calculate_angle(left_ear, nose_tip, right_ear)
                    print("Kalibrasi selesai. Sudut awal:", initial_angle)
                    continue

                # Visualisasi semua landmark wajah
                h, w, _ = frame.shape
                for idx, landmark in enumerate(face_landmarks.landmark):
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)

                movement_detected, angle = detect_head_movement(face_landmarks.landmark, initial_angle)

                # Tampilkan sudut dan status kemiringan kepala
                cv2.putText(frame, f"Angle: {angle:.2f} degrees", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                if movement_detected == "Right":
                    cv2.putText(frame, "Kepala miring ke kanan", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif movement_detected == "Left":
                    cv2.putText(frame, "Kepala miring ke kiri", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif movement_detected == "Straight":
                    cv2.putText(frame, "Kepala lurus", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow('Head Movement Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
