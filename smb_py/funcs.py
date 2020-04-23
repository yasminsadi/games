from lib_py.entity import Entity, Sprite
import lib_py.components as compo
import lib_py.shape as sh
import lib_py.actions as act
from lib_py.script import Script
import smb_py.vars as vars
import example

def upgradePlayer():
    vars.state += 1
    if vars.state >= len(vars.stateInfo):
        vars.state = 0
    # update model
    pl = example.get('player')
    pl.setModel(vars.stateInfo[vars.state], 'idle')

def setPlayer(state : int):
    vars.state = state
    pl = example.get('player')
    pl.setModel(vars.stateInfo[state], 'idle')
    


def makePiece(pos, vx, vy, model, parent : example.Wrap1):
    a = Sprite(model = model, pos = pos)
    id = parent.add(a)
    s = Script()
    s.addAction (act.MoveAccelerated (id = id, v0 = [vx, vy], a = [0, 0.5*vars.gravity], yStop=0))
    s.addAction (act.RemoveEntity (id = id))
    #		type = action.remove_object, args = { id = id1}
    example.play(s)

def coinResponse(player:example.Wrap1, coin:example.Wrap1, x, y):
    example.remove(coin.id())

def brickResponse (player : example.Wrap1, brick : example.Wrap1, x, y):
    b = brick.parent()
    brick_id = b.id()
    if vars.state == 0:
        s = Script()
        ystop = b.y()
        s.addAction (act.MoveAccelerated (v0 = [0, 50], a = [0, 0.5 * vars.gravity], yStop = ystop, id = brick_id))
        example.play(s)
    else:
        print ('removing ' + str(brick_id))
        example.remove(brick_id)
        m = example.get('main')
        makePiece(pos = [b.x(), b.y(), 1], vx = 60, vy = 180, model ='brickpiece', parent=m)
        makePiece(pos = [b.x(), b.y(), 1], vx = -60, vy = 180, model ='brickpiece', parent=m)
        makePiece(pos = [b.x(), b.y(), 1], vx = 120, vy = 120, model ='brickpiece', parent=m)
        makePiece(pos = [b.x(), b.y(), 1], vx = -120, vy = 120, model ='brickpiece', parent=m)

def bonusBrickResponse (player: example.Wrap1, brick: example.Wrap1, x, y):
    b = brick.parent()
    info = b.getInfo()
    hitsLeft = info['hitsLeft']
    brick_id = b.id()
    if hitsLeft > 0:
        info['hitsLeft'] -= 1
        s = Script()
        ystop = b.y()
        s.addAction (act.MoveAccelerated (v0 = [0, 50], a = [0, 0.5 * vars.gravity], yStop = ystop, id = brick_id))
        if hitsLeft == 1:
           s.addAction (act.Animate (anim='taken', id=brick_id)) 
        # release the bonus
        def p():
            info['callback'](b.x()/ vars.tileSize + 0.5, b.y() / vars.tileSize)
        s.addAction (act.CallFunc (f = p))
        example.play(s)

def playerHitByEnemy(player : example.Wrap1):
    # if Mario is hit by enemy, what happens depends on whether mario is supermario or not
    #local marioInfo = player:getinfo()
    #local supermario = marioInfo.supermario
    if vars.state > 0:
        setPlayer(0)
        vars.invincibility = True
        # marioInfo.invincible = true
        # factory.mario.change_state(player, 1)
        # player.state = "walk"
        # local act = {
        # 	{ type = action.blink, args = { id = player.id, duration=5, blink_duration= 0.2}},
        # 	{ type = action.callfunc, args = { func = function() marioInfo.invincible=false end }}
        # }
        # local s = script.make(act)
        # monkey.play(s)
    else:
        s = Script()
        s.addAction (act.SetState(state='warp', tag='player', args = {'anim': 'dead'}))
        s.addAction (act.Delay(sec=1))
        s.addAction (act.MoveAccelerated(v0 = [0    , 200], a= [0, vars.gravity], yStop= 0, tag='player'))
        s.addAction (act.RemoveEntity(id = player.id()))
        s.addAction (act.RestartRoom())        
        example.play(s)

