import pygame, sys, os

TILE_WIDTH = 50
TILE_HEIGHT = 85
TILE_FLOOR_HEIGHT = 40
X_RANGE, Y_RANGE = 800,600

EXITS = {1:{ (7,5): 2, (4,6): 3 }, 
         2:{ (0,6): 1, (7,7): 4 }, 
         3:{ (9,0): 1 }, 
         4:{ (2,0): 2 } } 
        
CONVERSE_EXITS = {1:{ 2: (7,5), 3: (4,6) },
                  2:{ 1: (0,6), 4: (7,7) },
                  3:{ 1: (9,0) },
                  4:{ 2: (2,0) } }

TRIGGER_DIR = {1: { 2:'DOWN', 3:'RIGHT'},
               2: { 1:'UP', 4:'RIGHT'},
               3: { 1:'LEFT'},
               4: { 2:'LEFT'} }


class Map() :
    x_border = y_border = False
    def __init__(self, map_num, from_map_num):
        self.map_num = map_num
        self.map_data = MAPS[map_num]
        self.map_midth = len(self.map_data[0])
        self.map_height = len(self.map_data)
        self.exits = EXITS[map_num]
        self.trigger_dir = TRIGGER_DIR[map_num]

        if from_map_num is -1:
            self.x_screen = 2
            self.y_screen = 1
        else :
            tmp = CONVERSE_EXITS[map_num][from_map_num]
            self.x_screen = tmp[0]
            self.y_screen = tmp[1]

    def draw_map( self, player, selectors):
        """Draws the map to a Surface object, including the player's position"""

        # map_surf will be the single Surface object that the tiles are drawn on,
        # by doing so it is easy to position the entire map on the BASE_SURF object

        # First, the width and height must be calculated.    
        map_surf_w = self.map_midth * TILE_WIDTH
        map_surf_h = (self.map_height-1) * TILE_FLOOR_HEIGHT + TILE_HEIGHT
        map_surf = pygame.Surface((map_surf_w, map_surf_h))
        map_surf.blit(pygame.transform.scale(SCENSE_IMAGES['sea'], (X_RANGE,Y_RANGE)),(0,0))   # start with a blank color on the surface.

        # Draw the tile sprites onto this surface.
        for r in range(len(self.map_data)):
            for c in range(len(self.map_data[r])):
                space_rect = pygame.Rect((c * TILE_WIDTH, r * TILE_FLOOR_HEIGHT, TILE_WIDTH, TILE_HEIGHT))

                if self.map_data[r][c] in TILE_DEFINITION:
                    base_tile = TILE_DEFINITION[self.map_data[r][c]]

                # First draw the base ground/wall tile.
                    map_surf.blit(base_tile, space_rect)             

                for item in selectors:
                    if (r, c) == item.pos:
                        map_surf.blit(SCENSE_IMAGES['selector'], space_rect)
                        
                # Last draw the player on the board.
                if (r, c) == player.pos:
                    map_surf.blit(SCENSE_IMAGES['boy'], space_rect)
        if map_surf_w < X_RANGE and map_surf_h < Y_RANGE: return map_surf, True
        else : return map_surf, False

    def make_move(self, player, move_to):
        offset = (0,0)

        if move_to == 'UP':
            offset = (-1,0)
        elif move_to == 'DOWN':
            offset = (1,0)
        elif move_to == 'LEFT':
            offset = (0,-1)
        elif move_to == 'RIGHT':
            offset = (0,1)

        # TODO: compute the position that the player want to move
        # TODO: check if that position is on the floor
        tmp_player_pos = (offset[0] + player.pos[0],offset[1] + player.pos[1])
        if tmp_player_pos[0] >= self.map_height or tmp_player_pos[1] >= self.map_midth  or \
        tmp_player_pos[0] < 0 or tmp_player_pos[1] < 0 or \
        self.map_data[tmp_player_pos[0]][tmp_player_pos[1]] == '#' or \
        self.map_data[tmp_player_pos[0]][tmp_player_pos[1]] == 'x':
            return
                
        player.pos = tmp_player_pos
        if player.pos[0]* TILE_FLOOR_HEIGHT < Y_RANGE//2 : self.y_screen = 0   
        elif player.pos[0]* TILE_FLOOR_HEIGHT > (self.map_height-1)*TILE_FLOOR_HEIGHT+TILE_HEIGHT-Y_RANGE/2 : 
            self.y_screen = self.y_screen   
            self.y_border = True
        else : 
            if self.y_border : self.y_border = False
            else :self.y_screen -= offset[0]

        if player.pos[1]* TILE_WIDTH < X_RANGE//2 : self.x_screen = 0
        elif player.pos[1]* TILE_WIDTH > (self.map_midth-1)*TILE_WIDTH-X_RANGE//2 : 
            self.x_screen = self.x_screen
            self.x_border = True
        else : 
            if self.x_border : self.x_border = False
            else : self.x_screen -= offset[1]

    def get_screen_move(self) :
        return (self.x_screen* TILE_WIDTH,self.y_screen* TILE_FLOOR_HEIGHT)

