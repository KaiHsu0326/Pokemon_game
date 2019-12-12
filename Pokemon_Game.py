import pygame, sys, os, random, time
from Class.pokemon import POKEDEX, Pokemon, Battle, Pokedex
from Class.map import Map, X_RANGE, Y_RANGE, MAPS
from Class.bag import Bag

class Player():
    def __init__(self,pos):
        self.pos = pos

class Exit():
    def __init__(self,pos):
        self.pos = pos

class Grass():
    def __init__(self,pos):
        self.pos = pos

dir_path = os.path.dirname(os.path.abspath(__file__))

pygame.init()

IMAGES = {'title': pygame.image.load(dir_path+'/image/pokemon-logo.png'),
          'cover': pygame.image.load(dir_path+'/image/cover.png'),
          'sea': pygame.image.load(dir_path+'/image/sea.png'),
          'choose_poke_bg': pygame.image.load(dir_path+'/image/choose_poke_bg.png'),
          'arrow_up': pygame.image.load(dir_path+'/image/arrow_up.png')}

ALL_MAPS_DATA = ['']
for m in MAPS : ALL_MAPS_DATA.append(m)

def set_state(x,y,all_exit):
    player = Player((x,y))
    exits = []   
    for e in all_exit:exits.append(Exit(e))
    return player, exits

def change_map(move_to) :
    if player.pos in current_map.exits and current_map.trigger_dir[current_map.exits[player.pos]] == move_to :
        return True
    return False

