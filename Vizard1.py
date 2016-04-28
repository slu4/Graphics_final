import viz
import vizact
import math

# This will launch Vizard and set the background clear color to a nice sky blue
viz.setMultiSample(4)
viz.fov(60)
viz.go()

#viz.clearcolor(viz.SKYBLUE)

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
#Vizard has a shortcut for loading environment maps. So go ahead and add the following line of code to your script:
#env = viz.addEnvironmentMap('sky.jpg')
env = viz.addEnvironmentMap( 'R136.jpg')

#env = viz.addTexture('lake3.jpg')

# Add ground
#viz.addChild('ground_gray.osgb')

#  Vizard has a built-in plugin called 'skydome.dlc'. This creates a dome around the user.
sky = viz.addCustomNode('skydome.dlc')

#Now apply the environment map texture to the dome
sky.texture(env)


class moving_logo:
	"""
	Class for a rotating Vizard logo at a given position within a given
	environment.
	"""
	def __init__(self, x, y, z, viz, env):
		# Add in a logo. Use the built in logo.ive
		self.logo = viz.addChild('logo.ive')
		# set position
		self.logo.setPosition([x, y, z])
		# Apply the surrounding texture
		self.logo.texture(env)
		# We need to set the appearance of the logo to viz.ENVIRONMENT_MAP
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
	print deg
	# Convert degrees to radians and calculate X and Y positions
	xr = math.radians(deg)
	yr = math.radians(deg)
	# Calc X & Y and scale the positions
	xp = math.cos(xr) * scale_fac
	yp = math.sin(yr) * scale_fac
	
	print "xr, yr: ", xr, yr
	print "xp, yp: ", xp, yp
	# Make a moving_logo and append it to the list
	# Make every other one reflect the environment (it will be shiny)
	if shiny:
		logos.append(moving_logo(xp, yp + height_offset, 8, viz, env))
		shiny = False
	else:
		logos.append(moving_logo(xp, yp + height_offset, 8, viz, None))
		shiny = True
		
# Start of Mbah's code

viz.clearcolor(viz.SKYBLUE)
ground=viz.addChild('ground_grass.osgb')
ground.setScale([2,2,2])
viz.MainView.setPosition([0,1.8,-10])

ball=viz.addChild('ball.wrl')
ball.setPosition(0,0.4,-4)
ball.setScale(1.5,1.5,1.5)
ball.addAction
tree = viz.addChild('plant.osgb')
tree.setPosition(-8.5,0,0)
tree.setScale(2,4,2)
tree1 = viz.addChild('plant.osgb')
tree1.setPosition(8.5,0,0)
tree1.setScale(2,4,2)
tree2 = viz.addChild('plant.osgb')
tree2.setPosition(-8.5,0,-8.5)
tree2.setScale(2,4,2)
tree3 = viz.addChild('plant.osgb')
tree3.setPosition(8.5,0,-8.5)
tree3.setScale(2,4,2)

ball.addAction()