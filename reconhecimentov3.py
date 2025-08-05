import cv2
import face_recognition
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import numpy as np

# Definir pasta_base com fallback seguro para ambientes sem __file__
try:
    pasta_base = os.path.dirname(os.path.abspath(__file__))
except NameError:
    pasta_base = os.getcwd()

# Criar pasta database e subpastas para as classes
database_path = os.path.join(pasta_base, 'database')
os.makedirs(database_path, exist_ok=True)

classes = ['low', 'hight', 'hard']

for c in classes:
    os.makedirs(os.path.join(database_path, c), exist_ok=True)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconhecimento Facial")
        self.root.geometry("700x600")

        self.cap = None
        self.frame = None
        self.video_label = None
        self.capturando = False

        self.encodings = []
        self.labels = []

        self.mostrar_menu()

    def mostrar_menu(self):
        self.limpar_tela()
        self.label = tk.Label(self.root, text="Escolha uma opção:", font=("Arial", 16))
        self.label.pack(pady=10)

        self.btn_cadastro = tk.Button(self.root, text="Cadastro", command=self.iniciar_cadastro)
        self.btn_cadastro.pack(fill='x', padx=100, pady=5)

        self.btn_reconhecimento = tk.Button(self.root, text="Reconhecimento", command=self.iniciar_reconhecimento)
        self.btn_reconhecimento.pack(fill='x', padx=100, pady=5)

        self.btn_sair = tk.Button(self.root, text="Sair", command=self.root.quit)
        self.btn_sair.pack(fill='x', padx=100, pady=5)

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def abrir_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a câmera.")
            return False
        return True

    def fechar_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None

    def mostrar_video(self):
        if not self.capturando:
            return
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(15, self.mostrar_video)

    def iniciar_cadastro(self):
        if not self.abrir_camera():
            return
        self.capturando = True

        self.limpar_tela()

        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        btn_capture = tk.Button(self.root, text="Capturar Foto", command=self.capturar_cadastro)
        btn_capture.pack(pady=10)

        btn_cancel = tk.Button(self.root, text="Cancelar", command=self.cancelar)
        btn_cancel.pack()

        self.mostrar_video()

    def capturar_cadastro(self):
        if not self.capturando:
            return
        self.capturando = False  # Para o loop de vídeo
        self.root.after(100, self._processar_captura_cadastro)

    def _processar_captura_cadastro(self):
        frame = self.frame
        if frame is None:
            messagebox.showerror("Erro", "Nenhum frame capturado.")
            self.fechar_camera()
            self.mostrar_menu()
            return

        classe = simpledialog.askstring("Classe", "Digite a classe (low, hight, hard):")
        if not classe:
            messagebox.showinfo("Cancelado", "Cadastro cancelado.")
            self.fechar_camera()
            self.mostrar_menu()
            return
        classe = classe.lower()
        if classe not in classes:
            messagebox.showerror("Erro", "Classe inválida.")
            self.capturando = True
            self.mostrar_video()
            return

        pasta = os.path.join(database_path, classe)
        nome_arquivo = f"user_{len(os.listdir(pasta)) + 1}.jpg"
        caminho = os.path.join(pasta, nome_arquivo)
        cv2.imwrite(caminho, frame)
        messagebox.showinfo("Sucesso", f"Foto salva em {caminho}")
        self.fechar_camera()
        self.mostrar_menu()

    def cancelar(self):
        self.capturando = False
        self.fechar_camera()
        self.mostrar_menu()

    def iniciar_reconhecimento(self):
        if not self.abrir_camera():
            return
        self.capturando = True

        self.limpar_tela()

        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        btn_capture = tk.Button(self.root, text="Capturar Foto", command=self.capturar_reconhecimento)
        btn_capture.pack(pady=10)

        btn_cancel = tk.Button(self.root, text="Cancelar", command=self.cancelar)
        btn_cancel.pack()

        # Carregar imagens e encodings
        self.encodings = []
        self.labels = []

        for classe in classes:
            path = os.path.join(database_path, classe)
            for arquivo in os.listdir(path):
                if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(path, arquivo)
                    imagem = face_recognition.load_image_file(img_path)
                    enc = face_recognition.face_encodings(imagem)
                    if enc:
                        self.encodings.append(enc[0])
                        self.labels.append(classe)

        if not self.encodings:
            messagebox.showwarning("Aviso", "Nenhuma imagem cadastrada encontrada. Faça um cadastro primeiro.")
            self.fechar_camera()
            self.mostrar_menu()
            return

        self.mostrar_video()

    def capturar_reconhecimento(self):
        if not self.capturando:
            return
        self.capturando = False  # Para o loop de vídeo
        self.root.after(100, self._processar_captura_reconhecimento)

    def _processar_captura_reconhecimento(self):
        frame = self.frame
        if frame is None:
            messagebox.showerror("Erro", "Nenhum frame capturado.")
            self.fechar_camera()
            self.mostrar_menu()
            return

        cv2.imwrite("temp.jpg", frame)
        imagem_capturada = face_recognition.load_image_file("temp.jpg")
        enc_capturada = face_recognition.face_encodings(imagem_capturada)

        if not enc_capturada:
            messagebox.showwarning("Aviso", "Nenhum rosto detectado na foto capturada.")
            self.fechar_camera()
            self.mostrar_menu()
            return

        rosto_capturado = enc_capturada[0]

        resultados = face_recognition.compare_faces(self.encodings, rosto_capturado)
        distancias = face_recognition.face_distance(self.encodings, rosto_capturado)

        if True in resultados:
            melhor_match_index = np.argmin(distancias)
            classe_reconhecida = self.labels[melhor_match_index]
            messagebox.showinfo("Reconhecimento", f"Pessoa reconhecida na classe: {classe_reconhecida.upper()}")
        else:
            messagebox.showinfo("Reconhecimento", "Pessoa não reconhecida.")

        self.fechar_camera()
        self.mostrar_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
