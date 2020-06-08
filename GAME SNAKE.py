# Importando as libs que vão ser utilizadas
import pygame
import random
import time

# inicialização do pygame
pygame.init()

# Definição de cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)
green_skin = (0, 197, 15)
alien = (0, 51, 90)
menu = (128, 255, 128)

# Defições da resolução
display_width = 800
display_height = 600

# Box, janela do jogo
gameDisplay = pygame.display.set_mode((display_width, display_height))

# Nome dessa janela, setagem de icone
pygame.display.set_caption("GAME SNAKE")
icon = pygame.image.load('icone_jogo.png')
pygame.display.set_icon(icon)

# Definindo os sprites/ imagens no geral
img = pygame.image.load('snakehead2.png')
img2 = pygame.image.load('snakebody2.png')
img3 = pygame.image.load('snakehead_green.png')
img4 = pygame.image.load('snakebody1_green.png')
img5 = pygame.image.load('apple_normal.png')
img6 = pygame.image.load('coca.png')
img7 = pygame.image.load('rotten_apple2.png')
art1 = pygame.image.load('snake_venom.png')
art2 = pygame.image.load('snake_green.png')
art3 = pygame.image.load('snakeicon4.png')
art4 = pygame.image.load('background.png')
art5 = pygame.image.load('winnerv3.png')
art6 = pygame.image.load('background2.jpg')
# Setagem de FPS
clock = pygame.time.Clock()

# Declarando variáveis para os funções, loop.
flag = 0
lis = [0]
cont = 0
sorte = 0
azar = 0

snakeCm = 0
respawn = time.localtime()
respawnR = time.localtime()
tempoR = 0
AppleEspessura = 30
block_size = 20
block_apple = 30
FPS = 30

direction = 'right'

# Definindo parêmetros da fonte do jogo
smallfont = pygame.font.Font("game_over.ttf", 30)
medfont = pygame.font.Font("game_over.ttf", 50)
largefont = pygame.font.Font("game_over.ttf", 100)


# Funções para a mensagem na tela, esquerda, centro, direita, render da fonte.
def text_objects(text, color, size):
    global textSurface
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0,
                      size="small"):  # msg = str, color = cor, y_displace = posição do centro em y da msg, size = tamanho
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def message_to_screen_left(msg, color, y_displace=0,
                           size="small"):  # msg = str, color = cor, y_displace = posição do centro em y da msg, size = tamanho
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 6), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def message_to_screen_right(msg, color, y_displace=0,
                            size="small"):  # msg = str, color = cor, y_displace = posição do centro em y da msg, size = tamanho
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 1.2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


# Loop de pausa
def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        gameDisplay.blit(art3, [270, 200])
        best_score(lis[-1])
        message_to_screen("PAUSADO", black, -200, 'large')
        message_to_screen('Aperte C para continuar ou Q para sair!', black, 200, 'medium')
        pygame.display.update()
        clock.tick(5)


# Função de pontuação
def score(score):
    text = medfont.render(f"Score: {score}", True, black)
    gameDisplay.blit(text, [20, 0])


# Função de maior pontuação
def best_score(score, color=black):
    text = medfont.render(f"Best Score: {score}", True, color)
    gameDisplay.blit(text, [600, 0])


# Função para validar a maior pontuação
def vali_score(cont):
    if cont > lis[0]:
        lis.pop()
        lis.append(cont)


# Função para validar a randomização da coca
def valida_coca():
    global sorte
    sorte = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return sorte


# Função para validar a randomização da rotten_Apple
def valida_rotten():
    global azar
    azar = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return azar


# Função para as randomização das coordenadas da  maçã
def randAppleGen():
    randAppleX = random.randrange(30, display_width - block_apple)
    randAppleY = random.randrange(30, display_height - block_apple)

    return randAppleX, randAppleY


# Função para a randomização das coordenadas  da coca
def randCocaGen():
    cocaX = random.randrange(30, display_width - block_apple)
    cocaY = random.randrange(30, display_height - block_apple)

    return cocaX, cocaY


# Função para a randomização das coordenadas  da coca
def randRottenApple():
    rottenX = random.randrange(30, display_width - block_apple)
    rottenY = random.randrange(30, display_height - block_apple)

    return rottenX, rottenY


