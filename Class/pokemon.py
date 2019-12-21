import pygame, sys, os, random, time, json
from .map import X_RANGE, Y_RANGE

POKEDEX = { 1:'Bulbasaur', 2:'Ivysaur', 3:'Venusaur', 4:'Charmander', 5:'Charmeleon',
            6:'Charizard', 7:'Squirtle', 8:'Wartortle', 9:'Blastoise'}

LEVEL_TOP =[0,0]
level = 2
inital = 30
add_value = 20
while level < 40:
    LEVEL_TOP.append(inital)
    inital += add_value
    add_value += 10
    level += 1

dir_path = os.path.dirname(os.path.abspath(__file__))
json_data = open(dir_path+'/pokemon_data.json').read()
poke_data = json.loads(json_data)

class Move():
    def __init__(self, name, total_num, type, desc):
        self.name = name
        self.left_num = self.total_num = total_num
        self.type = type
        self.desc = desc

    def use_move(self) :
        self.left_num -= 1


class Pokemon():
    image_path = dir_path+'/../image/poke_image'
    sketch_path = dir_path + '/../image/sketch_image/'
    image_front = []
    image_back = []
    frame_num = 0

    def __init__(self,num, level):
        self.name = POKEDEX[num]
        self.image_front, self.image_back = self.load_image()
        self.sketch = pygame.image.load(self.sketch_path +'/'+ self.name + '_sketch.png')
        self.f_size = self.image_front[0].get_rect().size
        self.b_size = self.image_back[0].get_rect().size
        self.level = level
        self.remain_blood = self.hp = poke_data[self.name]['hp']+(level-1)*random.randint(poke_data[self.name]['add_value'][0],poke_data[self.name]['add_value'][1])
        self.attack = poke_data[self.name]['attack']+(level-1)*random.randint(poke_data[self.name]['add_value'][0],poke_data[self.name]['add_value'][1])
        self.defense = poke_data[self.name]['defense']+(level-1)*random.randint(poke_data[self.name]['add_value'][0],poke_data[self.name]['add_value'][1])
        self.move = self.move_type(poke_data[self.name]['type'])
        self.exp = 0
        
    def move_type(self, pkm_type):
        move = []
        if pkm_type == 'grass':
            move = [Move('attack1', 30, 'grass', 'entry move'),Move('attack2',20, 'grass', 'intermediate move'),
                    Move('attack3',10, 'grass', 'andvanced move'),Move('attack4',5, 'grass', 'super move')]
        elif pkm_type == 'fire':
            move = [Move('attack5',30, 'fire', 'entry move'),Move('attack6',20, 'fire', 'intermediate move'),
                    Move('attack7',10, 'fire', 'andvanced move'),Move('attack8',5, 'fire', 'super move')]
        elif pkm_type == 'water':
            move = [Move('PoisonPowder',30, 'water', 'entry move'),Move('attack10',20, 'water', 'intermediate move'),
                    Move('attack11',10, 'water', 'andvanced move'),Move('PoisonPowder',5, 'water', 'super move')]

        return move

    def load_image(self) :
        pok_front = []
        pok_back = []
        num = 1
        file_number = len(os.listdir(self.image_path +'/'+ self.name +'_front'))
        while num < file_number :
            pok_front.append(pygame.image.load(self.image_path +'/'+ self.name + '_front/' + self.name + '_front' + str(num) + '.png'))
            num+= 1

        num = 1
        file_number = len(os.listdir(self.image_path +'/'+ self.name +'_back'))
        while num < file_number :
            pok_back.append(pygame.image.load(self.image_path +'/'+ self.name + '_back/' + self.name + '_back' + str(num) + '.png'))
            num+= 1

        return pok_front, pok_back

    def get_frame_num(self, direction) :
        if (direction == 'front' and self.frame_num >= len(self.image_front)-1) or \
            (direction == 'back' and self.frame_num >= len(self.image_back)-1):
            self.frame_num = 0

        self.frame_num += 1
        return self.frame_num

    def cal_blood_lose_prcnt(self, width):       
        return int(width*self.remain_blood/self.hp)

    def cal_exp_prcnt(self, width):
        while self.exp >= LEVEL_TOP[self.level] :
            self.exp -= LEVEL_TOP[self.level] 
            self.level += 1
            self.has_level_up = True

        return int(width*self.exp/LEVEL_TOP[self.level])

        

