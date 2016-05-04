import viz
import vizact
import vizshape
import random

viz.setMultiSample(4)
viz.collision(viz.ON)
viz.fov(90)
viz.go()
viz.phys.enable()

# Start Ben's Code. This is a pseudo random woods.
for x in [-7,-5, -3, 1,3, 5,7, 9]:
	#for z in [-9, -6, -2, 2, 6, 10]:
	z = (23*x +13)%10
	myTrunk = vizshape.addCylinder(height = 2.0, radius = 0.5)
	myTrunk.setPosition([x,1.0,z])
	myTrunk.color([0.545,0.271,0.075])
	myLeaves = vizshape.addCone(height = 3.0, radius = 1.5)
	myLeaves.color([0,1,0])
	myLeaves.setPosition([x,3.5,z])
# End Ben's Code



#viz.fogcolor(0.5,0.5,0.5)
#viz.fog(1,10)
viz.clearcolor(viz.SKYBLUE)


ground=viz.addChild('ground_grass.osgb')

ground.collidePlane()
ground.setScale([2,2,2])
viz.MainView.move([0,0,-12]) #change view
#viz.MainView.setPosition([0,15,-15]) #change view
#viz.MainView.setEuler([0,30,0]) #rotation (y,x,z)

#Change environment function
env1=viz.addEnvironmentMap('sky.jpg')
env2=viz.addTexture('brick.jpg')
sky = viz.addCustomNode('skydome.dlc')
sky.texture(env2)

def textu():
	choice=env1
	sky.texture(choice)
	
def textu2():
	choice=env2
	sky.texture(choice)
	
vizact.onkeydown( 'c', textu )
vizact.onkeydown( 'd', textu2 ) 
#Change environment function


#env = viz.addEnvironmentMap(name)

#envs = ('sky.jpg', 'R136.jpg')
#def changeEnv(name):
#	#idx=1
#	#env = viz.addEnvironmentMap(envs[idx])
#	env = viz.addEnvironmentMap(name)
#	sky = viz.addCustomNode('skydome.dlc')
#	sky.texture(env)
#	#idx = (idx + 1) % 2
#	
#vizact.ontimer2(1, viz.PERPETUAL, changeEnv, vizact.choice(envs,vizact.LOOP))


#pigeons = []
#for i in range(10):

    #Generate random values for position and orientation
    #x = random.randint(-4,3)
    #z = random.randint(4,8)
    #yaw = random.randint(0,360)

	
	
#plants = []
#for x in [-3, -1, 1, 3]:		#sample for loop
    #for z in [4, 2, 0, -2, -4]:
       # plant = viz.addChild('plant.osgb',cache=viz.CACHE_CLONE)
       # plant.setPosition([x,0,z])
       # plants.append(plant)

#spin = vizact.spin(0,1,0,15) #says spin about y axis at a 15 degree angle


#sample function, The function spinPlant will get called every 0.5 seconds for a total of 20 times (1 + 19 repeats). 
#Each time, the spin action is applied to the next plant in the list.
#def spinPlant(plant):		
#    plant.addAction(spin)
#vizact.ontimer2(0.5,19,spinPlant,vizact.choice(plants))
#for indefinite repeats, use ontimer function, has no repeat parameter
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
		
#def animalMoves():