# Função para setar um tempo de surface, no caso a coca.
def valida_tempo(respawn):
    global tempo
    if tempo > 60:
        tempo = 60
    if respawn.tm_sec == tempo:
        valida_coca()
    


# Função para setar um tempo de surface, no caso a rotten_apple.
def valida_tempo_rotten(respawnR):
    global tempoR
    if tempoR > 60:
        tempoR = 60
    if respawnR.tm_sec == tempoR:
        valida_rotten()
    


# Tela inicial
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        gameDisplay.blit(art3, [270, 20])
        gameDisplay.blit(img5, (750, 40))
        gameDisplay.blit(img6, (750, 80))
        gameDisplay.blit(img7, (750, 120))
        message_to_screen("BEM-VINDO AO GAME SNAKE",
                          green,
                          -15, 'large')
        message_to_screen("O objetivo do jogo é comer maças !",
                          black,
                          80, 'medium')
        message_to_screen("Quanto mais voce come, mais voce cresce !",
                          black,
                          100, 'medium')
        message_to_screen("Se voce se colidir com voce ou com as paredes, voce perde ! ",
                          black,
                          130, 'medium')
        message_to_screen("Aperte C para jogar ou Q para sair.",
                          red,
                          250, 'large')
        message_to_screen_left("CONTROLES :",
                               red,
                               -270, 'medium')
        message_to_screen_left("SETA PARA CIMA | W",
                               red,
                               -250, 'medium')
        message_to_screen_left("SETA PARA BAIXO | S",
                               red,
                               -230, 'medium')
        message_to_screen_left("SETA PARA ESQUERDA | A",
                               red,
                               -210, 'medium')
        message_to_screen_left("SETA PARA DIREITA | D",
                               red,
                               -190, 'medium')
        message_to_screen_left("PAUSAR O JOGO = P",
                               red,
                               -170, 'medium')
        message_to_screen_right('PONTUAÇAO:', black, -290, 'medium')
        message_to_screen_right('1 PONTO ----', black, -250, 'medium')
        message_to_screen_right('5 PONTOS ----', black, -210, 'medium')
        message_to_screen_right('-1 PONTO ----', black, -170, 'medium')
        pygame.display.update()
        clock.tick(15)


# Tela de dificuldade
def choose_difficulty():
    global FPS
    choose_dif = True
    while choose_dif:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    FPS = 10
                    choose_dif = False
                elif event.key == pygame.K_2:
                    FPS = 20
                    choose_dif = False
                elif event.key == pygame.K_3:
                    FPS = 30
                    choose_dif = False

        gameDisplay.fill(menu)
        message_to_screen("Escolha a dificuldade: ", black, -200, 'large')
        message_to_screen_left("Fácil", green, 100, 'large')
        message_to_screen_left('1', green, 150, 'large')
        message_to_screen('Médio', alien, 100, 'large')
        message_to_screen('2', alien, 150, 'large')
        message_to_screen_right('Difícil', red, 100, 'large')
        message_to_screen_right('3', red, 150, 'large')
        pygame.display.update()


# Tela para escolher skin
def choose_skin():
    global img, img2, flag
    choose_sk = True
    while choose_sk:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    img = img3
                    img2 = img4
                    flag = 1
                    choose_sk = False
                elif event.key == pygame.K_2:
                    img = pygame.image.load('snakehead2.png')
                    img2 = pygame.image.load('snakebody2.png')
                    flag = 0
                    choose_sk = False

        gameDisplay.fill(black)
        gameDisplay.blit(art2, [0, 300])
        gameDisplay.blit(art1, [550, 300])
        message_to_screen("Escolha sua skin: ", red, -180, 'large')
        message_to_screen_left("1", green, 200, 'large')
        message_to_screen_right('2', alien, 200, 'large')
        pygame.display.update()




def winner_loop():
    global lis, snakeCm, score
    winner = True
    while winner:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    snakeCm += 60
                    winner = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.blit(art6, (0, 0))
        gameDisplay.blit(art5, (80, 55))
        message_to_screen('Parabéns voce, zerou o jogo!'.upper(), menu, -250, 'large')
        message_to_screen('C para continuar jogando!', menu, 200, 'large')
        message_to_screen('Q para fechar o jogo!', menu, 250, 'large')
        pygame.display.update()

