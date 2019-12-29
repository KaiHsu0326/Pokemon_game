import pygame, sys, os, random, time
from Class.pokemon import Pokemon, Battle, Pokedex
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
pygame.mixer.init()

IMAGES = {'title': pygame.image.load(dir_path+'/image/pokemon-logo.png'),
          'cover': pygame.image.load(dir_path+'/image/cover.png'),
          'sea': pygame.image.load(dir_path+'/image/sea.png'),
          'choose_poke_bg': pygame.image.load(dir_path+'/image/choose_poke_bg.png'),
          'arrow_up': pygame.image.load(dir_path+'/image/arrow_up.png')}

MUSIC = {'start': dir_path+'/sound/start.mp3',
         'wild_poke_1' : dir_path+'/sound/wild_poke_1.mp3',
         'wild_poke_2': dir_path+'/sound/wild_poke_2.mp3',
         'map1': dir_path+'/sound/map1.mp3',
         'evolution' : dir_path + '/sound/evolution.mp3',}

# music_paly = False
ALL_MAPS_DATA = ['']
for m in MAPS : ALL_MAPS_DATA.append(m)

def play_music(filename,time) :
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(time)


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

def get_situation():
    global situation
    return situation[-1]


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

def change_situation(add, situ):
    global inbox_choice, timer
    if add:
        situation.append(situ)
    else :situation.pop()

    inbox_choice = False      
    timer = 1  

choose = timer = pokedex = 1
situation = ['begin']
recovering = inbox_choice = False
BASE_SURF = pygame.display.set_mode((X_RANGE, Y_RANGE))
fontObj = pygame.font.Font('freesansbold.ttf', 35)
current_map = Map(1,-1)
bag = Bag()
player,exits= set_state(current_map.x_screen, current_map.y_screen, current_map.exits)
init_p = [Pokemon(0,5),Pokemon(6,7),Pokemon(3,5)]
play_music(MUSIC['start'],-1)

