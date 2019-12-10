import pygame, sys, os, random, time
from .map import X_RANGE, Y_RANGE

POKEDEX = { 1:'Bulbasaur', 2:'Ivysaur', 3:'Venusaur', 4:'Charmander', 5:'Charmeleon',
            6:'Charizard', 7:'Squirtle', 8:'Wartortle', 9:'Blastoise'}

POKE_STATS = {'unevol':[45,49,(2,3),16], 'fir_evol': [60,62,(2,3),32], 'sec_evol': [80,82,(1,2)]}

UNEVOL = ['Bulbasaur','Charmander','Squirtle']
FIR_EVOL = ['Ivysaur','Charmeleon','Wartortle']
SEC_EVOL = ['Venusaur','Charizard','Blastoise']

TYPE = {'Bulbasaur': 'grass', 'Ivysaur': 'grass', 'Venusaur': 'grass',
        'Charmander': 'fire', 'Charmeleon': 'fire', 'Charizard': 'fire',
        'Squirtle': 'water', 'Wartortle': 'water', 'Blastoise': 'water'}

MOVE = {'grass':['attack1','attack2','attack3','attack4'],
        'fire':['attack5','attack6','attack7','attack8'],
        'water':['attack9','attack10','attack11','attack12']}

LEVEL_TOP =[0,0]
level = 2
inital = 30
add_value = 20
while level < 40:
    LEVEL_TOP.append(inital)
    inital += add_value
    add_value += 10
    level += 1

LATENCY = 1
dir_path = os.path.dirname(os.path.abspath(__file__))

class Pokemon():
    image_path = dir_path+'/../image/poke_image'
    image_front = []
    image_back = []
    stats = []
    frame_num = 0
    late = 0

    def __init__(self,num, level):
        self.name = POKEDEX[num]
        self.image_front, self.image_back = self.load_image()
        self.f_size = self.image_front[0].get_rect().size
        self.b_size = self.image_back[0].get_rect().size
        self.level = level
        if self.name in UNEVOL:self.stats = POKE_STATS['unevol']
        if self.name in FIR_EVOL:self.stats = POKE_STATS['fir_evol']
        if self.name in SEC_EVOL:self.stats = POKE_STATS['sec_evol']
        self.hp = self.stats[0]+(level-1)*random.randint(self.stats[2][0],self.stats[2][1])
        self.attack = self.stats[1]+(level-1)*random.randint(self.stats[2][0],self.stats[2][1])
        self.move = MOVE[TYPE[self.name]]
        self.exp = LEVEL_TOP[level]
        

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
        if (direction == 'front' and self.frame_num >= len(self.image_front)) or \
            (direction == 'back' and self.frame_num >= len(self.image_back)):
            self.frame_num = 0

        tmp = self.frame_num
        self.late += 1
        if self.late == LATENCY :
            self.late = 0
            self.frame_num += 1
        return tmp

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
    arrow_direction = [(520, 485),(665, 485),(520, 535),(665, 535)]

    def __init__(self, p1, p2) :
        self.my_pokemon = p1
        self.my_pkm_image = p1.image_back
        self.opp_pokemon = p2
        self.opp_pkm_image = p2.image_front
        self.offset = 0
        self.display_move ={ True: p1.move, False: ['FIGHT','BAG','POKEMON','RUN'] } 

    def display_battle_text(self, bat_surf, choose_move):
        display_text(bat_surf, 'What should '+ self.my_pokemon.name + ' do?' , (100,515), 20) 
        display_text(bat_surf, self.display_move[choose_move][0], (555,490), 20)
        display_text(bat_surf, self.display_move[choose_move][1], (700,490), 20)
        display_text(bat_surf, self.display_move[choose_move][2], (555,540), 20)
        display_text(bat_surf, self.display_move[choose_move][3], (700,540), 20)


    def display_pokemon(self,bat_surf, poke_site, poke, image, face, hp_image_name, hp_site) :
        space_rect = pygame.Rect(poke_site)
        pkm = pygame.transform.scale(image[poke.get_frame_num(face)], \
            (int(poke.f_size[0]*1.5), int(poke.f_size[1]*1.5)))       
        rect = pkm.get_rect()
        rect.midbottom = space_rect.midbottom
        bat_surf.blit(pkm, rect)
        if face is 'back': 
            pygame.draw.rect(bat_surf,(73,83,87),(579,360,188,20))
            pygame.draw.rect(bat_surf,(120,243,172),(579,360,188,20))
            pygame.draw.rect(bat_surf,(73,83,87),(520,410,247,10))
            pygame.draw.rect(bat_surf,(225,207,64),(520,410,247,10))
        elif face is 'front': 
            pygame.draw.rect(bat_surf,(73,83,87),(212,72,186,20))
            pygame.draw.rect(bat_surf,(120,243,172),(212,72,186,20))
        
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
        self.display_battle_text(bat_surf, choose_move)
        self.offset = display_arrow(move_to, self.offset)
        bat_surf.blit(BATTLE_IMGAE['arrow_right'], self.arrow_direction[self.offset]) 
        return bat_surf, self.offset

    def draw_battle_round(self,turn,choose,opp_x,my_x):
        bat_surf = pygame.Surface((X_RANGE, Y_RANGE))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['battle_bg'], (int(self.bg_size[0]*0.63), int(self.bg_size[1]*0.63))), (0,0))
        self.display_pokemon(bat_surf, (520+opp_x,70, 135, 140), self.opp_pokemon, self.opp_pkm_image, 'front', 'opp_hp', (50,25)) 
        self.display_pokemon(bat_surf, (200+my_x,250, 135, 140), self.my_pokemon, self.my_pkm_image, 'back', 'my_hp', (400,325))
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(500,150)), (0,450)) # 第一塊方格 What should ... do
        bat_surf.blit(pygame.transform.scale(BATTLE_IMGAE['text'],(300,150)), (500,450)) # 第二塊方格 FIGHT BAG ...
        if turn is 'player':display_text(bat_surf, self.my_pokemon.name + ' uses ' + self.my_pokemon.move[choose] , (100,515), 20) 
        elif turn is 'opponent':display_text(bat_surf, self.opp_pokemon.name + ' uses ' + self.opp_pokemon.move[choose] , (100,515), 20) 
        return bat_surf

class Pokedex():
    pokemon_list = []
    def __init__(self, p) :
        self.pokemon_list.append(p)

    