# Função da cobra
def snake_grow(block_size, snakeList):
    global flag, gameOver
    if direction == 'right':
        head = img
        body = img2

    if direction == 'left':
        head = pygame.transform.rotate(img, 180)
        body = pygame.transform.rotate(img2, 177)

    if direction == 'up':
        head = pygame.transform.rotate(img, 90)
        body = pygame.transform.rotate(img2, 87)
    if direction == 'down':
        head = pygame.transform.rotate(img, 270)
        body = pygame.transform.rotate(img2, 267)

    # Tratando do crescimento / diminuição
    try:
        gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    except IndexError:
        gameOver = True
    for XnY in snakeList[:-1]:
        if flag == 0:
            pygame.draw.rect(gameDisplay, alien, [XnY[0], XnY[1], block_size, block_size])
        elif flag == 1:
            pygame.draw.rect(gameDisplay, green_skin, [XnY[0], XnY[1], block_size, block_size])
        gameDisplay.blit(body, (XnY[0], XnY[1]))


# Função do jogo

def gameLoop():
    global direction, cont, lis, flag, sorte, tempo, respawn, azar, tempoR, respawnR, snakeCm
    direction = 'right'
    # Condições para o loop
    gameExit = False  # Loop do jogo em sí
    gameOver = False  # Loop de escolha

    # Começar no meio  da tela
    lead_x = display_width / 2
    lead_y = display_height / 2

    # Variavéis para o processamento do movimento e apple
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeCm = 1

    # Chamando a função para randomizar a apple/coca/rotten_apple.
    randAppleX, randAppleY = randAppleGen()
    cocaX, cocaY = randCocaGen()
    rottenX, rottenY = randRottenApple()
    valida_rotten()
    # Loop para o jogo dentro da função
    while not gameExit:  # Enquanto gameExit nao for False

        # Dentro do jogo, esse loop para saida do user ou jogar novamente
        while gameOver == True:
            # Vai imprimir essa mensagem na tela
            gameDisplay.fill(black)
            message_to_screen("Game over",
                              red,
                              -50,
                              size="large")

            message_to_screen("Aperte C para jogar novamente!", red, 50, size="medium")
            message_to_screen("Aperte 1 para trocar de dificuldade!", red, 100, size="medium")
            message_to_screen("Aperte 2 para trocar de skin!", red, 150, size="medium")
            message_to_screen("Aperte Q para sair!", red, 200, size="medium")
            best_score(lis[-1], red)
            pygame.display.update()

            # Se  a tecla for Q, a condição passa de GameExit passa a ser verdadeira, acabando com o loop ao todo e a saida desse loop, é gameOver = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        # O jogo apenas sai nesse loop
                        gameExit = True
                        gameOver = False
                    # Caso seja o event seja a tecla c, Chama o loop novamente,  em sua forma bruta, dando um reset    
                    elif event.key == pygame.K_c:
                        gameLoop()
                    elif event.key == pygame.K_1:
                        choose_skin()
                    elif event.key == pygame.K_2:
                        choose_difficulty()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    direction = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    direction = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    direction = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    direction = 'down'
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
            # Colisão com o box
            # Se ultrapassar o box, gameOver passa a ter condição True e volta la pro primeiro loop da função
            if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
                gameOver = True
                cont = 0
            if snakeCm == 0:
                gameOver = True

        if 200 <= snakeCm <= 250:
            winner_loop()

        # Entrada para o movimento do eixo x e y
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Preenchimento de cor, colocando o fundo, backgroound
        gameDisplay.blit(art4, (0, 0))


        # Desenhando a Apple e Apple

        gameDisplay.blit(img5, (randAppleX, randAppleY))
        if sorte == 1 or sorte == 5:
            gameDisplay.blit(img6, (cocaX, cocaY))
        if azar == 1:
            gameDisplay.blit(img7, (rottenX, rottenY))

        # Processamento do crescimento da cobra.
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeCm:
            snakeList.pop(0)
        # Tratando possiveis erros de index, fora da range da lista.
        try:
            if len(snakeList) > snakeCm:
                snakeList.pop()
        except IndexError:
            gameOver = True
        snake_grow(block_size, snakeList)

        # Processamento de colisão da cabeça da cobra com o corpo
        for cadasegmento in snakeList[:-1]:
            if cadasegmento == snakeHead:
                gameOver = True
                cont = 0

        score(snakeCm - 1)
        best_score(lis[-1])
        vali_score(cont)

        # Atualização do jogo, render, processamento.
        pygame.display.update()

        # Processamento em geral da maçã, tendo ligamento com a coca, pontuação, colisão e afins.
        if lead_x > randAppleX and lead_x < randAppleX + AppleEspessura or \
                lead_x + block_size > randAppleX and lead_x < randAppleX + AppleEspessura:
            if lead_y > randAppleY and lead_y < randAppleY + AppleEspessura:
                if sorte == 1 or sorte == 5:
                    sorte = 1
                elif sorte != 1 or sorte != 5:
                    valida_coca()
                elif azar == 1 or azar == 5 or azar == 7 or azar == 3:
                    azar = 1
                elif azar != 1 or azar != 5 or azar == 7 or azar != 3:
                    valida_rotten()


                randAppleX, randAppleY = randAppleGen()
                snakeCm += 1
                cont += 1
                valida_rotten()
                valida_rotten()
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleEspessura:
                if sorte == 1 or sorte == 5:
                    sorte = 1
                elif sorte != 1 or sorte != 5:
                    valida_coca()
                elif azar == 1 or azar == 5 or azar == 7 or azar == 3:
                    azar = 1
                elif azar != 1 or azar != 5 or azar != 7 or azar != 3:
                    valida_rotten()

                randAppleX, randAppleY = randAppleGen()
                snakeCm += 1
                cont += 1
                valida_rotten()

        # Processamento para a coca pontuação, colisão e afins.
        if sorte == 1 or sorte == 5:
            # Respawn é a setagem de segundos, um update de segundos enquanto está no loop
            respawn = time.localtime()
            valida_tempo(respawn)
            if lead_x > cocaX and lead_x < cocaX + AppleEspessura or \
                    lead_x + block_size > cocaX and lead_x < cocaX + AppleEspessura:
                if lead_y > cocaY and lead_y < cocaY + AppleEspessura:
                    cocaX, cocaY = randCocaGen()
                    snakeCm += 5
                    cont += 5
                    valida_coca()
                elif lead_y + block_size > cocaY and lead_y + block_size < cocaY + AppleEspessura:
                    cocaX, cocaY = randCocaGen()
                    snakeCm += 5
                    cont += 5
                    valida_coca()
        else:
            # Update de segundos, junto com o processamento de tempo, ele fica estático assim que sorte for valida.
            # Se passar o segundos forem igausi no valida_tempo, vai voltar para esse else, onde vai mudar
            # a posição da coca também
            respawn = time.localtime()
            tempo = respawn.tm_sec + 4
            cocaX, cocaY = randCocaGen()
        # Processamento Rotten Apple, pontuação, colisão e afins.

        if azar == 1 or azar == 5:
            respawnR = time.localtime()
            valida_tempo_rotten(respawnR)
            if lead_x > rottenX and lead_x < rottenX + AppleEspessura or \
                    lead_x + block_size > rottenX and lead_x < rottenX + AppleEspessura:
                if lead_y > rottenY and lead_y < rottenY + AppleEspessura:
                    rottenX, rottenY = randRottenApple()
                    snakeCm -= 1
                    valida_rotten()
                    cont -= 1

                elif lead_y + block_size > rottenY and lead_y + block_size < rottenY + AppleEspessura:
                    rottenX, rottenY = randRottenApple()
                    snakeCm -= 1
                    valida_rotten()
                    cont -= 1
        else:
            respawnR = time.localtime()
            tempoR = respawnR.tm_sec + 3
            rottenX, rottenY = randRottenApple()
        # Setando a atualização de fps
        clock.tick(FPS)

    # Finalização do pygame

    pygame.quit()
    quit()


# Chamando o jogo em ordem

game_intro()
choose_difficulty()
choose_skin()
gameLoop()