def foeIsHit(player : example.Wrap1, foe : example.Wrap1, x, y):
    # decrease foe energy
    info = foe.getInfo()
    info['energy'] -= 1
    if info['energy'] <= 0:
        example.remove(foe.id())
    else:
        foe.setState ('ishit', {})
        vx = 200 if player.x() < foe.x() else -200
        if foe.flipx: 
            vx *= -1
        foe.vx = vx
        print ('ciao')

def updateEnergy():
    a : example.Wrap1 = example.get('energy_label')
    a.setText('ENERGY ' + str(vars.energy))

def updateLives():
    a : example.Wrap1 = example.get('lives_label')
    a.setText('LIVES ' + str(vars.lives))


def goombaResponse (player : example.Wrap1, goomba : example.Wrap1, x, y):
    if vars.invincibility:
        return
    print ('qui')
    if (player.getState() == 'jump' and y > 0 and abs(x) < 0.01):
        s = Script()
        player.vy = 300
        s.addAction (act.SetState (state = 'dead', id = goomba.id() ))
        example.play(s)
        print ('ciao')
    else:
        playerHitByEnemy(player)


def createItem (f: callable, *args):
    def g(player: example.Wrap1, hotspot: example.Wrap1):
        example.remove(hotspot.id())
        m : example.Wrap1 = example.get('main')
        item = f(*args)
        m.add (item)
    return g

def koopaResponse (player : example.Wrap1, koopa : example.Wrap1, x, y):
    if koopa.getState() == 'hide':
        if (player.getState() == 'jump' and y > 0 and abs(x) < 0.01):
            player.vy = 300
        koopa.move(-10 * x, 0, 0)		
        left = 0 if (player.x() <koopa.x()) else 1
        s = Script()
        s.addAction (act.SetState(state='walk2', id=koopa.id(), args = {'left': left}))
        example.play(s)
    else:
        if (player.getState() == "jump" and y > 0 and abs(x) < 0.01):
            player.vy = 300
            s = Script()
            s.addAction (act.SetState(state='hide', id=koopa.id()))
            example.play(s)     
        else:
            playerHitByEnemy(player)


def mushroomResponse (player: example.Wrap1, mushroom: example.Wrap1, x, y):
    example.remove(mushroom.id())
    upgradePlayer()

def warpEnter( player: example.Wrap1, warp: example.Wrap1, x,y):
    info = warp.getInfo()
    # set the warp function
    if 'func' in info:
        vars.warp_func = info['func']

def hotspotEnter (player: example.Wrap1, warp: example.Wrap1, x, y):
    info = warp.getInfo()
    if 'func' in info:
        info['func'](player, warp)


def warpExit (player: example.Wrap1, warp: example.Wrap1, x, y):
    vars.warp_func = None


def warpIn(warpTo : list, newCamBounds : list = None):
    def f():
        vars.warp_func = None
        s = Script()
        s.addAction (act.SetState(tag='player', state='warp'))
        s.addAction (act.Move(speed=50, by =[0,-64], tag='player'))
        if newCamBounds:
            s.addAction (act.ChangeCamBounds('maincam', newCamBounds[0], newCamBounds[1], newCamBounds[2], newCamBounds[3]))
        s.addAction (act.Move(speed=0, to = [warpTo[0] * vars.tileSize, warpTo[1]*vars.tileSize], immediate= True, tag = 'player'))
        s.addAction (act.SetState(tag='player', state='walk'))
        example.play(s)
    return f

