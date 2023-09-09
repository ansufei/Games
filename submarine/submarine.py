import numpy as np
import random
import math

class Map:
    def __init__(self, density = 3):
        self.density = density / 9
        self.grid = self.draw_islands()
        self.islands = np.argwhere(self.grid=='I').tolist()

    def draw_islands(self):
        # create grid with n random obstacles distributed around the center of the grid squares
        subs = {key : None for key in range(1,10)} # dictionary of sectors
        for key in subs:
            square = np.random.choice(['','I'], p=[1-self.density, self.density], size=(9)).reshape(3, 3) # 3 by 3 grid with islands randomly distributed
            subs[key] = np.pad(square, (1,1), mode='empty') # padded by a layer of 1 cell all around => dimension 5 x 5
        # append the sectors (subs) side by side and from top-left to bottom-right
        grid = np.concatenate((subs[1],subs[2],subs[3]), axis=1)
        grid = np.concatenate((grid, np.concatenate((subs[4],subs[4],subs[6]), axis=1)),axis=0)
        grid = np.concatenate((grid, np.concatenate((subs[7],subs[8],subs[9]), axis=1)),axis=0)
        return grid
    
    def initial_position(self, coord = []):
        '''at the start of the game, the captain places the boat on the location of his choice on the map (not on an island)
        define empty initial coordinates to allow for a manual choice - only check that it's not on an island.
        '''
        np.place(self.grid, self.grid!='I', '') # erase anything that isn't an island - reset the map from a previous game
        available_positions = np.argwhere(self.grid=='') # returns an array of coordinate tuples of all cells that are not 'taken' (island or mine)
        if coord:
            if not coord in available_positions:
                print('You cannot place the boat on an island or outside the map')
        else:
            coord = random.choice(available_positions) # select a cell randomly within the above array
        self.grid[coord[0], coord[1]] = 'X' # mark with a X the current location in the grid
        return coord
    
class Boat:
    def __init__(self, team):
        self.damages = 0

    def draw_outline(self):
        pass

