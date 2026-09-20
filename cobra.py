from tkinter import *  # importa tudo do tkinter (Tk, Canvas, Label, etc.) sem precisar escrever tkinter.Tk(), só Tk()
import random  # usado pra sortear a posição da comida

# --- configurações do jogo (constantes) ---
game_width = 1000       # largura do canvas/jogo em pixels
game_height = 600       # altura do canvas/jogo em pixels
speed = 85               # intervalo em milissegundos entre cada "passo" do jogo (menor = mais rápido)
tamanho_espaco = 50      # tamanho de cada célula do grid (cobra e comida se movem de 50 em 50 pixels)
parte_corpo = 3          # quantidade inicial de segmentos do corpo da cobra
snake_cor = '#00FF00'    # cor da cobra (verde)
cor_food = '#FF0000'     # cor da comida (vermelho)
background = '#000000'   # cor de fundo do canvas (preto)

class Snake:
    def __init__(self):
        self.corpo_size = parte_corpo      # guarda o tamanho atual do corpo
        self.coordenadas = []              # lista de posições [x, y] de cada parte do corpo
        self.cubos = []                    # lista dos IDs dos retângulos desenhados no canvas

        # cria as coordenadas iniciais (todas em 0,0, por enquanto sobrepostas)
        for i in range(0, parte_corpo):
            self.coordenadas.append([0, 0])

        # desenha um quadrado no canvas pra cada parte do corpo e guarda o ID retornado
        for x, y in self.coordenadas:
            cubo = canvas.create_rectangle(x, y, x + tamanho_espaco, y + tamanho_espaco, fill=snake_cor, tags='cobra')
            self.cubos.append(cubo)  # sem guardar o ID, não teria como apagar/mover esse quadrado depois

