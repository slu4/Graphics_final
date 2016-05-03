import viz
import vizfx
import vizact
import vizshape
import vizinfo

import math
import random

# This will launch vizfxard and set the background clear color to a nice sky blue
viz.setMultiSample(4)
viz.fov(90)
viz.go()

#Next, let's add the environment map. An environment map is made up of 6
#textures. Each texture represents one side of a cube. This cube represents
#the surrounding environment of an object. This example will load the following 6 textures:
# 
#sky_posx.png 
#sky_negx.png 
#sky_posy.png 
#sky_negy.png 
#sky_posz.png 
#sky_negz.png
#
#vizfxard has a shortcut for loading environment maps. So go ahead and add the following line of code to your script:
# The envorinments that we want to load
envs = ('sky.jpg', 'R136.jpg')

#  vizard has a built-in plugin called 'skydome.dlc'. This creates a dome around the user.
sky = viz.addCustomNode('skydome.dlc')

# load the environment use daytime by default
env1 = viz.addEnvironmentMap(envs[0])
env2 = viz.addEnvironmentMap(envs[1])
sky = viz.addCustomNode('skydome.dlc')
env = env1        # set to environment 1 by default
sky.texture(env)  # update the skydome


def textu1():
	""" Change to environment 1 """
	print ''
	choice = env1
	env = choice
	sky.texture(choice)
	updatelogo(choice)
	
	
def textu2():
	""" Change to environment 2 """
	print ''
	choice = env2
	env = choice
	sky.texture(choice)

def updatelogo(choice):
	""" Update the environment of the `moving_logo`s in logo """
	for i, logo in enumerate(logos):
		print i, choice
		logo.update_env(choice)
	
vizact.onkeydown( 'c', textu1 )
vizact.onkeydown( 'd', textu2 ) 
# Add ground
#ground = vizfx.addChild('ground_gray.osgb')

#Now apply the environment map texture to the dome
sky.texture(env)

class moving_logo:
	"""
	Class for a rotating vizfxard logo at a given position within a given
	environment.
	"""
	logo = None
	#logo = viz.addChild('logo.ive')
	#logo.appearance(
	def __init__(self, x, y, z, vizfx, env):
		# Add in a logo. Use the built in logo.ive
		self.logo = viz.addChild('logo.ive')
		# set position
		self.logo.setPosition([x, y, z])
		# Apply the surrounding texture
		self.logo.texture(env)
		# We need to set the appearance of the logo to vizfx.ENVIRONMENT_MAP
		self.logo.appearance(viz.ENVIRONMENT_MAP)
		# Make the logo spin along Y
		self.logo.addAction( vizact.spin(0,1,0,60) )
	
	def update_env(self, choice):
		print env, choice
		self.logo.texture(choice)
		#self.logo.appearance(choice)
		
def makeCircle(start, stop, skip, radius, offset, z=0):
	"""
	Makes list of x, y, z points in a circle around the z axis.
	
	Inputs:
		start - int
			Starting point of the circle in degrees
		stop - int
			Ending point of the circle in degrees
		skip - int
			How often to make a point
		radius - int
			radius of the circle
		offset - int
			position in y that the center of the circle is offset by
		z - int
			Z location of points - default is 0.
	"""
	degrees = range(start, stop, skip)
	locs = []
	for deg in degrees:
		#print deg
		# Convert degrees to radians and calculate X and Y positions
		xr = math.radians(deg)
		yr = math.radians(deg)
		# Calc X & Y and scale the positions
		xp = math.cos(xr) * radius
		yp = math.sin(yr) * radius
		
		locs.append((xp, yp + offset, z))
	return locs

logos = []

logopos = makeCircle(0, 360, 60, 2, 2, 8)

for pos in logopos:
	logos.append(moving_logo(pos[0], pos[1], pos[2], viz, env))


#ground=vizfx.addChild('ground_grass.osgb')
#ground.setScale([2,2,2])
viz.MainView.setPosition([0,1.8,-10])