class Captain:
    '''
    - DONE Decides of the initial position of the boat
    - DONE Gives directions for 1 cell orthogonal moves
    - TO COMPLETE decides to resurface
    - drops a mine
    - TO COMPLETE launches a torpedo
    - launches a drone
    - activates the sonar
    - activates silence
    - waits for teammates to be ready
    - gives sector in case of resurface or sonar attack
    - DONE gives approximate position in case of a sonar attack by the enemy
    '''

    def __init__(self,team, raw_map, coord = []):
        self.team = team
        self.map = raw_map.grid
        self.islands = raw_map.islands
        self.x0, self.y0 = raw_map.initial_position(coord)
        self.x, self.y = self._current_position()
        print('Coordinates:', self.x, self.y)

    def _current_position(self):
        return np.argwhere(self.map == 'X')[0]

    def order_move(self, direction):
        '''Position the X one cell adjacent to the previous one in the direction given.
        If the boat is already on the edge of the map, or if the move would run the boat into an island, a mine or its previous route, abort and print an error'''
        # initialize position to current position
        x = self.x
        y = self.y
        # calculate propose coordinates with a move of one cell in the given direction
        if direction == 'HEAD NORTH' and x > 0:
            x -= 1
        elif direction == 'HEAD SOUTH' and x < len(self.map) - 1:
            x += 1
        elif direction == 'HEAD WEST' and y > 0:
            y -= 1
        elif direction == 'HEAD EAST' and y < len(self.map) - 1:
            y += 1
        # error message if boat on the edge of the map
        else:
            print('Team {}: The move {} is not allowed as the boat is on the edge of the map'.format(self.team, direction))
            return self.map
        # check that the proposed coordinates are free from obstacle
        if self.map[x,y] == '':
            print('Team {} : {}'.format(self.team, direction))
            # change symbol for last position that is now part of the route
            self.map[self.x,self.y] = '-'
            # assign symbol X to new current position
            self.map[x,y] = 'X'
            self.x, self.y = (x, y)
        else:
            print('Team {}: The move {} is not allowed as there is an obstacle on the way'.format(self.team, direction))
        return self.map

    def order_surface(self):
        '''While surfacing might be the only available move, it is not set automatically but must be a decision taken by the captain
        (if an AI, after trying all the other choices if necessary). 
        Actions:
        - resetting of the route
        - announcing the current sector to the enemy
        - completing the outline of the boat
        - waiting for feedback to resume dive'''
        print('Team {}: SURFACE'.format(self.team))
        # reset the route
        self._erase_route_after_surface()
        # announce the current sector to the enemy
        print('Team {}: ATTENTION, WE ARE SURFACING IN SECTOR {}'.format(self.team, self.give_sector()))
        # TO DO complete the outline of the boat
        print('Team {}: DIVE'.format(self.team))
        return self.map

    def _erase_route_after_surface(self):
        '''remove all the '-' signs indicating the route traveled - only keep the current position marked by an X'''
        return np.place(self.map, self.map=='-', '')
    
    def give_sector(self):
        '''sectors are subdivisions of the grid, of size 5 x 5, numeroted from 1 to 9 from the top left to the bottom right'''
        sX = math.ceil((self.x + 1) / 5) - 1 # as there are 5 x 5 cells in each sector (+1 / - 1 to convert from and to 0-indexing)
        sY = math.ceil((self.y + 1) / 5) - 1
        return np.arange(1,10).reshape(3,3)[sX,sY]

    def give_position_sonar(self):
        '''two pieces of information on coordinates/sector, except that one is correct and the other is not
        the wrong coordinate is chosen randomly among available positions that are not the correct one
        [optional: together the exact and wrong coordinate cannot land on an island - if they represent a row + column]
        Learning opportunity for AI to overwrite the random choice:
        - give exact + wrong that together could pass for correct, e.g. x and sector that do intersect
        - not adjacent to real location
        - attract enemy boat close to a mine
        - plausible coordinates given what we think the enemy knows about us
        '''
        # pick one correct, one wrong randomly out of the 3 possible types of positions (they must be of different types)
        coord_choices = ['row','column','sector']
        correct_coord, wrong_coord = random.sample(coord_choices, 2)
        # set default wrong = sector - any sector but current one
        wrong = random.choice([x for x in range(1,10) if not x == self.give_sector()])
        # incorrect row or column picked randomly from the correct line (row or column), skipping the actual correct value
        if wrong_coord == 'row':
            wrong = np.random.choice(np.where(self.map[:,self.y] != 'X')[0])
        elif wrong_coord == 'column':
            wrong = np.random.choice(np.where(self.map[self.x] != 'X')[0])
        # define correct coordinate from class variables
        if correct_coord == 'row':
            correct = self.x + 1 # 1-indexing
        elif correct_coord == 'column':
            correct = self.y + 1 # 1-indexing
        elif correct_coord == 'sector':
            correct = self.give_sector()
        # randomly print in the correct / wrong or wrong / correct order
        correct_first = correct_coord, correct
        wrong_first = wrong_coord, wrong
        first, second = np.random.permutation((correct_first, wrong_first))
        print('Team {} : WE ARE IN {}, {}'.format(self.team, ', '.join(first), ', '.join(second)))
        return self.map
                    
                    
    def _place_torpedo(self, lst_nodes):
        # missing if ((abs(impact_x - self.x) >= 2) | (abs(impact_y - self.y) >= 2))
        # implement: start the path at the edge of the safe zone
        v = [self.x, self.y]
        path = []
        tried = [v]
        distance = random.choice([3,4])    
        # continue until the path list contains between 2 and 4 values (the tried list gets incremented at every try, the path only at the successful ones)
        while len(path) < distance:
            directions = [[v[0],v[1] - 1],[v[0] + 1, v[1]],[v[0], v[1] + 1],[v[0] - 1, v[1]]] # left, down, right, up
            # start in initial position and choose randomly any direction
            next_node = random.choice(directions)
            # validate that the direction has not been tried before
            if not next_node in tried:
                tried.append(next_node)
                # validate that the direction is allowed
                if next_node in lst_nodes:
                    path.append(next_node)
                    v = next_node
        impact_x, impact_y = path.pop()
        self.map[impact_x,impact_y] = 'T'
        print('Team {} : TORPEDO LAUNCHED, IMPACT IN {}-{}'.format(self.team, impact_x, impact_y))
        return self.map

    def launch_torpedo(self):
        '''max 4 points away while moving in orthogonal directions.
        The islands cannot be on the itinerary
        The torpedo will blow a 3x3 square around the impact point.
        If a mine is in the impact zone, it will be destroyed
        If the boat launching the torpedo is in the impact zone, it will be impacted'''
        print('Team {}: I\'M LAUNCHING A TORPEDO'.format(self.team))
        # define a diamond shape of max distance 4 from current location
        radiation_zone = np.array([self.x,self.y]) + [(x,y) for x in range(-4,5) for y in range(-4,5) if abs(x) + abs(y) <= 4]
        # remove impact points outside the map
        pos_radiation_zone = [k for k in radiation_zone.tolist() if (k[0] >= 0) & (k[1] >= 0)]
        # remove islands from possible impact locations
        free_radiation_zone = [k for k in pos_radiation_zone if not k in self.islands]
        # select a point of impact at random
        return self._place_torpedo(free_radiation_zone)
    
    def drop_mine(self):
        pass

class Radio:
    
    def __init__(self, team, raw_map, coord=[]):
        self.team = team
        self.raw_map = raw_map
        self.map = raw_map.grid
        self.islands = raw_map.islands

    def guess_initial_position_enemy(self, coord=[]):
        return self.raw_map.initial_position(coord)

    def draw_enemy_map(self, direction):
        init = self.guess_initial_position_enemy()
        return [[0,0]]