class Food:
    def __init__(self):
        # sorteia uma posição x,y alinhada ao grid (múltiplo de tamanho_espaco)
        x = random.randint(0, (game_width//tamanho_espaco)-1) * tamanho_espaco
        y = random.randint(0, (game_height//tamanho_espaco)-1) * tamanho_espaco

        self.coordenadas = [x, y]  # guarda a posição da comida

        # desenha um círculo (oval) no canvas na posição sorteada
        canvas.create_oval(x, y, x + tamanho_espaco, y + tamanho_espaco, fill=cor_food, tags='food') # as coordenadas são o tamanho da imagem

def proximo_turno(snake, food):
    # pega a posição atual da cabeça (primeiro elemento da lista)
    x, y = snake.coordenadas[0]

    # move a posição da cabeça de acordo com a direção atual
    if direcao == 'up':
        y -= tamanho_espaco
    elif direcao == 'down':
        y += tamanho_espaco
    elif direcao == 'right':
        x += tamanho_espaco
    elif direcao == 'left':
        x -= tamanho_espaco

    # insere a nova posição no INÍCIO da lista → ela vira a nova cabeça
    snake.coordenadas.insert(0, (x, y))

    # desenha o novo quadrado (a nova cabeça) no canvas
    cubo = canvas.create_rectangle(x, y, x + tamanho_espaco, y + tamanho_espaco, fill=snake_cor)
    snake.cubos.insert(0, cubo)  # guarda o ID desse novo quadrado também no início da lista

    # verifica se a cabeça está na mesma posição da comida
    if x == food.coordenadas[0] and y == food.coordenadas[1]:
        global score  # necessário pra poder alterar a variável score, que foi criada fora da função
        score += 1
        Label.config(text=f'Score {score}')  # atualiza o texto do placar na tela

        canvas.delete('food')  # apaga a comida antiga do canvas
        food = Food()          # cria uma nova comida em posição aleatória
        # repare que aqui NÃO se apaga o último segmento do corpo → é assim que a cobra "cresce"

    else:
        # se não comeu, remove o último segmento do corpo (rabo), simulando movimento sem crescer
        del snake.coordenadas[-1]
        canvas.delete(snake.cubos[-1])  # apaga o quadrado do canvas
        del snake.cubos[-1]             # remove o ID da lista

    # verifica se bateu na parede ou em si mesma
    if check_colisao(snake):
        game_over()
        return  # sai da função pra não agendar uma próxima chamada (encerra o "loop")

    # agenda a próxima execução dessa mesma função daqui a `speed` milissegundos
    window.after(speed, proximo_turno, snake, food)

def mudar_direcao(nova_direcao):
    global direcao  # necessário pra alterar a variável direcao, criada fora da função

    # cada bloco impede que a cobra vire 180° sobre si mesma (ex: indo pra direita, não pode ir direto pra esquerda)
    if nova_direcao == 'left':
        if direcao != 'right':
            direcao = nova_direcao
    elif nova_direcao == 'right':
        if direcao != 'left':
            direcao = nova_direcao
    if nova_direcao == 'up':
        if direcao != 'down':
            direcao = nova_direcao
    elif nova_direcao == 'down':
        if direcao != 'up':
            direcao = nova_direcao

def check_colisao(snake):
    x, y = snake.coordenadas[0]  # posição atual da cabeça

    # bateu na parede esquerda ou direita
    if x < 0 or x >= game_width:
        return True
    # bateu na parede de cima ou de baixo
    elif y < 0 or y >= game_height:
        return True

    # verifica se a cabeça colidiu com alguma parte do próprio corpo
    # (começa do índice 1 porque o índice 0 é a própria cabeça)
    for corpo in snake.coordenadas[1:]:
        if x == corpo[0] and y == corpo[1]:
            return True

    return False  # nenhuma colisão

def game_over():
    canvas.delete(ALL)  # apaga tudo que estava desenhado no canvas
    # escreve "GAME OVER" no centro do canvas
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text='GAME OVER', fill='red', tags='gameover')

# --- montagem da janela ---
window = Tk()                       # cria a janela principal
window.title('Snake')               # define o título da janela
window.resizable(False, False)      # impede redimensionar a janela (largura, altura)

score = 0            # placar inicial
direcao = 'down'     # direção inicial da cobra

# cria o texto do placar e o exibe na janela
Label = Label(window, text=f'score {score}', font=('consolas', 40))
Label.pack()  # sem .pack(), o widget existe no código mas não aparece na tela

# cria a área de desenho do jogo e a exibe
canvas = Canvas(window, bg=background, height=game_height, width=game_width)
canvas.pack()

window.update()  # força o tkinter a processar a janela agora, senão winfo_width() abaixo retornaria 0

# lê as dimensões reais da janela e da tela do monitor
window_width = window.winfo_width()
window_height = window.winfo_height()
width_tela = window.winfo_screenwidth()
height_tela = window.winfo_screenheight()

# calcula onde posicionar a janela (aqui está fixo em 0,0 — não centraliza de fato)
x = int(window_width/2) - int(window_width/2)
y = int(window_height/2) - int(window_height/2)

window.geometry(f'{window_width}x{window_height}+{x}+{y}')  # aplica tamanho e posição da janela

# associa cada tecla de seta a uma chamada de mudar_direcao
# lambda event: ... existe pq o tkinter sempre passa um "event" pra função do bind, e aqui ele é ignorado
window.bind('<Left>', lambda event: mudar_direcao('left'))
window.bind('<Right>', lambda event: mudar_direcao('right'))
window.bind('<Down>', lambda event: mudar_direcao('down'))
window.bind('<Up>', lambda event: mudar_direcao('up'))

snake = Snake()  # cria a cobra
food = Food()    # cria a primeira comida

proximo_turno(snake, food)  # inicia o "loop" do jogo (que se re-agenda sozinho via window.after)

window.mainloop()  # inicia o loop de eventos do tkinter — mantém a janela aberta e reagindo a tudo