# Add things
ball=vizfx.addChild('ball.wrl')
ball.setPosition(0,0.4,-4)
ball.setScale(1.5,1.5,1.5)
ball.setPosition(-2, .5, 0)

tree = vizfx.addChild('plant.osgb')
tree.setPosition(-8.5,0,0)
tree.setScale(2,4,2)
tree1 = vizfx.addChild('plant.osgb')
tree1.setPosition(8.5,0,0)
tree1.setScale(2,4,2)
tree2 = vizfx.addChild('plant.osgb')
tree2.setPosition(-8.5,0,-8.5)
tree2.setScale(2,4,2)
tree3 = vizfx.addChild('plant.osgb')
tree3.setPosition(8.5,0,-8.5)
tree3.setScale(2,4,2)

sphere = vizshape.addSphere(pos=[-4, 2, 0], lighting=True, color=viz.YELLOW)

# Make something of our own, Just a square
viz.startLayer(viz.QUADS)
viz.vertexColor(1, 1, 0)
viz.vertex(-1, 1, 0)
viz.vertex(-1, 1, 1)
viz.vertex(-0, 1, 1)
viz.vertex(-0, 1, 0)
plane = viz.endLayer()

# Makes the sun move using a defined path.
sunPoints = makeCircle(0, 180, 30, 10, 0, 5)

sunPath = viz.addAnimationPath()
for i, points in enumerate(sunPoints):
	sunPath.addControlPoint(i*2, pos=points)
#sunPath.addControlPoint(2, pos=[-1, 2, 0])
#sunPath.addControlPoint(4, pos=[-2, 2, 0])
#sunPath.addControlPoint(6, pos=[-3, 2, 0])
#sunPath.addControlPoint(8, pos=[-4, 2, 0])


light = vizfx.addSpotLight(euler=(0, 90, 0), color=viz.RED)
light.position(-1, 1, 0)
light.spread(65)
light.intensity(5000)

link = viz.link(sunPath, sphere)
sunlightlink = viz.link(sunPath, light)
sunPath.play()

#plane = vizshape.addPlane(size=(200,200), cullFace=False, lighting=True)
#plane.color(viz.WHITE)
#quad = vizshape.addQuad(size=(200, 200), axis=-vizshape.AXIS_Y, cullFace=False)
cube = vizshape.addBox(size=(200., .5, 200.), lighting=True, color=viz.WHITE)

sphere = vizshape.addSphere(pos=[-4, 2, 0], lighting=True, color=viz.YELLOW)
sphere.appearance(viz.ENVIRONMENT_MAP)


# Try putting an arrow at things when clicked
arrow = vizshape.addArrow(length=2, color = viz.ORANGE)
arrow.visible(viz.OFF)

def pickObj():
    object = viz.pick()
    if object.valid() and object != arrow:
        pos = object.getPosition()
        pos[1] += .2
        print pos
        arrow.setPosition(pos)
        arrow.visible(viz.ON)

vizact.onmousedown(viz.MOUSEBUTTON_LEFT, pickObj)



############################################################################
#####################   Begin Mbah's Code  #################################
############################################################################

num=10
s=3
c=3
species='pigeon.cfg'
while num>0:
	x = random.randint(-4,4)
	z = random.randint(-8,-2)
	yaw = random.randint(0,360)
	animal = viz.addAvatar(species)
	animal.setScale(c,c,c)
	animal.setPosition(x,0,z)
	animal.setEuler(yaw,0,0)
	animal.collideMesh()
	animal.state(s)
	num=num-1
	if num==5:
		s=1
		species='duck.cfg'
		c=.5

c=9
s=1

x=-8.5
z=-8.5

trees=[]
for x in [-9,-7, -3, 5, 8,10]:
    for z in [-8,-6,-4, 0, 4,6]:
		tree = viz.addChild('plant.osgb',cache=viz.CACHE_CLONE)#make a bunch of trees 
		tree.setPosition(x,0,z)
		tree.setScale(2,4,2)
		z=z+3