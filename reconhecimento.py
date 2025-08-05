import cv2
import face_recognition
import os

# === 1. CAPTURAR A IMAGEM DE REFERÊNCIA COMO "joao.jpg" ===
print("👤 Vamos tirar a foto de referência (joao.jpg)...")
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("❌ Não foi possível acessar a câmera.")
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        print("❌ Erro ao capturar a imagem de referência.")
        break

    cv2.imshow("Imagem de Referência - Pressione [ESPAÇO] para capturar | [ESC] para sair", frame)

    key = cv2.waitKey(1)
    if key == 32:  # ESPAÇO
        cv2.imwrite("joao.jpg", frame)
        print("✅ Imagem de referência salva como 'joao.jpg'")
        break
    elif key == 27:  # ESC
        print("🚪 Encerrando script.")
        cam.release()
        cv2.destroyAllWindows()
        exit()

cam.release()
cv2.destroyAllWindows()

# === 2. CARREGAR E ENCODAR IMAGEM DE REFERÊNCIA ===
if not os.path.exists("joao.jpg"):
    print("❌ A imagem 'joao.jpg' não foi encontrada.")
    exit()

imagem_referencia = face_recognition.load_image_file("joao.jpg")
enc_ref = face_recognition.face_encodings(imagem_referencia)
if not enc_ref:
    print("❌ Nenhum rosto encontrado na imagem de referência.")
    exit()

rosto_referencia = enc_ref[0]

# === 3. CAPTURAR NOVA IMAGEM PARA VERIFICAÇÃO ===
print("📸 Agora vamos capturar uma nova imagem para verificar se é a mesma pessoa...")

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("❌ Não foi possível acessar a câmera.")
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        print("❌ Erro ao capturar imagem.")
        break

    cv2.imshow("Verificação - Pressione [ESPAÇO] para capturar | [ESC] para sair", frame)

    key = cv2.waitKey(1)
    if key == 32:  # ESPAÇO
        cv2.imwrite("captura.jpg", frame)
        print("✅ Foto de verificação salva como 'captura.jpg'")
        break
    elif key == 27:  # ESC
        print("🚪 Encerrando script.")
        cam.release()
        cv2.destroyAllWindows()
        exit()

cam.release()
cv2.destroyAllWindows()

# === 4. COMPARAÇÃO FACIAL ===
imagem_nova = face_recognition.load_image_file("captura.jpg")
enc_nova = face_recognition.face_encodings(imagem_nova)

if not enc_nova:
    print("❌ Nenhum rosto detectado na imagem de verificação.")
    exit()

rosto_novo = enc_nova[0]
resultado = face_recognition.compare_faces([rosto_referencia], rosto_novo)

# === 5. RESULTADO ===
if resultado[0]:
    print("🎉 Verificação bem-sucedida: é a mesma pessoa! ✅")
else:
    print("⚠️ Verificação falhou: NÃO é a mesma pessoa! ❌")   