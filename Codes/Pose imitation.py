#!/usr/bin/env python3
# -- coding: utf-8 --

import cv2
import mediapipe as mp
import numpy as np
import json
import time
from ainex_kinematics.motion_manager import MotionManager
from Poses import poses  # importamos tus 50 poses del robot

# ===============================
# Configuración
# ===============================
POSE_FILE = "poses_humanas.json"  # Archivo con las 50 poses humanas
DIST_THRESHOLD = 0.15  # Umbral de similitud (ajústalo si es necesario)

# ===============================
# Cargar poses humanas
# ===============================
with open(POSE_FILE, "r") as f:
    human_poses = json.load(f)
print(f"✅ {len(human_poses)} poses humanas cargadas desde {POSE_FILE}.")

# ===============================
# Inicializar MotionManager
# ===============================
motion_manager = MotionManager(action_path='/home/ubuntu/software/ainex_control>

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
# Configurar cámara
# ===============================
cap = cv2.VideoCapture("/dev/usb_cam")

if not cap.isOpened():
    print("❌ Error: No se pudo abrir la cámara en /dev/usb_cam.")
    print("👉 Verifica con el comando:")
    print("   ls /dev/video*")
    print("y cambia la ruta en cap = cv2.VideoCapture(...) según corresponda.")
    exit()

print("🤖 Robot imitando hasta 50 poses humanas...")
print("📸 Presiona 'q' para salir.")

# ===============================
# Funciones auxiliares
# ===============================
def extract_pose_vector(results):
    """Extrae coordenadas normalizadas de hombros, codos y muñecas"""
    if not results.pose_landmarks:
        return None
    lm = results.pose_landmarks.landmark
    vector = np.array([
        lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
        lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
        lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
        lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x
    ])
    return vector

def pose_similarity(vec1, vec2):
    """Calcula la distancia euclidiana normalizada entre dos vectores"""
    if vec1 is None or vec2 is None:
        return np.inf
    return np.linalg.norm(vec1 - vec2)

# ===============================
# Bucle principal
# ===============================
window_name = "Imitación en tiempo real"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

last_pose_id = None
last_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo leer frame de la cámara.")
        break

    # Procesar imagen con MediaPipe
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # Dibujar pose detectada
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_C>

        # Extraer vector de pose actual
        current_vec = extract_pose_vector(results)

        # Buscar la pose más parecida
        min_distance = np.inf
        best_pose_id = None
        for pid, saved_vec in human_poses.items():
            distance = pose_similarity(current_vec, np.array(saved_vec))
            if distance < min_distance:
                min_distance = distance
                best_pose_id = int(pid)

        # Si hay coincidencia buena, ejecutar
        if min_distance < DIST_THRESHOLD:
            if best_pose_id != last_pose_id or time.time() - last_time > 2:
                print(f"  Pose humana detectada: {best_pose_id} (distancia={min>
                if best_pose_id in poses:
                    print(f"🤖 Ejecutando pose del robot {best_pose_id}...")
                    motion_manager.set_servos_position(1000, poses[best_pose_id>
                    last_pose_id = best_pose_id
                    last_time = time.time()
                else:
                    print(f"⚠️ No existe la pose {best_pose_id} en el archivo Po>
        else:
            print(f"❌ Ninguna pose coincide (distancia mínima={min_distance:.3>

        # Mostrar texto en pantalla
        if best_pose_id:
            cv2.putText(frame, f"Pose {best_pose_id} (dist={min_distance:.3f})",
                        (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar imagen en ventana
    cv2.imshow(window_name, frame)

    # Salir con 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# ===============================
# Limpieza
# ===============================
cap.release()
cv2.destroyAllWindows()

