from smb_py.room import PlatformerRoom
import lib_py.engine as engine
import smb_py.factories as fact
import smb_py.builder as b
import lib_py.components as compo
import lib_py.shape as sh
from lib_py.entity import Entity
from lib_py.components import ShapeGfx
from lib_py.shape import Polygon
import example
import yaml

def builder():
    r = PlatformerRoom(
        id = 'world1_1', 
        width = 256, 
        height = 256, 
        worldWidth = 224, 
        worldHeight = 16, 
        playerModel = 'cody', 
        startPos = [32, 32])
    
    # r.main.add (b.line(x=0,y=0,A=[128,0],B=[128,50]))
    # r.main.add (b.line(x=0,y=0,A=[128,50],B=[256,100]))
    # r.main.add (b.line(x=0,y=0,A=[256,100],B=[256,200]))
    # r.main.add (b.line(x=0,y=0,A=[0,200],B=[256,200]))
    # r.main.add (b.line(x=0,y=0,A=[0,200],B=[0,0]))
    shape = Polygon([0, 0, 512, 0, 512, 100, 0, 100])
    r.main.add (b.poly(0, 0, shape))
    e = Entity()
    e.pos = [0,0,-5]
    e.addComponent (ShapeGfx(shape = shape, texture = 'gfx/block1.png', x0=2, repx=25, repy=25,slantx = 0.2 ))
    r.main.add(e)
    r.main.add (b.makeFoe('andore', 80, 32, 0.5, 5))
    #ba=Entity()
    #ba.addComponent(compo.ShapeGfxColor(shape=sh.Rect(200,100), color=[255,255,255,255]))
    #r.main.add(ba)

    # with open(example.dir+ '/rooms/world1_1.yaml') as f:
    #     rooms = yaml.load(f, Loader=yaml.FullLoader)
    #     for a in rooms['room']:
    #         f = a['template'][0]
    #         args = a['template'][1:]
    #         print (args)
    #         method_to_call = getattr(fact, f, None)
    #         if method_to_call:
    #             template = method_to_call(*args)
    #             print (f + ' found')
    #             for im in a['d']:
    #                 print (im)
    #                 e = template(*im)
    #                 r.addToDynamicWorld(e)
    #         else:
    #             print (f + ' not found')

    return r

engine.addRoom (id = 'world1_1', f=builder)
