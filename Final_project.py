import viz
import vizfx
import vizcam
import vizshape
import vizact
import math
import projector
import viztask
import random

viz.go()

# Disable the default headlight and set starting position
viz.MainView.getHeadLight().disable()
viz.MainView.setPosition(-18, 2,-14)  # will be linked with an avatar later
viz.MainView.setEuler( [70, 0, 0] )

#Add a model of my forest created in the inspector
forest = viz.add('forest_2.osgb' )


### Load environments  ###
# The envorinments that we want to load
envs = ('sky.jpg', 'newcube.jpg')

#  vizard has a built-in plugin called 'skydome.dlc'. This creates a dome around the user.
sky = viz.addCustomNode('skydome.dlc')

# load the environment use daytime by default
env1 = viz.addEnvironmentMap(envs[0])
env2 = viz.addEnvironmentMap(envs[1])

env = env1        # set to environment 1 by default
sky.texture(env)  # update the skydome to match

# Functions to change environments
def textu1():
	""" Change to environment 1 """
	choice = env1
	env = choice
	sky.texture(choice)

	
def textu2():
	""" Change to environment 2 """
	choice = env2
	env = choice
	sky.texture(choice)

# keep these in here...
vizact.onkeydown( 'c', textu1 )
vizact.onkeydown( 'd', textu2 ) 


def PathTask():
	"""
	A way to control what happens during animation.
	
	change_scene will handle changing the scene from day to night
	"""
	def change_scene(name):
		""" Change the Scene envorinment based on what is already active
		
		This basically calls textu1 and textu2 and changes the visiability of
		the sun, moon and their light sources.
		"""
		if name == 'envChange':
			print 'Changing environment'
			print sky.getTexture()
			if sky.getTexture() == viz.VizTexture(0):
				print 'Day time. Changing to night'
				print sky.getTexture()
				textu2()
				print sky.getTexture()
				sun.visible(False)
				sunlight.visible(False)
				moon.visible(True)
				moonlight.visible(True)
			else:
				print 'Night time. Changing to day'
				textu1()
				sun.visible(True)
				sunlight.visible(True)
				moon.visible(False)
				moonlight.visible(False)
		else:
			print "Found '{0}' as name. Not recognized".format(name)
	
	# This is the important part...
	while True:
		# Create a generator that will produce the invoked name of the
		# action listener and wait until it does. Then pass the name off
		# Wait for any event on the path
		d = yield viztask.waitPathEvent(sunPath, None)

		# Change the scene at the triggered time
		change_scene(d.name)


# Try a moon
moontex = viz.addTexture('moon_8k_color_brim16.jpg')

# Try a sun
suntex = viz.addTexture("gstar.jpg")

#Define the light as a point, positional light.
#This is done with the last '1' in this command's arguments.
sunlight = viz.addLight()
sunlight.position( 0,0,0,1 )
sunlight.intensity(50)
sunlight.texture(suntex)

# Get the sun from the forest scene that I created and use it as the sun
sun = forest.getChild("Sun")
sun.emissive(viz.YELLOW)
sun.texture(suntex)
sun.setPosition([20,0,0])

# Now the moon
moonlight = viz.addLight()
moonlight.position( 0,0,0,1 )
moonlight.intensity(1)
moonlight.color( [.6,.7,.9] )
moonlight.texture(moontex)

# Get the moon from the forest scene that I created and use it as the moon
moon = forest.getChild("Moon")
moon.texture(moontex)
#moonlight.setEuler([0,-180,0])
moon.emissive(viz.YELLOW)

# initially moon is not visiable
moon.visible(False)
moonlight.visible(False)


# link up the lights to objects
viz.link(sun, sunlight)
viz.link(moon, moonlight)


# Make a lantern on a tree have some light because its dark at night
lantern = forest.getChild('lantern')
lantern_position = [-8.2, 1.10, -3]
lantern.setPosition( lantern_position )

#Add a light source to put inside the lantern.
lantern_light = viz.addLight()

#Define the light as a point, positional light.
#This is done with the last '1' in this command's arguments.
lantern_light.position( 0,0,0,1 )

#Link the light to the lantern.
viz.link( lantern, lantern_light )

#Grab the flame part of the lantern model and give an emissive quality to emulate light.
flame = lantern.getChild( 'flame' )
flame.emissive( viz.YELLOW )

