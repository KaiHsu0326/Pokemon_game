import pygame, sys, os

from .map import X_RANGE, Y_RANGE
dir_path = os.path.dirname(os.path.abspath(__file__))


BAG_IMGAE = {'bag_bg' : pygame.image.load(dir_path+'/../image/bag_bg.png'),
             'PokeBall' : pygame.image.load(dir_path+'/../image/poke_balls.png'),
             'Potion' : pygame.image.load(dir_path+'/../image/potion.png'),
             'arrow_right' : pygame.image.load(dir_path+'/../image/arrow_right.png')}

BAGDEX = {'balls':['PokeBall'], 
          'props':['Potion'] }


def display_text(bat_surf, str, pos, font_size):
    fontObj = pygame.font.Font('freesansbold.ttf', font_size)
    textSurfaceObj = fontObj.render(str, True, (128,128,128))
    textRectObj = textSurfaceObj.get_rect()
    bat_surf.blit(textSurfaceObj, pos)


class Items():

    def __init__(self, name, num, description) :
        self.name = name
        self.num = num
        self.description = description
        self.image = BAG_IMGAE[name]
        self.type = self.get_type(name)

    def get_type(self, name):
        if name in BAGDEX['balls'] :return 'balls'
        elif name in BAGDEX['props'] :return 'props'

class Interface():
    choose_inside = 0
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        if name == 'Poké balls':
            self.items = [Items('PokeBall', 5, 'Catching wild Pokémon props')]
        else :
            self.items = [Items('Potion', 5, 'Allows one Pokémon to recover 20HP')]


class Bag():
    p_list = []
    use = False
    def __init__(self) :
        self.balls = None
        self.items = None
        self.current_interface = 1
        self.current_item = 0
        self.interfaces = [Interface('Items',(95,50)),Interface('Poké balls',(65,50))]

    def check_item(self, interface):
        for i in range(len(interface.items)):
            if interface.items[i].num is 0:
                del interface.items[i]

    def has_item_inside(self):
        if len(self.interfaces[self.current_interface].items) > 0:
            return True
        else: return False

    def draw_bag(self, move_to, inbox_choice, poke_list):
        bag_surf = pygame.Surface((X_RANGE, Y_RANGE))
        bag_surf.blit(pygame.transform.scale(BAG_IMGAE['bag_bg'],(800,600)), (0,0))
        self.check_item(self.interfaces[self.current_interface])
        if move_to == 'LEFT' :
            if not inbox_choice and self.current_interface > 0: self.current_interface -= 1
            elif inbox_choice: self.use = True
        elif move_to == 'RIGHT' :
            if not inbox_choice and self.current_interface < len(self.interfaces)-1 : self.current_interface += 1
            elif inbox_choice: self.use = False
        elif move_to == 'UP' :
            if not inbox_choice and self.current_item > 0: self.current_item -= 1
            elif inbox_choice and interface.choose_inside > 0: interface.choose_inside -= 1
        elif move_to == 'DOWN' :
            if not inbox_choice and self.current_item < len(self.interfaces[self.current_interface].items) -1 : self.current_item += 1
            elif inbox_choice and interface.choose_inside < len(poke_list) -1 : interface.choose_inside += 1

        display_text(bag_surf, self.interfaces[self.current_interface].name,self.interfaces[self.current_interface].pos, 32)
        self.draw_bag_items(bag_surf, self.interfaces[self.current_interface])
        if inbox_choice:
            interface = self.interfaces[self.current_interface]
            if interface.name == 'Poké balls': 
                pygame.draw.rect(bag_surf,(255,213,132),(200,200,400,200))
                display_text(bag_surf, f'Do you want to use {interface.items[self.current_item].name}', (250, 250), 20)
                display_text(bag_surf, '[Yes]', (300, 300), 25)
                display_text(bag_surf, '[No]', (450, 300), 25)

                if self.use :
                    bag_surf.blit(BAG_IMGAE['arrow_right'], (270, 300))
                else : 
                    bag_surf.blit(BAG_IMGAE['arrow_right'], (420, 300))
            elif interface.name == 'Items':
                self.p_list = poke_list
                pygame.draw.rect(bag_surf, (255,213,132), (470,100,280,200))
                l = 0
                for poke in poke_list[:6]:
                    display_text(bag_surf, poke.name, (520,120+l),20)
                    display_text(bag_surf, str(poke.remain_blood)+'/'+str(poke.hp), (680,120+l),20)
                    
                    l+=30
                bag_surf.blit(BAG_IMGAE['arrow_right'], (485,117+29*interface.choose_inside)) 
               
        return bag_surf

    def draw_bag_items(self,bag_surf, interface):
        if len(interface.items) is not 0 :
            index = 0
            for i in interface.items:         
                bag_surf.blit(pygame.transform.scale(i.image,(50,50)), (350,35+index*60)) #  上方圖片
                display_text(bag_surf, i.name, (425,50+index*60), 32)    
                display_text(bag_surf, 'X'+ str(i.num), (700,50+index*60), 32) # 幾個 ex. X5 
                index += 1
                
            bag_surf.blit(pygame.transform.scale(interface.items[self.current_item].image,(50,50)),(35,500)) # 下方圖片
            display_text(bag_surf, interface.items[self.current_item].description, (150, 500), 32) # 下方圖片說明
            pygame.draw.rect(bag_surf, (255, 0, 0), ((290, 25+(self.current_item*63)), (485, 65)), 5)

    def add_item(self, new_item): 
        if new_item.type is 'props':
            for item in self.interfaces[0].items:
                if new_item.name is item.name:
                    item.num += new_item.num
                    return 

            self.interfaces[0].items.append(new_item)

        if new_item.type is 'balls':
            for item in self.interfaces[1].items:
                if new_item.name is item.name:
                    item.num += new_item.num
                    return 

            self.interfaces[1].items.append(new_item)

    def use_props(self):
        self.use = False
        interface = self.interfaces[self.current_interface]
        props = interface.items[self.current_item]
        if interface.name == 'Poké balls': return True, props
        elif interface.name == 'Items':
            if props.name is 'Potion': 
                props.num -= 1
                self.p_list[interface.choose_inside].remain_blood += 20
                if self.p_list[interface.choose_inside].remain_blood > \
                   self.p_list[interface.choose_inside].hp:
                    self.p_list[interface.choose_inside].remain_blood = \
                    self.p_list[interface.choose_inside].hp

        return False, None

    def transaction(self) :     
        new_item = Items('PokeBall', 1, 'Catching wild Pokémon props')
        self.add_item(new_item)

            
