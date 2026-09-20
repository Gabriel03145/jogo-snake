from tkinter import *
import random

game_width = 1000
game_height = 600
speed = 85
tamanho_espaco = 50
parte_corpo = 3
snake_cor = '#00FF00'
cor_food = '#FF0000'
background = '#000000'

class Snake:
    def __init__(self):
        self.corpo_size = parte_corpo
        self.coordenadas = []
        self.cubos = []

        for i in range(0, parte_corpo):
            self.coordenadas.append([0, 0])

        for x, y in self.coordenadas:
            cubo = canvas.create_rectangle(x, y, x + tamanho_espaco, y + tamanho_espaco, fill=snake_cor, tags='cobra')
            self.cubos.append(cubo)

class Food:
    def __init__(self):

        x = random.randint(0, (game_width//tamanho_espaco)-1) * tamanho_espaco
        y = random.randint(0, (game_height//tamanho_espaco)-1) * tamanho_espaco

        self.coordenadas = [x, y]

        canvas.create_oval(x, y, x + tamanho_espaco, y + tamanho_espaco, fill=cor_food, tags='food')

def proximo_turno(snake, food):
    x, y = snake.coordenadas[0]

    if direcao == 'up':
        y -= tamanho_espaco

    elif direcao == 'down':
        y += tamanho_espaco

    elif direcao == 'right':
        x += tamanho_espaco

    elif direcao == 'left':
        x -= tamanho_espaco

    snake.coordenadas.insert(0, (x, y))

    cubo = canvas.create_rectangle(x, y, x + tamanho_espaco, y + tamanho_espaco, fill=snake_cor)

    snake.cubos.insert(0, cubo)

    if x == food.coordenadas[0] and y == food.coordenadas[1]:

        global score

        score += 1

        Label.config(text=f'Score {score}')

        canvas.delete('food')

        food = Food()

    else:

        del  snake.coordenadas[-1]

        canvas.delete(snake.cubos[-1])

        del snake.cubos[-1]

    if check_colisao(snake):
        game_over()
        return

    window.after(speed, proximo_turno, snake, food)

def mudar_direcao(nova_direcao):
    global direcao

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

    x, y = snake.coordenadas[0]

    if x < 0 or x >= game_width:
        return True
    
    elif y < 0 or y >= game_height:
        return True

    for corpo in snake.coordenadas[1:]:
        if x == corpo[0] and y == corpo[1]:
            return True

    return False

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, 
                       font=('consolas', 70), text='GAME OVER', fill='red', tags='gameover')
    

window = Tk()
window.title('Snake')
window.resizable(False, False)

score = 0
direcao = 'down'

Label = Label(window, text=f'score {score}', font=('consolas', 40))
Label.pack()

canvas = Canvas(window, bg=background, height=game_height, width=game_width)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
width_tela = window.winfo_screenwidth()
height_tela = window.winfo_screenheight()

x = int(window_width/2) - int(window_width/2)
y = int(window_height/2) - int(window_height/2)

window.geometry(f'{window_width}x{window_height}+{x}+{y}')

window.bind('<Left>', lambda event: mudar_direcao('left'))
window.bind('<Right>', lambda event: mudar_direcao('right'))
window.bind('<Down>', lambda event: mudar_direcao('down'))
window.bind('<Up>', lambda event: mudar_direcao('up'))

snake = Snake()
food = Food()

proximo_turno(snake, food)

window.mainloop()