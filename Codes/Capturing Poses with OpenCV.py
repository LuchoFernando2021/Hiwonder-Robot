#!/usr/bin/env python3
# -- coding: utf-8 --

import cv2
import mediapipe as mp
import numpy as np
import json
import os

# ===============================
# Archivo donde se guardarán las poses humanas
# ===============================
POSE_FILE = "poses_humanas.json"

# ===============================
# Cargar base de datos existente o crear una nueva
# ===============================
if os.path.exists(POSE_FILE):
    with open(POSE_FILE, "r") as f:
        pose_database = json.load(f)
else:
    pose_database = {}

# ===============================
# Inicializar MediaPipe Pose
# ===============================
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# ===============================
# Inicializar cámara (ajusta la ruta si es necesario)
# ===============================
cap = cv2.VideoCapture("/dev/usb_cam")

# Verificar que la cámara esté disponible
if not cap.isOpened():
    print("❌ Error: No se pudo abrir la cámara en /dev/usb_cam.")
    print("👉 Verifica con el comando:")
    print("   ls /dev/video*")
    print("y cambia la ruta en cap = cv2.VideoCapture(...) según corresponda.")
    exit()

# ===============================
# Función para extraer coordenadas de la pose
# ===============================
def extract_pose_vector(results):
    """
    Extrae coordenadas normalizadas (x) de los puntos clave:
    hombros, codos y muñecas izquierda y derecha.
    """
    if not results.pose_landmarks:
        return None

    lm = results.pose_landmarks.landmark
    vector = [
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
        lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
        lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x
    ]
    return vector

# ===============================
# Bucle principal de captura
# ===============================
print("📸 Presiona 'c' para capturar una pose (1–50) y 'q' para salir.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo leer frame de la cámara.")
        break

 # Procesar imagen con MediaPipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # Dibujar landmarks de la pose
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

    # Mostrar ventana
    cv2.imshow("Captura de poses", frame)

    # Controles de teclado
    key = cv2.waitKey(10) & 0xFF
    if key == ord("q"):  # Salir
        break
    elif key == ord("c"):  # Capturar pose
        pose_id = input("Número de pose (1–50): ").strip()

        # Validar que sea un número dentro del rango
        if pose_id.isdigit():
            pose_num = int(pose_id)
            if 1 <= pose_num <= 50:
                vector = extract_pose_vector(results)
                if vector is not None:
                    pose_database[pose_id] = vector
                    print(f"✅ Pose {pose_id} guardada correctamente.")

                    with open(POSE_FILE, "w") as f:
                        json.dump(pose_database, f, indent=2)
                else:
                    print("⚠️ No se detectó ninguna pose. Intenta de nuevo.")
            else:
                print("⚠️ Solo puedes guardar poses del 1 al 50.")
        else:
            print("⚠️ Ingresa un número válido entre 1 y 50.")

# ===============================
# Cierre ordenado
# ===============================
cap.release()
cv2.destroyAllWindows()