while True:
    
    move_to = None
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT :
                if get_situation() is not 'begin' and not recovering: move_to = 'LEFT'
            if e.key == pygame.K_RIGHT:
                if get_situation() is not 'begin' and not recovering: move_to = 'RIGHT'
            if e.key == pygame.K_UP:
                if get_situation() is not 'begin' and not recovering: move_to = 'UP'
            if e.key == pygame.K_DOWN:
                if get_situation() is not 'begin' and not recovering: move_to = 'DOWN'

            if e.key == pygame.K_b and get_situation() is 'walking':
                change_situation(True, 'bag')

            if e.key == pygame.K_c and get_situation() is 'walking': 
                change_situation(True, 'computer')

            if e.key == pygame.K_e and get_situation() is 'walking': 
                change_situation(True, 'evolution')

            if e.key == pygame.K_x :
                if inbox_choice: inbox_choice = False
                elif (get_situation() is 'bag' or get_situation() is 'pokedex' or get_situation() is 'computer' or get_situation() is 'shop') :
                    change_situation(False, '')

            if e.key == pygame.K_z :
                if get_situation() is 'begin' :
                    change_situation(True, 'choose_poke')

                elif get_situation() is 'walking' and current_map.is_npc_spot(player):
                    if current_map.is_npc_spot(player) == 'seller':
                        change_situation(True, 'shop')
                    elif current_map.is_npc_spot(player) == 'doctor':recovering = True

                elif get_situation() is 'choose_poke' :
                    pokedex = Pokedex(init_p[choose])
                    play_music(MUSIC['map1'],1) 
                    change_situation(True, 'walking')

                elif get_situation() is 'battle':
                    if inbox_choice: 
                        change_situation(True, 'battle_round')                      
                    elif choose is 0 and not inbox_choice:
                        inbox_choice = True
                    elif choose is 1:
                        change_situation(True, 'bag')
                    elif choose is 2:
                        change_situation(True, 'pokedex')
                    elif choose is 3:
                        play_music(MUSIC['map1'],1) 
                        change_situation(False, '')

                elif get_situation() is 'bag': 
                    if not inbox_choice and bag.has_item_inside(): inbox_choice = True
                    elif inbox_choice: 
                        throw_ball, props = bag.use_props(situation, current_map.challenge)
                        if throw_ball:
                            battle.set_catch_data(props)
                            change_situation(False, '')
                            change_situation(True, 'catch_pokemon')
                        inbox_choice = False

                elif get_situation() is 'pokedex':
                    if inbox_choice:
                        inbox_choice = False
                        if pokedex.swap_pokemon():
                            battle.set_my_pokemon(pokedex.pokemon_list[0])
                            change_situation(False, '')
                    else :
                        if pokedex.select_pokedex():
                            inbox_choice = True
                        else :
                            change_situation(False, '')

                elif get_situation() is 'computer':
                    if inbox_choice: 
                        pokedex.swap_com_poke()
                        inbox_choice = False
                    else : 
                        inbox_choice = True
                        
                elif get_situation() is 'shop':
                    if inbox_choice:
                        bag.transaction()
                        inbox_choice = False
                    else :
                        inbox_choice = True

    if get_situation() is 'begin' : draw_begin_cover()
 
    elif get_situation() is 'choose_poke' :
        draw_choose_begin_pokemon(init_p, move_to)

    elif get_situation() is 'battle_round' :
        if not battle.have_left_move_num(choose) and timer is 1:
            change_situation(False, '')
            inbox_choice = True
            continue
       
        bat_surf, finished = battle.battle_round_animate(timer, choose)
        BASE_SURF.blit(bat_surf, (0,0))
        timer += 1

        if finished : 
            change_situation(False, '')
            if battle.one_die():
                timer = -50
                change_situation(True, 'battle_finished')
            else :
                inbox_choice = False


    elif get_situation() is 'battle':       
        bat_surf, choose = battle.draw_battle(move_to, inbox_choice)
        BASE_SURF.blit(bat_surf, (0,0))

    elif get_situation() is 'bag': 
        bag_surf = bag.draw_bag(move_to, inbox_choice, pokedex.pokemon_list)
        BASE_SURF.blit(bag_surf, (0,0))

    elif get_situation() is 'pokedex' :
        pokedex_surf = pokedex.draw_pokedex(move_to, inbox_choice)
        BASE_SURF.blit(pokedex_surf, (0,0))

    elif get_situation() is 'computer':
        computer_surf = pokedex.draw_computer(move_to, inbox_choice)
        BASE_SURF.blit(computer_surf, (0,0))

    elif get_situation() is 'shop':
        shop_surf = bag.draw_shop(move_to, inbox_choice)
        BASE_SURF.blit(shop_surf, (0,0))

    elif get_situation() is 'battle_finished' :
        bonus = 0
        if pokedex.pokemon_list[0].has_level_up: 
            bonus = 50
        if timer < 0:
            bat_surf = battle.draw_battle_msg(0, 0)
        elif 0 < timer and timer < 200+bonus:
            if battle.my_pokemon_die():
                bat_surf = battle.draw_battle_msg(timer, 0, 0)
                if timer >= 140 and not battle.all_pokemon_die():
                    battle.set_my_pokemon(pokedex.seq_swap_poke())
                    change_situation(False, '') # pop to battle situation
            else : 
                bat_surf = battle.draw_battle_msg(0, timer, 0)
                if timer is 150:
                    battle.set_exp()

        elif timer >= 200+bonus: 
            change_situation(False, '') # pop to battle situation
            change_situation(False, '') # pop to walking situation
            inbox_choice = False
            pokedex.pokemon_list[0].has_level_up = False
            if pokedex.pokemon_list[0].evol_poke():
                change_situation(True, 'evolution')
            if not battle.my_pokemon_die():
                bag.add_money(battle.get_money())

            if battle.all_pokemon_die():
                current_map = Map(1,-1)
                recovering = True
                player,exits= set_state(6, 5, current_map.exits)
                
            elif current_map.challenge:
                if current_map.delete_challenge_spot():
                    print('Game_Over')
            play_music(MUSIC['map1'],1) 

        BASE_SURF.blit(bat_surf, (0,0))
        timer += 1


    elif get_situation() is 'evolution' :
        evol_surf, evol = pokedex.pokemon_list[0].draw_evolution(timer)
        if evol: 
            pokedex.pokemon_list[0] = evol
        if timer is 10:
            play_music(MUSIC['evolution'],1)
        if timer is 200:
            time.sleep(1)
            # music_paly = False
            change_situation(False, '') # pop to walking situation
            play_music(MUSIC['map1'],1) 
        timer += 1
        BASE_SURF.blit(evol_surf, (0,0))


    elif get_situation() is 'catch_pokemon' :
        bat_surf, catch, pokemon = battle.draw_catch_pokemon(timer, props)
        BASE_SURF.blit(bat_surf, (0,0))
        timer += 1
        if timer is 250:
            if catch:
                change_situation(False, '') # pop to battle situation
                change_situation(False, '') # pop to walking situation
                pokemon.recover()
                pokedex.pokemon_list.append(pokemon)
                play_music(MUSIC['map1'],1) 
            else:
                change_situation(False, '') # pop to battle situation

    elif change_map(move_to):
        # ALL_MAPS_DATA[current_map.map_num] = current_map
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

        if recovering:
            pygame.draw.rect(BASE_SURF,(255,213,132),(275,100,250,70))
            textSurfaceObj = fontObj.render('Recovering.....', True, (128,128,128))
            textRectObj = textSurfaceObj.get_rect()
            BASE_SURF.blit(textSurfaceObj, (275,120))
            if timer is 40:
                pokedex.recover_fight_poke()
                recovering = False
                timer = 0
            timer+= 1

        pygame.display.update()
        if move_to != None and current_map.map_data[player.pos[0]][player.pos[1]] is 'M' or current_map.challenge:
            if random.randint(1,10) is 1 or current_map.challenge: 
                time.sleep(0.1)           
                moniter = 0
                start_time = time.time()
                play_music(MUSIC['wild_poke_2'],1) 
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

                play_music(MUSIC['wild_poke_1'],-1)
                opp_data = pokedex.bomb_into_poke()
                battle = Battle(pokedex.pokemon_list[0],Pokemon(opp_data[0],opp_data[1]))
                battle.set_poke_list(pokedex.pokemon_list[:6])
                change_situation(True, 'battle')
                # music_paly = False

    pygame.display.update()