BATTLE_IMGAE = {'battle_bg' : pygame.image.load(dir_path+'/../image/battle_bg.png'),
                'text' : pygame.image.load(dir_path+'/../image/battle_text.png'),
                'opp_hp' : pygame.image.load(dir_path+'/../image/opp_hp.png'),
                'my_hp' : pygame.image.load(dir_path+'/../image/my_hp.png'),
                'arrow_right' : pygame.image.load(dir_path+'/../image/arrow_right.png'),}

POKEDEX_IMGAE = {'pokedex_bg' : pygame.image.load(dir_path+'/../image/pokedex_bg.png'),
                 'not_choose_poke' : pygame.image.load(dir_path+'/../image/not_choose_poke.png'),
                 'first_poke' : pygame.image.load(dir_path+'/../image/first_poke.png'), 
                 'choose_poke' : pygame.image.load(dir_path+'/../image/choose_poke.png'),
                 'choose_cancel' : pygame.image.load(dir_path+'/../image/choose_cancel.png'),}

COMPUTER_IMGAE = {'computer_bg' : pygame.image.load(dir_path+'/../image/computer_bg.png'),
                  'pointer' : pygame.image.load(dir_path+'/../image/pointer.png'), }

def display_text(bat_surf, str, pos, font_size):
    fontObj = pygame.font.Font('freesansbold.ttf', font_size)
    textSurfaceObj = fontObj.render(str, True, (100,100,100))
    textRectObj = textSurfaceObj.get_rect()
    bat_surf.blit(textSurfaceObj, pos)

def display_arrow(move_to, offset):
    if move_to is 'LEFT' and offset > 0: offset -= 1        
    if move_to is 'RIGHT' and offset < 3: offset += 1
    if move_to is 'UP' and offset > 1: offset -= 2      
    if move_to is 'DOWN' and offset < 2 : offset += 2
    return offset