def warpUp(warpTo : list, newCamBounds : list = None):
    def f(player, hotspot):
        s = Script()
        s.addAction (act.SetState(tag='player', state='demo', args = { 'left': 0 })),
        s.addAction (act.Delay (sec=1))
        s.addAction (act.SetState(tag='player', state='warp'))
        if newCamBounds:
            s.addAction (act.ChangeCamBounds('maincam', newCamBounds[0], newCamBounds[1], newCamBounds[2], newCamBounds[3]))
        s.addAction (act.Move(speed=0, to = [warpTo[0] * vars.tileSize, warpTo[1]*vars.tileSize], immediate= True, tag = 'player'))
        s.addAction (act.Move(speed=50, by =[0, 64], tag='player'))
        s.addAction (act.SetState(tag='player', state='walk'))
        example.play(s)
    return f


def flag(p, h):
    p.vx = 0
    p.vy = 0
    example.remove(h.id())
    flag = example.get('flag')
    s = Script()
    s.addAction(act.SetState (state = 'warp', tag='player', args = {'anim': 'slide'}), id = 0)
    s.addAction (act.Move (speed = 80, by = [0, -(flag.y()-h.y())], tag='flag'), after= [0])
    s.addAction (act.Move (speed = 80, to = [p.x(), h.y()], tag='player'), after= [0])
    s.addAction (act.SetState(tag='player', state='demo', args = { 'left': 0 })),
    #s.addAction (act.SetState (state='walk', tag='player'))
    example.play(s)

def endlevel(p, h):
    example.remove(p.id())

    # 	return factory.hotspot.create { 
	# 	pos = p, 
	# 	width = 2, 
	# 	height = 256, 
	# 	func = function(mario, hotspot)
	# 		local mario = monkey.getEntity("player")
	# 		hotspot:remove()
	# 		mario.state = "slide"
	# 		local delta = math.abs(mario.y - 48, 0)
	# 		local actions = {
	# 			{ type = action.noop, ref = 1},
	# 			{ type = action.move, ref = 2, after={1}, args = {tag="player", by = {0, -delta}, speed = 50}},
	# 			{ type = action.move, after={1}, args = {tag="flag", by = {0, -128}, speed = 50}},
	# 			{ type = action.set_state, after= {2}, args = {tag = "player", state = "walk"}},
	# 			{ type = action.set_demo_mode, args = { tag="player", value=true, sync = true, length = 10, events = {
	# 				{ t=0, key = 262, event ="down"}
	# 			}}},
	# 		}
	# 		local s = script.make(actions)
	# 		monkey.play(s)		
	# 	end
    # print ('fuckme')
    
# factory.bonus_brick.response = function(p1, p2)

# 	local brick = p2:parent()
# 	local brick_info = brick:getinfo()
# 	if brick_info.hitsleft > 0 then
# 		brick_info.hitsleft = brick_info.hitsleft - 1
# 		local actions = {
# 			{ 
# 				type = action.moveaccel, 
# 				args = { 
# 					id = brick.id, 
# 					initial_velocity = {0, 50}, 
# 					acceleration = {0, 0.5*variables.gravity}, 
# 					ystop = brick_info.y
# 				}
# 			}
# 		}
# 		if (brick_info.hitsleft == 0) then
# 			table.insert (actions, {
# 				type = action.animate,
# 				args = { id = brick.id, anim = "taken" }
# 			})
# 		end
		

# 		table.insert (actions, {
# 			type = action.callfunc,
# 			args = {
# 				func = function()
# 					local pos = {brick.x+0.5*engine.tilesize, brick.y, 1}
# 					local factory = glib.get(brick_info.factory)
# 					local args = glib.get(brick_info.args)

# 					local o = factory.create(args, pos)
# 					print("Mio cuggggg")
# 					local m1 = monkey.getEntity("main")
# 					local id = monkey.addEntity (o, m1)

# 					-- hey, do I have to perform a script on this?
# 					if (factory.script ~= nil) then
# 						print ("FATTTTONE")
# 						local actions = factory.script(id, pos)
# 						local s = script.make(actions)
# 						monkey.play(s)
# 					end


# 				end
				
# 			}
# 		})

# 		-- release the bonus
# 		local s = script.make(actions)
# 		monkey.play(s)
# 	end	
# end
