import pygame, sys, os

TILE_WIDTH = 50
TILE_HEIGHT = 85
TILE_FLOOR_HEIGHT = 40
X_RANGE, Y_RANGE = 800,600

'''
    1: start_map
    2: forest_map1
    3: forest_map2
    4: forest_map3
    5: forest_map4
    6: bridge_map
    7: boss_map 
'''
EXITS = {1:{ (11,4): 2}, 
         2:{ (0,2): 1, (8,15): 3 }, 
         3:{ (5,0): 2, (14,4): 4 }, 
         4:{ (0,4): 3, (15,7): 5 },
         5:{ (0,6): 4, (11,15): 6 },
         6:{ (6,0): 5, (6,21): 7 },
         7:{ (6,0): 6} } 
        
CONVERSE_EXITS = {1:{ 2: (11,4) },
                  2:{ 1: (0,2), 3: (8,15) },
                  3:{ 2: (5,0), 4: (14,4) },
                  4:{ 3: (0,4), 5: (15,7) },
                  5:{ 4: (0,6), 6: (11,15) },
                  6:{ 5: (6,0), 7: (6,21) },
                  7:{ 6: (6,0)} }

TRIGGER_DIR = {1: { 2:'DOWN'},
               2: { 1:'UP', 3:'RIGHT'},
               3: { 2:'LEFT', 4:'DOWN'},
               4: { 3:'UP', 5:'DOWN'},
               5: { 4:'UP', 6:'RIGHT'},
               6: { 5:'LEFT', 7:'RIGHT'},
               7: { 6:'LEFT'} }

CHALLENGER_SPOT= {2:[(12,5),(8,11)],
                  3:[(4,6) ,(12,4)],
                  4:[(13,6)],
                  5:[(7,5),(10,14)]}

CHALLENGE_TRIGGER={2:[(13,5), (9,11)],
                    3:[(5,6), (13,4)],
                    4:[(13,7)],
                    5:[(7,6), (11,14)],
                    7:[(6,4), (6,10), (6,16), (6,22)]}

# test
# CHALLENGE_TRIGGER={7:[(6,4), (6,10), (6,16), (6,22)]}

SELL_TRIGGER = { 1 :[(6,3)], 4:[(9,7)], 6:[(6,17)]}
RECOVER_TRIGGER={ 1 :[(6,5)], 6:[(6,19)]}

SELLER_SPOT = { 1 :[(5,3)], 4:[(9,8)], 6:[(5,17)]}
DOCTOR_SPOT = { 1 :[(5,5)], 6:[(5,19)] }

PRINCESS_SPOT = {7:[(5,4), (5,10), (5,16), (5,22)]}