#Play with the light source's parameters.
lantern_light.color( viz.YELLOW )
lantern_light.quadraticattenuation( 1 )
lantern_light.intensity( 8 )

#Give the lantern some shine.
lantern.specular(viz.YELLOW)
lantern.shininess(10)

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

# Get the points for the sun and moon to follow
sunPoints = makeCircle(0, 390, 30, 20, 0, 0)
moonPoints = makeCircle(-180, 210, 30, 20, 0, 0)  # moon is 180 past sun
# set initial positions
sun.setPosition(sunPoints[0])
moon.setPosition(moonPoints[0])

# create animation paths
sunPath = viz.addAnimationPath()
moonPath = viz.addAnimationPath()

# add the points into the control paths
time = 2
for i, points in enumerate(sunPoints):
	sunPath.addControlPoint(i * time, pos=points)
	moonPath.addControlPoint(i * time, pos=moonPoints[i])

# set up the paths
sunanimation = viz.link(sunPath, sun)
moonanimation = viz.link(moonPath, moon)
sunPath.setLoopMode(viz.LOOP)
moonPath.setLoopMode(viz.LOOP)

# Calculate the times that the sun will set and rise
halfway = ((len(sunPoints) - 1) /2) * time
full = (len(sunPoints) - 1) * time

sunPath.addEventAtTime("envChange", halfway)
sunPath.addEventAtTime("envChange", full)

sunPath.play()
moonPath.play()

viztask.schedule(PathTask())


vizact.onkeydown('b', viz.window.startRecording, 'initialRecording.avi' ) 
vizact.onkeydown('e', viz.window.stopRecording )

#Hit the 's' key for a screen capture. 
#Save that files as 'image.bmp'. 
vizact.onkeydown( 's', viz.window.screenCapture, 'Vizard_screenShot.bmp' )


# Grab the main view.
view = viz.MainView
#Turn on viewpoint collision and set its distance buffer.
viz.collision(viz.ON)
viz.collisionbuffer( 4.5 )
viz.MainView.collision( viz.ON )

# Add avatar
a = vizfx.addAvatar( 'vcc_male.cfg')
a.state(1)
aHead = a.getBone('Bip01 Head')

#a.setPosition(view.getPosition()[0], view.getPosition()[1],view.getPosition()[2]+2)
#a.setEuler(view.getEuler(viz.BODY_ORI))
#a.setPosition([0.35,-1.2,0.2],viz.REL_LOCAL)

#Link the avatar to the view.
avLink = viz.link( view, a )
#
avLink.preTrans( [0, -2, 4])

def onMouseDown():
	"""Make the avatar appear to walk"""
	a.state(2)
	#a.setPosition(view.getPosition)
	
def onMouseUp(button):
	"""Stop the avatar from walking"""
	if button == viz.MOUSEBUTTON_LEFT:
		a.state(1)
		

vizact.whilemousedown(viz.MOUSEBUTTON_LEFT, a.state, 2) 
vizact.onmouseup(viz.MOUSEBUTTON_LEFT, onMouseUp, viz.MOUSEBUTTON_LEFT)


# Enable physics
viz.phys.enable()
ground = forest.getChild('Plane01')
ground.collidePlane()
a.collideBox()

#
#
# Start Ben's Code. This is a pseudo random woods.
for x in [7,-5, -3, 1,3, 5,7, 9]:
	#for z in [-9, -6, -2, 2, 6, 10]:
	z = (23*x +13)%10 + 10
	myTrunk = vizshape.addCylinder(height = 2.0, radius = 0.5)
	myTrunk.setPosition([x,1.0,z])
	myTrunk.color([0.545,0.271,0.075])
	myLeaves = vizshape.addCone(height = 3.0, radius = 1.5)
	myLeaves.color([0,1,0])
	myLeaves.setPosition([x,3.5,z])
	
#Dirt
viz.startLayer(viz.POLYGON)
viz.vertexColor(0.263, 0.078, 0.078)
viz.vertex(-5, 0.1, -5)
viz.vertex(-3, 0.1, 0)
viz.vertex(2, 0.1, 0)
viz.vertex(4, 0.1, 2)
viz.vertex(0, 0.1, -5)
myPath = viz.endLayer()
myPath.setPosition(5, 0.1, 0)
myPath.setScale([2,2,2])

