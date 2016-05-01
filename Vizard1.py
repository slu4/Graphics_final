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
#sky = viz.addCustomNode('skydome.dlc')

# load the daytime environment by default
#env = viz.addEnvironmentMap(envs[0])
#sky.texture(env)

#idx = 1
def changeEnv(name):
	"""
	Function called to manage timers.
	"""
	#idx=1
	#env = viz.addEnvironmentMap(envs[idx])
	env = viz.addEnvironmentMap(name)
	sky = viz.addCustomNode('skydome.dlc')
	sky.texture(env)
	#idx = (idx + 1) % 2
	
vizact.ontimer2(1, viz.PERPETUAL, changeEnv, vizact.choice(envs,vizact.LOOP))
# Add ground
#ground = vizfx.addChild('ground_gray.osgb')

#Register the timer callback. 
#viz.callback(viz.TIMER_EVENT,onTimer) 
# start the timer
#viz.starttimer( REPEATER, 1, viz.PERPETUAL ) 

#Now apply the environment map texture to the dome
#sky.texture(env)

class moving_logo:
	"""
	Class for a rotating vizfxard logo at a given position within a given
	environment.
	"""
	def __init__(self, x, y, z, vizfx, env):
		# Add in a logo. Use the built in logo.ive
		self.logo = vizfx.addChild('logo.ive')
		# set position
		self.logo.setPosition([x, y, z])
		# Apply the surrounding texture
		self.logo.texture(env)
		# We need to set the appearance of the logo to vizfx.ENVIRONMENT_MAP
		self.logo.appearance(viz.ENVIRONMENT_MAP)
		# Make the logo spin along Y
		self.logo.addAction( vizact.spin(0,1,0,60) )
		

# Make a cricle of rotating logos
stop = 360         # Number of degrees in circle
skip = 60          # How often to make a logo in degrees (ex. 45 or 90)
scale_fac = 2      # Basically radius of the circle
height_offset = 2  # How high off the "ground" for the center of the circle
# Calculate the number of 
degrees = range(0, stop, skip)

# not really needed but may be useful later
logos = []
shiny = True
for deg in degrees:
	#print deg
	# Convert degrees to radians and calculate X and Y positions
	xr = math.radians(deg)
	yr = math.radians(deg)
	# Calc X & Y and scale the positions
	xp = math.cos(xr) * scale_fac
	yp = math.sin(yr) * scale_fac
	
	#print "xr, yr: ", xr, yr
	#print "xp, yp: ", xp, yp
	#print "xp, yp: ", xp, yp
	# Make a moving_logo and append it to the list
	# Make every other one reflect the environment (it will be shiny)
	if shiny:
		logos.append(moving_logo(xp, yp + height_offset, 8, vizfx, env))
		shiny = False
	else:
		logos.append(moving_logo(xp, yp + height_offset, 8, vizfx, None))
		shiny = True
		
# Start of Mbah's code

viz.clearcolor(viz.SKYBLUE)
#ground=vizfx.addChild('ground_grass.osgb')
#ground.setScale([2,2,2])
viz.MainView.setPosition([0,1.8,-10])

ball=vizfx.addChild('ball.wrl')
ball.setPosition(0,0.4,-4)
ball.setScale(1.5,1.5,1.5)

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

viz.startLayer(viz.QUADS)
viz.vertexColor(1, 1, 0)
viz.vertex(-1, 1, 0)
viz.vertex(-1, 1, 1)
viz.vertex(-0, 1, 1)
viz.vertex(-0, 1, 0)

sun = viz.endLayer()

# Makes the sun move using a defined path.
sunPath = viz.addAnimationPath()
sunPath.addControlPoint(2, pos=[-1, 2, 0])
#sunPath.addControlPoint(4, pos=[-2, 2, 0])
#sunPath.addControlPoint(6, pos=[-3, 2, 0])
sunPath.addControlPoint(8, pos=[-4, 2, 0])
ball.setPosition(-2, .5, 0)

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

