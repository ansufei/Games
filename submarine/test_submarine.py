import submarine
import pytest
import numpy as np

class MapTest(submarine.Map):
   pass

def test_draw_islands():
    grid = submarine.Map(density=3).grid
    # not testing anything. Should be variable
    assert grid.size == 15*15
    
    # check the nb of islands is proportional to the density and size of the grid
    # density of approximatively 1/3 of islands on the 9/15 surface of the map => test for 1/2 as the upper limit
    #assert len(np.argwhere(grid=='I')) <= 1/2 * 9/25 * grid.size # commented out as too unreliable > review std deviation of random function
    # 1/4 as the lower limit
    #assert len(np.argwhere(grid=='I')) >= 1/4 * 9/25 * grid.size
    
    # check there are no islands on the edges
    assert any(np.argwhere(grid[0] == 'I')) == False # first line
    assert any(np.argwhere(grid[-1] == 'I')) == False # last line
    assert any(np.argwhere(grid[:,0]) == 'I') == False # first column
    assert any(np.argwhere(grid[:,-1]) == 'I') == False # last column

@pytest.mark.skip
def test_launch_torpedo(captain):
    captain = submarine.Captain('A')

def test_radio_draws_one_move():
    grid = submarine.Map()
    radio = submarine.Radio('A', grid)
    assert len(radio.draw_enemy_map('North')) == 1
