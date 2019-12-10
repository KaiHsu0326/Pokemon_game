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
    image_front = []
    image_back = []
    frame_num = 0

    def __init__(self,num, level):
        self.name = POKEDEX[num]
        self.image_front, self.image_back = self.load_image()
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

BATTLE_IMGAE = {'battle_bg' : pygame.image.load(dir_path+'/../image/battle_bg.png'),
                'text' : pygame.image.load(dir_path+'/../image/battle_text.png'),
                'opp_hp' : pygame.image.load(dir_path+'/../image/opp_hp.png'),
                'my_hp' : pygame.image.load(dir_path+'/../image/my_hp.png'),
                'arrow_right' : pygame.image.load(dir_path+'/../image/arrow_right.png'),}

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

    my_pkm_hurt = opp_pkm_hurt = 0
    has_level_up = set_exp = False
    opp_move = exp_gained = 0

    def __init__(self, p1, p2) :
        self.my_pokemon = p1
        self.my_pkm_image = p1.image_back
        self.opp_pokemon = p2
        self.opp_pkm_image = p2.image_front
        self.offset = 0
        self.display_move ={ True: p1.move, False: ['FIGHT','BAG','POKEMON','RUN'] } 

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

    def cal_blood_lose_prcnt(self, face, width):
        if face is 'back': 
            return int(width*self.my_pokemon.remain_blood/self.my_pokemon.hp)

        elif face is 'front': 
            return int(width*self.opp_pokemon.remain_blood/self.opp_pokemon.hp)

    def cal_exp_prcnt(self, gain_exp, width):
        self.my_pokemon.exp += gain_exp
        while self.my_pokemon.exp >= LEVEL_TOP[self.my_pokemon.level] :
            self.my_pokemon.exp -= LEVEL_TOP[self.my_pokemon.level] 
            self.my_pokemon.level += 1
            self.has_level_up = True

        return int(width*self.my_pokemon.exp/LEVEL_TOP[self.my_pokemon.level])

    def cal_gain_exp(self):
        if not self.set_exp :return 0
        else :
            self.exp_gained = (self.opp_pokemon.hp + self.opp_pokemon.attack + self.opp_pokemon.defense)//3
            return self.exp_gained

    def get_hurt(self, turn, choose) :
        if turn is 'player' :
            hurt = int(self.opp_pokemon.attack*(1+0.06*choose) - self.my_pokemon.defense)
            if hurt <= 0 : hurt = random.randint(2,5)
            if self.my_pokemon.level - self.opp_pokemon.level >= 4: hurt += 15
            if self.my_pokemon.remain_blood > hurt:
               self.my_pokemon.remain_blood -= hurt
            else : self.my_pokemon.remain_blood = 0
            print(f'get {hurt} points hurt and my pokemon hp remain : {self.my_pokemon.remain_blood} ')

        elif turn is 'opponent':
            hurt = int(self.my_pokemon.attack*(1+0.06*choose) - self.opp_pokemon.defense)
            if hurt <= 0 : hurt = random.randint(2,5)          
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
            pygame.draw.rect(bat_surf,(120,243,172),(579,360,self.cal_blood_lose_prcnt(face, 188),20)) # green
            pygame.draw.rect(bat_surf,(73,83,87),(520,410,247,10))
            pygame.draw.rect(bat_surf,(225,207,64),(520,410,self.cal_exp_prcnt(self.cal_gain_exp(), 247),10))  # yellow
        elif face is 'front': 
            pygame.draw.rect(bat_surf,(73,83,87),(212,72,186,20))
            pygame.draw.rect(bat_surf,(120,243,172),(212,72,self.cal_blood_lose_prcnt(face, 186),20))  # green
        
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

    def draw_battle_over(self, my_shift, opp_shift):
        bat_surf = pygame.Surface((X_RANGE, Y_RANGE))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['battle_bg'], (int(self.bg_size[0]*0.63), int(self.bg_size[1]*0.63))), (0,0))
        if opp_shift < 10:
            self.display_pokemon(bat_surf, (520,70+opp_shift*20, 135, 140), self.opp_pokemon, self.opp_pkm_image, 'front', 'opp_hp', (50,25)) 
        if my_shift < 10:
            self.display_pokemon(bat_surf, (200,250+my_shift*20, 135, 140), self.my_pokemon, self.my_pkm_image, 'back', 'my_hp', (400,325))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(500,150)), (0,450)) # 第一塊方格 What should ... do
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(300,150)), (500,450)) # 第二塊方格 FIGHT BAG ...
        if my_shift is not 0 :
            display_text(bat_surf, self.my_pokemon.name + ' dissolved!', (100,515), 20) 
        elif my_shift > 200 or opp_shift > 200:
            display_text(bat_surf, self.my_pokemon.name + ' grew to LV. ' + str(self.my_pokemon.level) + '!', (100,515), 20) 
        elif 150 <= my_shift or 150 <= opp_shift:
            display_text(bat_surf, self.my_pokemon.name + ' gained ' + str(self.exp_gained) + ' EXP. Points!', (100,515), 20) 
        
        else : 
            display_text(bat_surf, self.opp_pokemon.name + ' dissolved!', (100,515), 20) 
        return bat_surf

    def have_left_move_num(self, choose):
        if self.my_pokemon.move[choose].left_num > 0: return True
        else :return False

    def decrease_move_num(self, choose):
        self.my_pokemon.move[choose].use_move()
        self.offset = 0

    def one_die(self):
        if self.my_pokemon.remain_blood is 0 or self.opp_pokemon.remain_blood is 0:
            return True
        else : return False

    def my_pokemon_die(self):
        if self.my_pokemon.remain_blood is 0: return True
        else : return False

    def set_cal_exp(self):
        self.set_exp = not self.set_exp


class Pokedex():
    pokemon_list = []
    def __init__(self, p) :
        self.pokemon_list.append(p)

    

