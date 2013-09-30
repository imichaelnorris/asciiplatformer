import curses

class Location(tuple):
    def __add__(self, t):
        return Location([self[0] + t[0], self[1] + t[1]])

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.refresh()

HEIGHT, WIDTH = stdscr.getmaxyx()
loc = WIDTH//2, HEIGHT//2
loc = Location(loc)
RIGHT = Location([1, 0])
LEFT = Location([-1, 0])
UP = Location([0, 1])
DOWN = Location([0, -1])

class Weapon(object):
    def __init__(self, char):
        self.wld = char[0]
        self.atk = char[1]
    def wield(self):
        return self.wld
    def attack(self):
        return self.atk

class Player(object):
    '''add player state so I can decide if it should "walk" based on if it's changed spaces'''
    def __init__(self, curse_ref, loc=None):
        self.loc = loc
        self.curse_ref = curse_ref
        self.state = 0
        self.wield = True
        self.attack = False
        self.weapon = Weapon(['|', '_'])

    def setAttack(self, atk=False):
        self.attack = atk

    def draw(self, loc=None):
        '''Draw player from heart being loc'''
        if (loc == None):
            loc = self.loc
        stdscr.addch(loc[1], loc[0], 77)
        stdscr.addch(loc[1]-1, loc[0], 79)
        if (self.wield):
            if not self.attack:
                stdscr.addch(loc[1]-1, loc[0]+1, self.weapon.wield())
            else:
                stdscr.addch(loc[1]-1, loc[0]+1, self.weapon.attack())

        if self.state:
            stdscr.addch(loc[1]+1, loc[0]+1, 92)
            stdscr.addch(loc[1]+1, loc[0]-1, 47)
            self.state = False
        else:
            stdscr.addch(loc[1]+1, loc[0], 124)
            #stdscr.addch(loc[1]+1, loc[0]-1, 124)
            self.state = True

def check_loc(location, size=(3, 3, 2, 2)):
    '''size is (height, width), (abs position of middle from topleft corner)'''
    if (location[0] < (WIDTH - size[0] + size[2])) and location[0] - size[0] + size[2] >= 0:
        if (location[1] < (HEIGHT - size[1] + size[3])) and location[1]- size[1] + size[3]>= 0:
            return True
    return False

curses.curs_set(False)
player = Player(curses)
locOld = None

#call function if a key not in the dict has been pressed
#for now, delete after I call, but I can add differing functionality
# for different types of events
functionCallMap = {}

key = ''
try :
    while key != 27:
        if len(functionCallMap) != 0:
            if not functionCallMap.has_key(key):
                for i in functionCallMap: functionCallMap[i]()
        stdscr.clear()
        stdscr.refresh()
        #stdscr.addch(loc[1], loc[0], 46)
        player.draw(loc)
        key = stdscr.getch()
        stdscr.refresh()
        locOld = loc
        if key == curses.KEY_RIGHT and check_loc(loc+RIGHT): 
            loc = loc + RIGHT
        elif key == curses.KEY_LEFT and check_loc(loc+LEFT): 
            loc = loc + LEFT
        elif key == curses.KEY_UP and check_loc(loc+DOWN): 
            loc = loc + DOWN
        elif key == curses.KEY_DOWN and check_loc(loc+UP): 
            loc = loc + UP
        elif key == 97:
            player.attack = True
            functionCallMap[97] = player.setAttack
except Exception as e:
    print e.args, e.message, e
    raise Exception("something happened")
finally:
    curses.curs_set(True)
    curses.endwin()