class Map() :
    x_border = y_border = False
    challenge = False
    def __init__(self, map_num, from_map_num):
        self.map_num = map_num
        self.map_data = MAPS[map_num]
        self.map_midth = len(self.map_data[0])
        self.map_height = len(self.map_data)
        self.exits = EXITS[map_num]
        self.trigger_dir = TRIGGER_DIR[map_num]

        if from_map_num is -1:
            self.x_screen = 7
            self.y_screen = 4
        else :
            tmp = CONVERSE_EXITS[map_num][from_map_num]
            self.x_screen = tmp[0]
            self.y_screen = tmp[1]

    def is_npc_spot(self, player):
        if self.map_num in SELL_TRIGGER and player.pos in SELL_TRIGGER[self.map_num]:
            return 'seller'
        elif self.map_num in RECOVER_TRIGGER and player.pos in RECOVER_TRIGGER[self.map_num]:
            return 'doctor'
        else :None

    def delete_challenge_spot(self):
        game_over = False
        if self.map_num is 7:
            self.map_data[CHALLENGE_TRIGGER[self.map_num][0][0]][CHALLENGE_TRIGGER[self.map_num][0][1]+1] = 'o'
            if len(self.map_data[CHALLENGE_TRIGGER[self.map_num]]) is 1:
                game_over = True
        del CHALLENGE_TRIGGER[self.map_num][0]
        return game_over

    def draw_map( self, player, selectors):
        """Draws the map to a Surface object, including the player's position"""

        # map_surf will be the single Surface object that the tiles are drawn on,
        # by doing so it is easy to position the entire map on the BASE_SURF object

        # First, the width and height must be calculated.    
        map_surf_w = self.map_midth * TILE_WIDTH
        map_surf_h = (self.map_height-1) * TILE_FLOOR_HEIGHT + TILE_HEIGHT
        map_surf = pygame.Surface((map_surf_w, map_surf_h))
        map_surf.blit(pygame.transform.scale(SCENSE_IMAGES['sea'], (X_RANGE,Y_RANGE)),(0,0))   # start with a blank color on the surface.
        map_surf.blit(pygame.transform.scale(SCENSE_IMAGES['sea'], (X_RANGE,Y_RANGE)),(X_RANGE,0))
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
                    if self.map_num in CHALLENGE_TRIGGER and (r,c) in CHALLENGE_TRIGGER[self.map_num]:
                        self.challenge = True
                    else: self.challenge = False

                if self.map_num in CHALLENGER_SPOT and (r, c) in CHALLENGER_SPOT[self.map_num]:
                    map_surf.blit(SCENSE_IMAGES['challenger'], space_rect)

                if self.map_num in SELLER_SPOT and (r, c) in SELLER_SPOT[self.map_num]:
                    map_surf.blit(SCENSE_IMAGES['seller'], space_rect)

                if self.map_num in DOCTOR_SPOT and (r, c) in DOCTOR_SPOT[self.map_num]:
                    map_surf.blit(SCENSE_IMAGES['doctor'], space_rect)

                if self.map_num in PRINCESS_SPOT and (r, c) in PRINCESS_SPOT[self.map_num]:
                    map_surf.blit(SCENSE_IMAGES['princess'], space_rect) 

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
        self.map_data[tmp_player_pos[0]][tmp_player_pos[1]] == 'x' or \
        self.map_data[tmp_player_pos[0]][tmp_player_pos[1]] == '1' or \
        self.map_data[tmp_player_pos[0]][tmp_player_pos[1]] == 'Tt' or \
        self.map_data[tmp_player_pos[0]][tmp_player_pos[1]] == 'Ts':
            return
                
        player.pos = tmp_player_pos
        if player.pos[0]* TILE_FLOOR_HEIGHT < Y_RANGE//2 : self.y_screen = 0   
        elif player.pos[0]* TILE_FLOOR_HEIGHT > (self.map_height-1)*TILE_FLOOR_HEIGHT+TILE_HEIGHT-Y_RANGE/2 : 
            self.y_screen = -(((self.map_height-1)*TILE_FLOOR_HEIGHT+TILE_HEIGHT-Y_RANGE)//TILE_FLOOR_HEIGHT)
        else : 
            self.y_screen = (Y_RANGE//2-player.pos[0]* TILE_FLOOR_HEIGHT)//TILE_FLOOR_HEIGHT

        if player.pos[1]* TILE_WIDTH < X_RANGE//2 : self.x_screen = 0
        elif player.pos[1]* TILE_WIDTH > (self.map_midth-1)*TILE_WIDTH-X_RANGE//2 : 
            self.x_screen = -(((self.map_midth-1)*TILE_WIDTH-X_RANGE)//TILE_WIDTH+1)
        else : 
            self.x_screen = (X_RANGE//2-player.pos[1]* TILE_WIDTH)//TILE_WIDTH-1
        self.first = False

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
              'challenger': pygame.image.load(image_path+'horngirl.png'),
              'princess': pygame.image.load(image_path+'princess.png'),
              'doctor': pygame.image.load(image_path+'catgirl.png'),
              'seller': pygame.image.load(image_path+'pinkgirl.png'),
              'rock': pygame.image.load(image_path+'Rock1.png'),
              'sea': pygame.image.load(image_path+'sea.png')}

TREE_IMAGES = {'tree_tall': pygame.image.load(image_path+'Tree_Tall.png'),
               'tree_short': pygame.image.load(image_path+'Tree_Short.png'), 
               'tree_ugly': pygame.image.load(image_path+'Tree_Ugly.png'), }

TILE_DEFINITION = {'x': SCENSE_IMAGES['corner'],
               '#': SCENSE_IMAGES['wall'],
               'o': SCENSE_IMAGES['inside floor'],
               'M': SCENSE_IMAGES['grass'],
               '1': SCENSE_IMAGES['rock'],
               'Tt': TREE_IMAGES['tree_tall'],
               'Ts': TREE_IMAGES['tree_short'],
               'Tu': TREE_IMAGES['tree_ugly'],
               }

start_map = [[' ',' ',' ',' ','#',' ',' ',' ',' '],
             [' ',' ',' ','#','#','#',' ',' ',' '],
             [' ',' ','#','#','#','#','#',' ',' '],
             [' ','#','#','#','o','#','#','#',' '],
             ['#','#','#','o','o','o','#','#','#'],
             [' ','#','o','o','o','o','o','#',' '],
             [' ','#','o','o','o','o','o','#',' '],
             [' ','#','o','o','o','o','o','#',' '],
             [' ','#','o','o','o','o','o','#',' '],
             [' ','#','o','o','o','o','o','#',' '],
             [' ','#','o','o','o','o','o','#',' '],
             [' ','#','#','1','o','1','#','#',' '],
            ]

boss_map =  [[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
             ['x','x','x','x','x','#','x','x','x','x','x','#','x','x','x','x','x','#','x','x','x','x','x','#'],
             ['x','x','x','x','x','#','x','x','x','x','x','#','x','x','x','x','x','#','x','x','x','x','x','#'],
             ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
             ['#','o','o','o','o','#','o','o','o','o','o','#','o','o','o','o','o','#','o','o','o','o','o','#'],
             ['o','o','o','o','o','#','o','o','o','o','o','#','o','o','o','o','o','#','o','o','o','o','o','#'],
             ['#','o','o','o','o','#','o','o','o','o','o','#','o','o','o','o','o','#','o','o','o','o','o','#'],
             ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
             ['x','x','x','x','x','#','x','x','x','x','x','#','x','x','x','x','x','#','x','x','x','x','x','#'],
             ['x','x','x','x','x','#','x','x','x','x','x','#','x','x','x','x','x','#','x','x','x','x','x','#'],
             [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
             [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
             ]

forest_map1 = [['Tt','Tt','o','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Ts','o' ,'Ts','Ts','Ts','Ts','Ts','Ts','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Ts','o' ,'Ts','Ts','Ts','Ts','Ts','Ts','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','x' ,'o' ,'x' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','M' ,'M' ,'M' ,'1' ,'1' ,'1' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt'],
              ['Tt','M' ,'M' ,'M' ,'M' ,'M' ,'1' ,'M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt'],
              ['Tt','M' ,'M' ,'M' ,'M' ,'M' ,'1' ,'M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','x' ],
              ['Tt','Tt','M' ,'M' ,'M' ,'M' ,'1' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'o' ],
              ['Tt','Tt','M' ,'M' ,'M' ,'M' ,'Tt','o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'x' ],
              ['Tt','Tt','o' ,'Tt','Tt','Tt','Tt','M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt'],
              ['Tt','o' ,'o' ,'o' ,'o' ,'Tt','Tt','M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt'],
              ['Tt','Tt','o' ,'o' ,'o' ,'o' ,'o', 'M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','o' ,'o' ,'o' ,'o', 'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
            ]

forest_map2 = [['Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','M' ,'M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt','Tt','Tt'],
              ['x' ,'Tt','o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt','Tt'],
              ['o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'Tt','Tt','M' ,'M' ,'Tt','Tt','Tt','Tt','Tt'],
              ['x' ,'o' ,'o' ,'o' ,'Tt','Tt','o' ,'Tt','Tt','1' ,'1' ,'1' ,'M' ,'M' ,'Tt','Tt'],
              ['Tt','M' ,'M' ,'Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'Tt','Tt'],
              ['Tt','M' ,'Tt','Tt','Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','M' ,'M' ,'M' ,'M' ,'Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt'],
              ['Tt','Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'Tt'],
              ['Tt','Tt','Tt','Tt','o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'1' ,'Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','x' ,'o' ,'x' ,'1' ,'1' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
             ]

forest_map3 = [['Tt','Tt','Tt','x' ,'o' ,'x' ,'1' ,'1' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','M' ,'M' ,'M' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt'],
              ['Tt','Tt','M' ,'M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt'],
              ['Tt','Tt','M' ,'M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'M' ,'Tt'],
              ['Tt','M' ,'M' ,'M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'Tt'],
              ['Tt','Tt','M' ,'M' ,'M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt'],
              ['Tt','Tt','Tt','M' ,'M' ,'M' ,'M' ,'M' ,'Tt','M' ,'Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','o' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['1' ,'1' ,'M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'Tt','Tt','Tt'],
              ['1' ,'1' ,'M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'Tt','Tt'],
              ['1' ,'1' ,'M' ,'M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'M' ,'M' ,'M' ,'Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','x' ,'o' ,'x' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ]

forest_map4 = [['Tt','Tt','Tt','Tt','Tt','Tt','o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','o' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','x' ,'o' ,'x' ,'Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'Ts','Ts','Ts','Ts','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','o' ,'o' ,'M' ,'M' ,'M' ,'M' ,'#' ,'#' ,'#' ,'#' ,'#' ],
              ['Tt','Tt','Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'#' ],
              ['Tt','Tt','Tt','Tt','Tt','o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'x' ],
              ['Tt','Tt','Tt','Tt','Tt','M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ],
              ['Tt','Tt','Tt','Tt','Tt','M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'x' ],
              ['Tt','Tt','Tt','Tt','Tt','M' ,'M' ,'M' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'#' ],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','M' ,'M' ,'M' ,'M' ,'#' ,'#' ,'#' ,'#' ,'#' ],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','M' ,'M' ,'M' ,'M' ,'Ts','Ts','Ts','Ts','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Ts','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ['Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt','Tt'],
              ]

bridge_map = [
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              ['#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#', '#' ,'#' ],
              ['x' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'x' ],
              ['o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ],
              ['x' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'o' ,'x' ],
              ['#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#' ,'#', '#' ,'#' ],
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              [' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ' ,' ', ' ' ,' ' ],
              ]

MAPS = {1:start_map, 2:forest_map1, 3:forest_map2, 4:forest_map3, 5:forest_map4, 6:bridge_map, 7:boss_map}