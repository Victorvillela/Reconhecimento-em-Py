👤 Face Recognition App (Python)

Aplicação desktop em Python para cadastro e reconhecimento facial utilizando webcam, com classificação de rostos em níveis (low, hight, hard). O sistema conta com interface gráfica simples desenvolvida em Tkinter e reconhecimento facial baseado em embeddings.

🚀 Funcionalidades

📷 Captura de imagem via webcam

📝 Cadastro de rostos por classe (low, hight, hard)

🧠 Reconhecimento facial automático

🗂️ Organização das imagens por diretórios

🖥️ Interface gráfica intuitiva (Tkinter)

⚠️ Tratamento básico de erros (câmera, rosto não detectado, base vazia)

🛠️ Tecnologias Utilizadas

Python 3.8+

OpenCV

face_recognition

NumPy

Pillow (PIL)

Tkinter

📂 Estrutura do Projeto
.
├── main.py
├── database/
│   ├── low/
│   ├── hight/
│   └── hard/
└── README.md

📦 Instalação

Instale as dependências necessárias:

pip install opencv-python face_recognition numpy pillow


⚠️ A biblioteca face_recognition depende do dlib. Em alguns sistemas pode ser necessário instalar uma versão compatível manualmente.

▶️ Como Executar
python main.py


Ao iniciar, o menu principal exibirá as opções:

Cadastro

Reconhecimento

Sair

📝 Cadastro Facial

Selecione Cadastro

Capture a imagem pela webcam

Informe a classe desejada (low, hight ou hard)

A imagem será salva automaticamente no banco de dados

🔍 Reconhecimento Facial

Selecione Reconhecimento

Capture uma imagem

O sistema compara o rosto com a base cadastrada

O resultado é exibido em tela

⚙️ Funcionamento

Utiliza face encodings para representar rostos

Compara rostos usando distância euclidiana

Seleciona o melhor match com menor distância

📌 Observações

Utilize boa iluminação para melhores resultados

Cada imagem deve conter apenas um rosto

A câmera padrão usada é VideoCapture(0)

🚧 Melhorias Futuras

Reconhecimento em tempo real

Persistência de encodings em arquivo

Identificação visual do rosto na tela

Ajuste de threshold de reconhecimento

Suporte a múltiplas câmeras

👨‍💻 Autor

Victor Villela
Projeto desenvolvido para estudos e demonstração de Visão Computacional e Reconhecimento Facial em Python.