#River
viz.startLayer(viz.TRIANGLE_FAN)
viz.vertexColor(viz.BLUE)
viz.vertex(-5, 0.1, -20)
viz.vertex(-5, 0.1, -5)
viz.vertex(-3, 0.1, 0)
viz.vertex(2, 0.1, 0)
viz.vertex(1, 0.1, 10)
viz.vertexColor(0, 0, 0.8, 1)
viz.vertex(-1, 0.1, 20)
viz.vertex(3, 0.1, 7)
viz.vertex(3, 0.1, 0)
myStream = viz.endLayer()
myStream.setPosition(-15, 0.1, 0)

# Dave's code again
from vizfx.postprocess.effect import BaseShaderEffect

class UnderwaterEffect(BaseShaderEffect):

    def __init__(self, speed=0.0, scale=0.0, density=20.0, **kw):
        self._speed = speed
        self._scale = scale
        self._density = density
        BaseShaderEffect.__init__(self,**kw)

    def _getFragmentCode(self):
        return """
        uniform sampler2D vizpp_InputTex;
        uniform float osg_FrameTime;
        uniform float speed;
        uniform float scale;
        uniform float density;
        void main()
        {
            vec2 uv = gl_TexCoord[0].xy;

            //bumpUV.y = fract(bumpUV.y - osg_FrameTime*0.1);
            vec2 dt;
            dt.x = sin(speed*osg_FrameTime+uv.y*density)*0.001*scale;
            dt.y = cos(0.7+0.7*speed*osg_FrameTime+uv.x*density)*0.001*scale;

            gl_FragColor = texture2D(vizpp_InputTex,uv+dt);
        }
        """

    def _createUniforms(self):
        self.uniforms.addFloat('speed',self._speed)
        self.uniforms.addFloat('scale',self._scale)
        self.uniforms.addFloat('density',self._density)

    def setSpeed(self,speed):
        self._speed = speed
        self.uniforms.setValue('speed',speed)

    def getSpeed(self):
        return self._speed

    def setScale(self,scale):
        self._scale = scale
        self.uniforms.setValue('scale',scale)

    def getScale(self):
        return self._scale

    def setDensity(self,density):
        self._density = density
        self.uniforms.setValue('density',density)

    def getDensity(self):
        return self._density

effect = UnderwaterEffect()
vizfx.postprocess.addEffect(effect)

myStream.collideMesh()

# Create a box to track colisions
bodyBox = viz.add('box.wrl')#,scale=[0.1,0.1,0.1])
bodyBox.collideBox()
bodyBox.disable(viz.DYNAMICS)
bodyBox.enable(viz.COLLIDE_NOTIFY)
rHandLink = viz.link( a.getBone('Bip01') , bodyBox )
#tweak the position of the box to cover the hand
rHandLink.preTrans([0.05,-1.0,0])

# Make the box invisable
bodyBox.disable(viz.RENDERING)


def onCollideBegin(e):
    if e.obj1 == bodyBox:
        if e.obj2 == myStream:
			print "begin"
			effect.setScale(10.0)
			effect.setSpeed(5.0)

def onCollideEnd(e):
    if e.obj1 == bodyBox:
        if e.obj2 == myStream:
			print "End"
			effect.setScale(0.0)
			effect.setSpeed(0.0)

viz.callback(viz.COLLIDE_BEGIN_EVENT,onCollideBegin)
viz.callback(viz.COLLIDE_END_EVENT,onCollideEnd)


#winnie codes, put some ducks in the river added some 
duck = viz.add('duck.cfg')
duck.setPosition([-16,-0.1,7])
duck.setEuler([180,0,0])

duck = viz.add('duck.cfg')
duck.setPosition([-8,0.1,9])
duck.setEuler([180,0,0])

duck = viz.add('duck.cfg')
duck.setPosition([-14,-0.1,12])
duck.setEuler([180,0,0])

pigeons = []
for i in range(10):

    #Generate random values for position and orientation
    x = random.randint(-4,3)
    z = random.randint(4,8)
    yaw = random.randint(0,360)

    #Load a pigeon
    pigeon = viz.addAvatar('pigeon.cfg')

    #Set position, orientation, and state
    pigeon.setPosition([x,0,z])
    pigeon.setEuler([yaw,0,0])
    pigeon.state(1)

    #Append the pigeon to a list of pigeons
    pigeons.append(pigeon)

pigeonClone = pigeon.clone(scale=[5]*3)
pigeonClone.addAction(vizact.spin(0,1,0,45))
pigeonClone.enable(viz.DEPTH_TEST,op=viz.OP_ROOT)


