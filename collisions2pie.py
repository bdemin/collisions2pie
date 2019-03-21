import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import winsound
from pygame import mixer

        
class Block(object):
    def __init__(self, size, x, mass, v):
        self.mass = mass
        self.height = size
        self.width = self.height
        
        self.x = x
        self.v = v
        
        self.count = 0

        mixer.init()
        self.sound = mixer.Sound('click.wav')

    def draw(self):
        self.patch = Rectangle((self.x, 0), self.width, self.height, fc = 'g')
        return self.patch
    
    def collision(self, other):
        return not((self.x + self.width < other.x) or (self.x > other.x + other.width))
    
    def wall(self):
        if self.x < 0:
            self.v *= -1
            free_channel = mixer.find_channel()
            free_channel.play(self.sound)
        
    def bounce(self, other):
        _sum = self.mass + other.mass
        diff = self.mass - other.mass
        temp_v = (self.v*diff + other.v*2*other.mass)/_sum
        other.v = (self.v*2*self.mass - other.v*diff)/_sum
        self.v = temp_v
        
        self.count += 1
        mixer.find_channel().play(self.sound)

        
fig1 = plt.figure(figsize = (19, 10))
ax1 = fig1.add_subplot(111)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 3)
ax1.set_aspect(1)

block1 = Block(size = 0.5, x = 2, mass = 1, v = 0)
block2 = Block(size = 2, x = 5, mass = 10000000, v = -3)

dt = 0.01
count = 0

def init():
    patches = [block1.draw(), block2.draw()]
    for patch in patches:
        ax1.add_patch(patch)
    
    return block1.patch, block2.patch,


def animate(i):    
    if block1.collision(block2):
        block1.bounce(block2)
        print(block1.count)
    block1.wall()
    block2.wall()
    
    block1.x += dt*block1.v
    block2.x += dt*block2.v
    
    block1.patch.set_x(block1.x)
    block2.patch.set_x(block2.x)
    
    return block1.patch, block2.patch,



fps = 60

anim = animation.FuncAnimation(fig1, animate, interval = 20, repeat = False, init_func = init, blit = True)

plt.show()