class Battle():
    bg_size = BATTLE_IMGAE['battle_bg'].get_rect().size
    arrow_direction = [[(520, 485),(665, 485),(520, 535),(665, 535)],
                       [(40, 485),(235, 485),(40, 535),(235, 535)]]

    pos_move = has_level_up = set_exp = False
    opp_attack = exp_gained = 0

    def __init__(self, p1, p2) :
        # self.my_pokemon = p1
        # self.my_pkm_image = p1.image_back
        self.opp_pokemon = p2
        self.opp_pkm_image = p2.image_front
        self.offset = 0
        # self.display_move ={ True: p1.move, False: ['FIGHT','BAG','POKEMON','RUN'] } 
        self.set_my_pokemon(p1)

    def display_battle_text(self, bat_surf):
        display_text(bat_surf, 'What should '+ self.my_pokemon.name + ' do?' , (100,515), 20) 
        display_text(bat_surf, 'FIGHT', (555,490), 20)
        display_text(bat_surf, 'BAG', (700,490), 20)
        display_text(bat_surf, 'POKEMON', (555,540), 20)
        display_text(bat_surf, 'RUN', (700,540), 20)

    def display_move_text(self, bat_surf, offset) :
        display_text(bat_surf, self.my_pokemon.move[0].name, (75,490), 20)
        display_text(bat_surf, self.my_pokemon.move[1].name, (270,490), 20)
        display_text(bat_surf, self.my_pokemon.move[2].name, (75,540), 20)
        display_text(bat_surf, self.my_pokemon.move[3].name, (270,540), 20)

        display_text(bat_surf, str(self.my_pokemon.move[offset].left_num) +' / '+ str(self.my_pokemon.move[offset].total_num), (550,490), 20)
        display_text(bat_surf, self.my_pokemon.move[offset].type, (680,490), 20)
        display_text(bat_surf, self.my_pokemon.move[offset].desc, (520,540), 20)

    def set_exp(self):
        self.exp_gained = (self.opp_pokemon.hp + self.opp_pokemon.attack + self.opp_pokemon.defense)//3
        self.my_pokemon.exp += self.exp_gained

    def get_hurt(self, turn, choose) :
        if turn is 'player' :
            hurt = int(self.opp_pokemon.attack*(1+0.06*choose) - self.my_pokemon.defense)
            if hurt <= 0 : hurt = random.randint(2,5)
            hurt += 10
            if self.my_pokemon.remain_blood > hurt:
               self.my_pokemon.remain_blood -= hurt
            else : self.my_pokemon.remain_blood = 0
            print(f'get {hurt} points hurt and my pokemon hp remain : {self.my_pokemon.remain_blood} ')

        elif turn is 'opponent':
            hurt = int(self.my_pokemon.attack*(1+0.06*choose) - self.opp_pokemon.defense)
            if hurt <= 0 : hurt = random.randint(2,5)   
            hurt += 10      
            if self.opp_pokemon.remain_blood > hurt:
               self.opp_pokemon.remain_blood -= hurt
            else : self.opp_pokemon.remain_blood = 0
            print(f'get {hurt} points hurt and opp pokemon hp: {self.opp_pokemon.remain_blood}')

    def display_pokemon(self,bat_surf, poke_site, poke, image, face, hp_image_name, hp_site) :
        space_rect = pygame.Rect(poke_site)
        pkm = pygame.transform.scale(image[poke.get_frame_num(face)], \
            (int(poke.f_size[0]*1.5), int(poke.f_size[1]*1.5)))       
        rect = pkm.get_rect()
        rect.midbottom = space_rect.midbottom
        bat_surf.blit(pkm, rect)
        if face is 'back': 
            pygame.draw.rect(bat_surf,(73,83,87),(579,360,188,20))
            pygame.draw.rect(bat_surf,(120,243,172),(579,360,self.my_pokemon.cal_blood_lose_prcnt(188),20)) # green
            pygame.draw.rect(bat_surf,(73,83,87),(520,410,247,10))
            pygame.draw.rect(bat_surf,(225,207,64),(520,410,self.my_pokemon.cal_exp_prcnt(247),10))  # yellow
        elif face is 'front': 
            pygame.draw.rect(bat_surf,(73,83,87),(212,72,186,20))
            pygame.draw.rect(bat_surf,(120,243,172),(212,72,self.opp_pokemon.cal_blood_lose_prcnt(186),20))  # green
        
        hp_surf = pygame.Surface((400, 100), pygame.SRCALPHA)
        hp_surf.blit(pygame.transform.scale(BATTLE_IMGAE[hp_image_name],(400,100)), (0,0))
        if face is 'back':display_text(hp_surf, str(poke.level), (346,12), 27)
        elif face is 'front':display_text(hp_surf, str(poke.level), (329,18), 27)
        bat_surf.blit(hp_surf, hp_site)      
        
    def draw_battle(self, move_to, choose_move) :
        bat_surf = pygame.Surface((X_RANGE, Y_RANGE))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['battle_bg'], (int(self.bg_size[0]*0.63), int(self.bg_size[1]*0.63))), (0,0))
        self.display_pokemon(bat_surf, (520,70, 135, 140), self.opp_pokemon, self.opp_pkm_image, 'front', 'opp_hp', (50,25)) 
        self.display_pokemon(bat_surf, (200,250, 135, 140), self.my_pokemon, self.my_pkm_image, 'back', 'my_hp', (400,325))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(500,150)), (0,450)) # 第一塊方格 What should ... do
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(300,150)), (500,450)) # 第二塊方格 FIGHT BAG ...
        if not choose_move : self.display_battle_text(bat_surf)
        else : self.display_move_text(bat_surf,self.offset)
        self.offset = display_arrow(move_to, self.offset)
        bat_surf.blit(BATTLE_IMGAE['arrow_right'], self.arrow_direction[choose_move][self.offset]) 
        return bat_surf, self.offset

    def draw_battle_round(self,turn,choose,opp_x,my_x):
        bat_surf = pygame.Surface((X_RANGE, Y_RANGE))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['battle_bg'], (int(self.bg_size[0]*0.63), int(self.bg_size[1]*0.63))), (0,0))
        self.display_pokemon(bat_surf, (520+opp_x,70, 135, 140), self.opp_pokemon, self.opp_pkm_image, 'front', 'opp_hp', (50,25)) 
        self.display_pokemon(bat_surf, (200+my_x,250, 135, 140), self.my_pokemon, self.my_pkm_image, 'back', 'my_hp', (400,325))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(500,150)), (0,450)) # 第一塊方格 What should ... do
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(300,150)), (500,450)) # 第二塊方格 FIGHT BAG ...
        if turn is 'player' :
            display_text(bat_surf, self.my_pokemon.name + ' used ' + self.my_pokemon.move[choose].name , (100,515), 20) 
        elif turn is 'opponent' : 
            display_text(bat_surf, self.opp_pokemon.name + ' used ' + self.opp_pokemon.move[choose].name , (100,515), 20) 
        return bat_surf

    def battle_round_animate(self, timer, choose):
        attack_time = 40
        hurt_time = 10
        bat_surf = pygame.Surface((X_RANGE, Y_RANGE))

        if timer < attack_time:
            bat_surf = self.draw_battle_round('player',choose,0,0)
 
        elif attack_time <= timer and timer < attack_time+hurt_time:
            if self.pos_move:
                bat_surf = self.draw_battle_round('player',choose,5,0)
            else :bat_surf = self.draw_battle_round('player',choose,-5,0)
            self.pos_move = not self.pos_move

        elif timer == attack_time+hurt_time:
            self.decrease_move_num(choose)
            self.get_hurt('opponent',choose)
            bat_surf = self.draw_battle_round('player',choose,0,0)

            can_use = []
            for i in range(4):
                if self.opp_pokemon.move[i].left_num != 0:
                    can_use.append(i)

            self.opp_attack = can_use[random.randint(0,len(can_use)-1)]

            if self.one_die() : 
                return bat_surf, True
            
        elif attack_time+hurt_time < timer and timer < attack_time*2+hurt_time:
            bat_surf = self.draw_battle_round('opponent',self.opp_attack,0,0)

        elif attack_time*2+hurt_time <= timer and timer < 2*(attack_time+hurt_time):
            if self.pos_move:
                bat_surf = self.draw_battle_round('opponent',self.opp_attack,0,5)
            else :bat_surf = self.draw_battle_round('opponent',self.opp_attack,0,-5)
            self.pos_move = not self.pos_move

        elif timer == 2*(attack_time+hurt_time):
            self.get_hurt('player',self.opp_attack)
            bat_surf = self.draw_battle_round('opponent',self.opp_attack,0,0)
            if self.one_die() : 
                return bat_surf, True
            
        elif 2*(attack_time+hurt_time) < timer:
            bat_surf = self.draw_battle_round('opponent',self.opp_attack,0,0)
            return bat_surf, True

        return bat_surf, False

    def draw_battle_over(self, my_shift, opp_shift):
        bat_surf = pygame.Surface((X_RANGE, Y_RANGE))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['battle_bg'], (int(self.bg_size[0]*0.63), int(self.bg_size[1]*0.63))), (0,0))
        if opp_shift < 10:
            self.display_pokemon(bat_surf, (520,70+opp_shift*20, 135, 140), self.opp_pokemon, self.opp_pkm_image, 'front', 'opp_hp', (50,25)) 
        if my_shift < 10:
            self.display_pokemon(bat_surf, (200,250+my_shift*20, 135, 140), self.my_pokemon, self.my_pkm_image, 'back', 'my_hp', (400,325))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(500,150)), (0,450)) # 第一塊方格 What should ... do
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(300,150)), (500,450)) # 第二塊方格 FIGHT BAG ...
        self.display_dif_msg(bat_surf, my_shift, opp_shift)
        return bat_surf

    def display_dif_msg(self, bat_surf, my_shift, opp_shift):
        value = [my_shift, opp_shift]
        lose_num = -1
        if opp_shift is 0 and my_shift is not 0: lose_num = 0
        elif opp_shift is not 0 and my_shift is 0: lose_num = 1

        if lose_num is 1:
            if 200 <= value[lose_num]:
                display_text(bat_surf, self.my_pokemon.name + ' grew to LV. ' + str(self.my_pokemon.level) + '!', (100,515), 20) 
            elif 150 <= value[lose_num] : 
                display_text(bat_surf, self.my_pokemon.name + ' gained ' + str(self.exp_gained) + ' EXP. Points!', (100,515), 20) 
            else :
                display_text(bat_surf, 'Enemy ' + self.opp_pokemon.name + ' fainted!', (100,515), 20) 
        elif lose_num is 0 : 
            if 140 <= value[lose_num] : 
                display_text(bat_surf, 'All of your pokemons fainted', (100,515), 20) 
            else :
                display_text(bat_surf, 'Your Pokemon ' + self.my_pokemon.name + ' fainted!', (100,515), 20) 

    def have_left_move_num(self, choose):
        if self.my_pokemon.move[choose].left_num > 0: return True
        else :return False

    def decrease_move_num(self, choose):
        self.my_pokemon.move[choose].use_move()
        print(self.my_pokemon.move[choose].left_num)
        self.offset = 0

    def one_die(self):
        if self.my_pokemon.remain_blood is 0 or self.opp_pokemon.remain_blood is 0:
            return True
        else : return False

    def my_pokemon_die(self):
        if self.my_pokemon.remain_blood is 0: return True
        else : return False

    def set_my_pokemon(self, p1):
        self.my_pokemon = p1
        self.my_pkm_image = p1.image_back
        self.display_move ={ True: p1.move, False: ['FIGHT','BAG','POKEMON','RUN'] } 