dir_path = os.path.dirname(os.path.abspath(__file__))
image_path = dir_path+'/../image/'

SCENSE_IMAGES = {'selector': pygame.image.load(image_path+'Selector.png'),
              'corner': pygame.image.load(image_path+'Wall_Block_Tall.png'),
              'wall': pygame.image.load(image_path+'Wood_Block_Tall.png'),
              'inside floor': pygame.image.load(image_path+'Plain_Block.png'),
              'grass': pygame.image.load(image_path+'Grass_Block.png'),
              'boy': pygame.image.load(image_path+'boy.png'),
              'rock': pygame.image.load(image_path+'Rock1.png'),
              'sea': pygame.image.load(image_path+'sea.png')}

TILE_DEFINITION = {'x': SCENSE_IMAGES['corner'],
               '#': SCENSE_IMAGES['wall'],
               'o': SCENSE_IMAGES['inside floor'],
               'M': SCENSE_IMAGES['grass'],
               '1': SCENSE_IMAGES['rock'],
               }

game_map = [ [' ',' ',' ',' ',' ',' ',' '],
           ['x','#','#','#','#','x',' '],
           ['#','o','o','o','o','#','x'],
           ['#','o','o','M','M','o','#'],
           ['#','o','M','M','M','o','o'],
           ['#','o','o','M','M','o','#'],
           ['#','o','o','o','o','o','#'],
           ['x','#','#','#','#','o','x']]

game_map2 = [['o','o','#','#','#','o','o','o'],
            ['#','#','#','o','o','o','#','o'],
            ['#','o','o','o','o','o','#','o'],
            ['#','#','#','o','o','o','#','o'],
            ['#','o','#','#','o','o','#','#'],
            ['#','o','#','o','o','o','#','#'],
            ['#','o','o','o','o','o','o','#'],
            ['#','o','o','o','o','o','o','o'],
            ['#','#','#','#','#','#','#','#']]

game_map3 = [['M','M','#','#','#','#','#','M','M','M','#','#','#','#','#','M','#','#','M'],
            ['#','o','o','#','#','M'],
            ['#','o','o','#','#','M'],
            ['#','o','o','#','#','M'],
            ['#','o','o','#','#','M'],
            ['#','o','o','#','#','M'],
            ['#','o','o','#','#','M'],            
            ['#','o','o','#','#','M'],
            ['#','o','o','#','#','M'],
            ['o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','#','#','#','#','#','#','#','M','M','#','#','#','#','#','M','M','#','M']]

game_map4 = [['M','M','#','#','#','#','#','M','M','M','#','#','#','#','#','M','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['o','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','o','o','o','o','#','o','o','o','o','o','o','o','o','#','#','M'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','o','o','M','M','o','o','o','o','M','M','o','o','o','o','M','M','o','o'],
            ['#','#','#','#','#','#','#','#','M','M','#','#','#','#','#','M','M','#','M']]

MAPS = {1:game_map, 2:game_map2, 3:game_map3,4:game_map4}