def draw_begin_cover() :
    BASE_SURF.fill((46, 46, 46)) 
    BASE_SURF.blit(pygame.transform.scale(IMAGES['cover'], (X_RANGE,Y_RANGE)),(30,0))
    image = pygame.transform.scale(IMAGES['title'], (int(X_RANGE/2.2),int(Y_RANGE/2.2)))
    rect = image.get_rect()
    rect.center = (X_RANGE//4.2,Y_RANGE//2.2)
    BASE_SURF.blit(image,rect)
    textSurfaceObj = fontObj.render('\'z\' to start the game', True, (255,255,255))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (X_RANGE//2, 550)
    BASE_SURF.blit(textSurfaceObj, textRectObj)

def current_situation():
    global sit_num
    situation = {1:'begin', 2:'choose_poke', 3:'walking', 4:'battle', 5:'bag', 6:'pokedex', 7:'battle_round', 8:'other_situation'}
    return situation[sit_num]


def draw_choose_begin_pokemon(poke, move_to) :
    global choose
    BASE_SURF.blit(pygame.transform.scale(IMAGES['choose_poke_bg'], (X_RANGE,Y_RANGE)),(0,0))
    textSurfaceObj = fontObj.render('\'z\' to choose your Pokemon', True, (0,0,0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (X_RANGE//2, 50)
    BASE_SURF.blit(textSurfaceObj, textRectObj)

    index = 0
    while index < len(poke): 
        p = pygame.transform.scale(poke[index].image_front[poke[index].get_frame_num('front')], \
            (int(poke[index].f_size[0]*2.5), int(poke[index].f_size[1]*2.5)))
        rect = p.get_rect()
        if index is 0:
            space_rect = pygame.Rect((130,300, 140, 140))
            rect.midbottom = space_rect.bottomleft
        elif index is 1:
            space_rect = pygame.Rect((330,300, 140, 140))
            rect.midbottom = space_rect.midbottom
        elif index is 2:
            space_rect = pygame.Rect((530,300, 140, 140))
            rect.midbottom = space_rect.bottomright
        BASE_SURF.blit(p, rect)
        index += 1

    offset = 0
    if move_to is 'LEFT' and choose > 0 : offset = -1
    elif move_to is 'RIGHT' and choose < 2: offset = 1
    choose += offset

    arrow = pygame.transform.scale(IMAGES['arrow_up'], (50,50))
    rect = arrow.get_rect()
    if choose is 0 : 
        space_rect = pygame.Rect((130,400, 140, 140))
        rect.midbottom = space_rect.bottomleft
    elif choose is 1 : 
        space_rect = pygame.Rect((330,400, 140, 140))
        rect.midbottom = space_rect.midbottom
    elif choose is 2 : 
        space_rect = pygame.Rect((530,400, 140, 140))
        rect.midbottom = space_rect.bottomright  
    BASE_SURF.blit(arrow, rect)

test_list = [Pokemon(1,5),Pokemon(7,5),Pokemon(4,5),Pokemon(2,5),Pokemon(3,5),Pokemon(5,5)]
opp_attack = timer =  pokedex = 0
prior_sit_num = sit_num = choose = 1
choose_inside = pos_move = False
BASE_SURF = pygame.display.set_mode((X_RANGE, Y_RANGE))
fontObj = pygame.font.Font('freesansbold.ttf', 35)
current_map = Map(1,-1)
bag = Bag()
player,exits= set_state(current_map.x_screen, current_map.y_screen, current_map.exits)
init_p = [Pokemon(1,5),Pokemon(7,5),Pokemon(4,5)]

while True:
    
    move_to = None
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT :
                if current_situation() is not 'begin': move_to = 'LEFT'
            if e.key == pygame.K_RIGHT:
                if current_situation() is not 'begin': move_to = 'RIGHT'
            if e.key == pygame.K_UP:
                if current_situation() is not 'begin': move_to = 'UP'
            if e.key == pygame.K_DOWN:
                if current_situation() is not 'begin': move_to = 'DOWN'

            if e.key == pygame.K_b and current_situation() is 'walking':
                sit_num = 5

            if e.key == pygame.K_t and current_situation() is 'walking': # Transaction 
                bag.transaction()

            if e.key == pygame.K_x :
                if (current_situation() is 'bag' or current_situation() is 'pokedex') :
                    sit_num = prior_sit_num
                elif choose_inside: choose_inside = False

            if e.key == pygame.K_z :
                if current_situation() is 'begin' :
                    sit_num = 2
                elif current_situation() is 'choose_poke' :
                    pokedex = Pokedex(init_p[choose])
                    sit_num = prior_sit_num = 3
                elif current_situation() is 'battle':
                    if choose_inside: 
                        sit_num = 7
                        timer = 0
                        opp_attack = random.randint(0,3)
                        
                    elif choose is 0 and not choose_inside:choose_inside = True
                    elif choose is 1:sit_num = 5
                    elif choose is 2:sit_num = 6
                    elif choose is 3:sit_num = 3

                elif current_situation() is 'bag': 
                    if not choose_inside: choose_inside = True
                    else : choose_inside: bag.use_props()
    
    if current_situation() is 'begin' : draw_begin_cover()
 
    elif current_situation() is 'choose_poke' :
        draw_choose_begin_pokemon(init_p, move_to)

    elif current_situation() is 'battle_round' :
        if not battle.have_left_move_num(choose):
            sit_num = 4
            continue
       
        bat_surf, sit_num = battle.battle_round_animate(timer, choose, opp_attack)
        BASE_SURF.blit(bat_surf, (0,0))
        timer += 1
        if sit_num is 8: timer = -50
        elif sit_num is 4: choose_inside = False

    elif current_situation() is 'battle':       
        bat_surf, choose = battle.draw_battle(move_to, choose_inside)
        BASE_SURF.blit(bat_surf, (0,0))

    elif current_situation() is 'bag': 
        bag_surf = bag.draw_bag(move_to, choose_inside, test_list)
        BASE_SURF.blit(bag_surf, (0,0))

    elif current_situation() is 'pokedex' :
        pokedex_surf = pokedex.draw_pokedex(move_to)
        BASE_SURF.blit(pokedex_surf, (0,0))

    elif current_situation() is 'other_situation' :
        if choose_inside:
            bonus = 0
            if battle.has_level_up: bonus = 50
            if timer < 0:
                bat_surf = battle.draw_battle_over(0, 0)
            elif 0 < timer and timer < 200+bonus:
                if battle.my_pokemon_die():
                    bat_surf = battle.draw_battle_over(timer, 0)
                else : 
                    bat_surf = battle.draw_battle_over(0, timer)
                    if timer is 149 or timer is 150:
                        battle.set_cal_exp()

            elif timer > 200+bonus: 
                sit_num = 3
                choose_inside = False

        BASE_SURF.blit(bat_surf, (0,0))
        timer += 1

    elif change_map(move_to):
        ALL_MAPS_DATA[current_map.map_num] = current_map
        current_map = Map(current_map.exits[player.pos], current_map.map_num)
        player,exits= set_state(current_map.x_screen, current_map.y_screen, current_map.exits.keys())

    else :
        current_map.make_move( player, move_to)
        BASE_SURF.blit(pygame.transform.scale(IMAGES['sea'], (X_RANGE,Y_RANGE)),(0,0))     
        map_surf, need_center = current_map.draw_map(player, exits)  
        map_surf_rect = map_surf.get_rect()
        if need_center : 
            map_surf_rect.center = BASE_SURF.get_rect().center
            BASE_SURF.blit(map_surf, map_surf_rect)
        else : BASE_SURF.blit(map_surf, current_map.get_screen_move())

        pygame.display.update()
        if move_to != None and current_map.map_data[player.pos[0]][player.pos[1]] is 'M' :
            if random.randint(1,10) is 1 : 
                time.sleep(0.1)           
                moniter = 0
                start_time = time.time()
                while time.time() - start_time < 1:
                    if moniter is 0: BASE_SURF.fill((0, 0, 0))  
                    elif moniter is 1 : BASE_SURF.fill((255, 255, 255)) 
                    else : 
                        BASE_SURF.blit(pygame.transform.scale(IMAGES['sea'], (X_RANGE,Y_RANGE)),(0,0)) 
                        if need_center :                              
                            map_surf_rect.center = BASE_SURF.get_rect().center
                            BASE_SURF.blit(map_surf, map_surf_rect)
                        else : BASE_SURF.blit(map_surf, current_map.get_screen_move())
                    pygame.display.update()
                    time.sleep(0.1)
                    moniter = (moniter+1)%3
                battle = Battle(pokedex.pokemon_list[0],Pokemon(1,1))
                sit_num = prior_sit_num = 4

    pygame.display.update()
