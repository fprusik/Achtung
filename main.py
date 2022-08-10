import pygame
import random
import math
import server
from threading import Thread

pygame.init()
dis_width = 1000
dis_height = 800
dis = pygame.display.set_mode((dis_width, dis_height), pygame.DOUBLEBUF)

pygame.display.set_caption('Achtung die Kurve')
# main_icon = pygame.image.load('head.jpg')
# pygame.display.set_icon(main_icon)

game_over = False
blue = (54, 180, 240, 255)
cgrey = (59, 68, 72, 255)
cred = (222, 14, 68, 255)
rad = 1
players = []

clock = pygame.time.Clock()
dis.fill(cgrey)
dis.blit(pygame.font.SysFont("bahnschrift", 25).render(' Click S to start', True, cred), [dis_width/2, dis_height/2])
pygame.display.update()
stop_threads = False


# Splash screen
while True: 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
    key_input = pygame.key.get_pressed()
    #print(key_input)
    if key_input[pygame.K_s]:
        break

class Player():
    def __init__(self, color, name):
        self.player_move = 2
        self.player_speed = 20 #original: 60
        self.playerx = int(random.randint(dis_width/10, dis_width*0.9))
        self.playery = int(random.randint(dis_height/10, dis_height*0.9))
        self.prev_playerx = 0
        self.prev_playery = 0
        self.color = color
        self.name = name
        # self.alpha = math.pi/4
        # self.beta = math.pi/4
        #self.alpha = math.pi/random.randint(0, 360)
        self.alpha = math.pi * random.randrange(0, 2000)/1000
        print(self.alpha)
        #self.beta = math.pi/random.randint(0, 360)
        self.x_change = random.randint(0, 6) - 3
        self.y_change = random.randint(0, 6) - 3
        # x_change = math.pi/random.randint(0, 180)
        # y_change = math.pi/random.randint(0, 180)
        self.player_line = []
        self.player_line.append([self.playerx, self.playery])
        self.prev_x = None
        self.prev_y = None
    def __str__(self) -> str:
        return self.name

    def __del__(self):
        pass

def newgame():
    player1 = Player(blue, 'Filip')
    player2 = Player(cred, 'Damian')
    players.append(player1)
    players.append(player2)
    #t = Thread(target=server.listeningGuest, args=(players[0].alpha))
    dis.fill(cgrey)
    pygame.display.update()
    gameLoop()

def nextmove(player):
    player.playerx += round(math.sin(player.alpha) * player.player_move, 1)
    player.playery += round(math.cos(player.alpha) * player.player_move, 1)
    player.playerx = round(player.playerx, 1)
    player.playery = round(player.playery, 1)
    if player.playerx >= dis_width or player.playerx < 0 or player.playery >= dis_height or player.playery < 0:
        quitgame(player)
    for j in range(len(players)):
        for i in range(len(players[j].player_line)):
            if abs(players[j].player_line[i][0]-player.playerx)<=1 and abs(players[j].player_line[i][1]-player.playery)<=1:
                print(str(player) + ' Catched')
                quitgame(player)

def quitgame(loser):
    #global stop_threads
    print(str(loser) + ' lose the game')
    game_over = True
    dis.fill(cgrey)
    dis.blit(pygame.font.SysFont("bahnschrift", 25).render(str(loser) + ' lose the game', True, cred), [dis_width/6, dis_height/6])
    pygame.display.update()
    server.stopThread()
    t.join()
    while game_over:
        for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print('Try to excape')
                        #t.stop()
                        # server.stopThread()
                        #stop_threads = True
                        # t.join()
                        #print('After join()')
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        game_over = False
                        print(len(players))
                        for i in range(len(players)): # delete all Players' objects in list and then clear the list
                            players[i] = None
                        players.clear()
                        newgame() 
    
def paint(gamer):
    # global prev_x
    # global prev_y
    coorx = gamer.playerx
    coory = gamer.playery
    #print(round(coorx, 1))
    gamer.player_line.append([coorx, coory])
    
    pygame.draw.circle(dis, gamer.color, (coorx, coory), rad)
    #pygame.draw.rect(dis, blue, (playerx, playery, 2, 2))
    if gamer.prev_x is not None:
        diff_x = coorx - gamer.prev_x
        diff_y = coory - gamer.prev_y
        steps = int(max(abs(diff_x), abs(diff_y)))
        if steps > 0:
            dx = diff_x/steps
            dy = diff_y/steps
            for _ in range(steps):
                gamer.prev_x += dx
                gamer.prev_y += dy
                pygame.draw.circle(dis, gamer.color, (round(gamer.prev_x), round(gamer.prev_y)), rad)       
                #pygame.draw.rect(dis, blue, (round(prev_x), round(prev_y), 2, 2))   
    gamer.prev_x = coorx
    gamer.prev_y = coory

def gameLoop():
    global game_over
    
    t.start()
    print('STARTS')
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over = True
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_LEFT]: 
            players[0].alpha += math.pi/45
        if key_input[pygame.K_RIGHT]:
            players[0].alpha -= math.pi/45
        if key_input[pygame.K_a]: 
            players[1].alpha += math.pi/45
        if key_input[pygame.K_s]:
            players[1].alpha -= math.pi/45
        if server.moveL == True:
            players[1].alpha += math.pi/45
            server.moveL = False
            print('move L made')
        if server.moveR == True:
            players[1].alpha -= math.pi/45
            server.moveR = False
            print('move R made')
        nextmove(players[0])
        nextmove(players[1])
        
        paint(players[0])
        paint(players[1])
       
        pygame.display.update()

        clock.tick(players[0].player_speed)


#t = Thread(target=just4test)
t = Thread(target=server.listeningGuest)
newgame()
#gameLoop()
quitgame()