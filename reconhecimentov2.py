import cv2
import face_recognition
import os

# Criar pastas para as classes, se não existirem
classes = ['low', 'hight', 'hard']
for c in classes:
    os.makedirs(f'database/{c}', exist_ok=True)

def cadastro():
    print("👤 Cadastro de novo usuário.")
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Não foi possível acessar a câmera.")
        return

    print("Pressione [ESPAÇO] para tirar a foto de cadastro ou [ESC] para sair.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Erro ao capturar imagem.")
            break

        cv2.imshow("Cadastro - Pressione [ESPAÇO] para capturar | [ESC] para sair", frame)

        key = cv2.waitKey(1)
        if key == 32:  # ESPAÇO
            nome_arquivo = None
            while True:
                classe = input("Digite a classe (low, hight, hard): ").strip().lower()
                if classe in classes:
                    # Salvar com nome único para evitar sobrescrever
                    nome_arquivo = f'database/{classe}/user_{len(os.listdir(f"database/{classe}")) + 1}.jpg'
                    cv2.imwrite(nome_arquivo, frame)
                    print(f"✅ Foto salva em '{nome_arquivo}'.")
                    break
                else:
                    print("Classe inválida. Tente novamente.")
            break
        elif key == 27:  # ESC
            print("🚪 Cancelado.")
            break

    cam.release()
    cv2.destroyAllWindows()

def reconhecimento():
    print("🔍 Iniciando reconhecimento facial...")

    # Carregar todas as imagens e encodings
    encodings = []
    labels = []

    for classe in classes:
        path = f'database/{classe}'
        for arquivo in os.listdir(path):
            if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(path, arquivo)
                imagem = face_recognition.load_image_file(img_path)
                enc = face_recognition.face_encodings(imagem)
                if enc:
                    encodings.append(enc[0])
                    labels.append(classe)
                else:
                    print(f"⚠️ Nenhum rosto encontrado em {img_path}, pulando.")

    if not encodings:
        print("❌ Nenhuma imagem de cadastro encontrada. Faça um cadastro primeiro.")
        return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Não foi possível acessar a câmera.")
        return

    print("Pressione [ESPAÇO] para capturar a imagem para reconhecimento, [ESC] para sair.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("❌ Erro ao capturar imagem.")
            break

        cv2.imshow("Reconhecimento - Pressione [ESPAÇO] para capturar | [ESC] para sair", frame)

        key = cv2.waitKey(1)
        if key == 32:  # ESPAÇO
            cv2.imwrite("temp.jpg", frame)
            imagem_capturada = face_recognition.load_image_file("temp.jpg")
            enc_capturada = face_recognition.face_encodings(imagem_capturada)

            if not enc_capturada:
                print("❌ Nenhum rosto detectado na foto capturada.")
                continue

            rosto_capturado = enc_capturada[0]

            resultados = face_recognition.compare_faces(encodings, rosto_capturado)
            distancias = face_recognition.face_distance(encodings, rosto_capturado)

            if True in resultados:
                melhor_match_index = distancias.argmin()
                classe_reconhecida = labels[melhor_match_index]
                print(f"🎉 Pessoa reconhecida na classe: {classe_reconhecida.upper()}")
            else:
                print("⚠️ Pessoa não reconhecida.")

        elif key == 27:  # ESC
            print("🚪 Encerrando reconhecimento.")
            break

    cam.release()
    cv2.destroyAllWindows()

def main():
    while True:
        print("\n--- MENU ---")
        print("1 - Cadastro")
        print("2 - Reconhecimento")
        print("3 - Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            cadastro()
        elif escolha == '2':
            reconhecimento()
        elif escolha == '3':
            print("Encerrando programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()