class Pokedex():
    
    pokemon_list = []
    POKEDEX_MAX = 6
    change = False
    com_point = 0
    def __init__(self, p) :
        self.current_pokemon = 0
        self.current_compokemon = 0
        self.pokemon_list.append(p)
        
        self.pokemon_list.append(Pokemon(2,5))
        self.pokemon_list.append(Pokemon(3,5))
        self.pokemon_list.append(Pokemon(4,5))
        self.pokemon_list.append(Pokemon(5,5))
        self.pokemon_list.append(Pokemon(6,5))
        self.pokemon_list.append(Pokemon(7,5))
        self.pokemon_list.append(Pokemon(8,5))
        self.pokemon_list.append(Pokemon(9,5))



    def draw_pokedex(self, move_to, inbox_choice):
        pokedex_surf = pygame.Surface((X_RANGE, Y_RANGE))
        pokedex_surf.blit(pygame.transform.scale(POKEDEX_IMGAE['pokedex_bg'], (X_RANGE, Y_RANGE)), (0,0))
        display_text(pokedex_surf, 'CHOOSE A POKEMON', (100, 500), 32)

        # --------------第一隻(最左邊)----獨立顯示-----------------------
        pokedex_surf.blit(pygame.transform.scale(POKEDEX_IMGAE['first_poke'], (250, 200)), (50,50))
        pokedex_surf.blit(pygame.transform.scale(self.pokemon_list[0].sketch, (75, 75)), (75,100))
        display_text(pokedex_surf, self.pokemon_list[0].name, (150, 125), 25)
        display_text(pokedex_surf, str(self.pokemon_list[0].level), (190, 155), 25)
        pygame.draw.rect(pokedex_surf,(73,83,87),(142,190,132,8))
        pygame.draw.rect(pokedex_surf,(120,243,172),(142,190,self.pokemon_list[0].cal_blood_lose_prcnt(132),8)) # green 血量圖示

        display_text(pokedex_surf, str(self.pokemon_list[0].hp), (240, 210), 25) # 血量文字
        display_text(pokedex_surf, str(self.pokemon_list[0].remain_blood), (190,210), 25) # 血量文字
        # -------------------------------------------------------------

        for i in range(self.POKEDEX_MAX-1):
            pokedex_surf.blit(pygame.transform.scale(POKEDEX_IMGAE['not_choose_poke'], (400, 78)), (350,i*88))

        list_length = 5
        if len(self.pokemon_list) < 6 :
           list_length = len(self.pokemon_list)-1 # 因為第一隻不會選擇，所以要看的就是除了第一隻之外的剩下
           
        for i in range(list_length):
            pygame.draw.rect(pokedex_surf,(73,83,87),(604,29+i*88,123,8))
            pygame.draw.rect(pokedex_surf,(120,243,172),(604,29+i*88,self.pokemon_list[i+1].cal_blood_lose_prcnt(123),8)) # green 血量圖示
            display_text(pokedex_surf, str(self.pokemon_list[i+1].hp), (700, 50+i*88), 25) # 血量文字
            display_text(pokedex_surf, str(self.pokemon_list[i+1].remain_blood), (640,50+i*88), 25) # 血量文字

            pokedex_surf.blit(pygame.transform.scale(self.pokemon_list[i+1].sketch, (60, 60)), (354,15+i*88))
            display_text(pokedex_surf, self.pokemon_list[i+1].name, (425, 20+i*88), 20)
            display_text(pokedex_surf, str(self.pokemon_list[i+1].level), (480, 50+i*88), 20)
    
        if move_to == 'UP' and self.current_pokemon > 0:
            self.current_pokemon -= 1
        elif move_to == 'DOWN' and self.current_pokemon < list_length:
            self.current_pokemon += 1
        elif move_to == 'RIGHT' and inbox_choice:
            self.change = False
        elif move_to == 'LEFT' and inbox_choice:
            self.change = True

        if self.current_pokemon >= list_length:
            pokedex_surf.blit(pygame.transform.scale(POKEDEX_IMGAE['choose_cancel'], (200, 100)), (565,465)) # 選不到印cancel 
        else:
            pokedex_surf.blit(pygame.transform.scale(POKEDEX_IMGAE['choose_poke'], (400, 78)), (345,self.current_pokemon*88))
            pokedex_surf.blit(pygame.transform.scale(self.pokemon_list[self.current_pokemon+1].sketch, (60, 60)), (354,15+self.current_pokemon*88))
            display_text(pokedex_surf, self.pokemon_list[self.current_pokemon+1].name, (425, 20+self.current_pokemon*88), 20)
            display_text(pokedex_surf, str(self.pokemon_list[self.current_pokemon+1].level), (480, 50+self.current_pokemon*88), 20)
            display_text(pokedex_surf, str(self.pokemon_list[self.current_pokemon+1].hp), (700, 50+self.current_pokemon*88), 25) # 血量文字
            display_text(pokedex_surf, str(self.pokemon_list[self.current_pokemon+1].remain_blood), (640,50+self.current_pokemon*88), 25) # 血量文字    

        if inbox_choice:
            pygame.draw.rect(pokedex_surf,(255,213,132),(200,200,400,200))
            display_text(pokedex_surf, 'Want to change this pokemon?', (250, 250), 20)
            display_text(pokedex_surf, '[Yes]', (300, 300), 25)
            display_text(pokedex_surf, '[No]', (450, 300), 25)
            if self.change :
                pokedex_surf.blit(BATTLE_IMGAE['arrow_right'], (270, 300))
            else : 
                pokedex_surf.blit(BATTLE_IMGAE['arrow_right'], (420, 300))
        
        return pokedex_surf

    def swap_pokemon(self):
        if self.change:
            self.change = False
            self.pokemon_list[0], self.pokemon_list[self.current_pokemon+1] = self.pokemon_list[self.current_pokemon+1], self.pokemon_list[0]
            return True
        else: return False

    def select_pokedex(self) :
        if self.current_pokemon is 5 or self.current_pokemon is len(self.pokemon_list)-1:
            return False
        else : return True
        
    def draw_pokedex_pokemon(self, pokedex_surf):
        if len(pokemon_list) is not 0 :
            index = 0
            for i in pokemon_list:         
                bag_surf.blit(pygame.transform.scale(i.image,(50,50)), (350,35+index*60))
                display_text(bag_surf, i.name, (425,50+index*60))    
                display_text(bag_surf, 'X'+ str(i.num), (700,50+index*60)) 
                index += 1
                
            bag_surf.blit(pygame.transform.scale(interface.items[self.current_item].image,(50,50)),(35,500)) 
            display_text(bag_surf, interface.items[self.current_item].description, (150, 500)) 
            pygame.draw.rect(bag_surf, (255, 0, 0), ((290, 25+(self.current_item*63)), (485, 65)), 5)

    def draw_computer(self, move_to, inbox_choice):
        computer_surf = pygame.Surface((X_RANGE, Y_RANGE))
        computer_surf.blit(pygame.transform.scale(COMPUTER_IMGAE['computer_bg'], (X_RANGE, Y_RANGE)), (0,0))
        j =  k = 0 
        for i in range(6,len(self.pokemon_list)):
            if i % 5 == 1 and i > 6 :
                k += 1
                j = 0
            computer_surf.blit(pygame.transform.scale(self.pokemon_list[i].sketch, (70, 70)), (150+j*100,135+k*100))
            j += 1

        list_length = len(self.pokemon_list) - 7 # 還要扣掉自身可以帶的6隻

        if inbox_choice:
            if len(self.pokemon_list) > 6: inbox_list = 6
            else :inbox_list = len(self.pokemon_list)

            if move_to == 'UP' and self.com_point > 0:
                self.com_point -= 1
            elif move_to == 'DOWN' and self.com_point < inbox_list-1:
                self.com_point += 1
            pygame.draw.rect(computer_surf, (255,213,132), (470,100,280,200))
            l = 0
            for poke in self.pokemon_list[:6]:
                display_text(computer_surf, poke.name, (520,120+l), 20)
                display_text(computer_surf, str(poke.remain_blood)+'/'+str(poke.hp), (680,120+l), 20)
                
                l+=30
            computer_surf.blit(BATTLE_IMGAE['arrow_right'], (485,117+29*self.com_point)) 
        else :
            if move_to == 'LEFT' and self.current_compokemon > 0:
                self.current_compokemon -= 1
            elif move_to == 'RIGHT' and self.current_compokemon < list_length:
                self.current_compokemon += 1 
            elif move_to == 'UP' and self.current_compokemon-5 >= 0:
                self.current_compokemon -= 5 
            elif move_to == 'DOWN' and self.current_compokemon+5 <= list_length:
                self.current_compokemon += 5 
       
        x = self.current_compokemon % 5
        y = self.current_compokemon // 5
        computer_surf.blit(pygame.transform.scale(COMPUTER_IMGAE['pointer'], (40, 40)), (170+x*100,90+y*100))
        
        return computer_surf

    def get_poke_level(self):
        num = 0
        for poke in self.pokemon_list[:6]:
            num += poke.level

        if len(self.pokemon_list) > 6:
            num = num//6
        else:
            num = num//len(self.pokemon_list)

        return num-2

    def swap_com_poke(self):
        self.pokemon_list[self.current_compokemon+6], self.pokemon_list[self.com_point] = \
            self.pokemon_list[self.com_point], self.pokemon_list[self.current_compokemon+6]

        self.com_point = 0
        # self.current_compokemon = 0