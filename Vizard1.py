import viz
import vizact

viz.setMultiSample(4)
viz.fov(90)
viz.go()

viz.clearcolor(viz.SKYBLUE)
ground=viz.addChild('ground_grass.osgb')
ground.setScale([2,2,2])
viz.MainView.setPosition([0,1.8,-10])

ball=viz.addChild('ball.wrl')
ball.setPosition(0,0.4,-4)
ball.setScale(1.5,1.5,1.5)
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