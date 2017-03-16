from SenseEngine import *
from random import randint

class BallController(Script):
	def __init__(self):
		Script.__init__(self)
	def Start(self):
		print("Started")
		v = randint(-1, 1)
		if v == 0:
			v = 1
		self.masterObject.GetComponent(PhysicsObject).velocity.x = v
		v = randint(-1, 1)
		if v == 0:
			v = 1
		self.masterObject.GetComponent(PhysicsObject).velocity.y = v
	def OnCollision(self, collider):
		if collider.masterObject.tag == "PaddleMid":
			self.Bounce(-1, -1)
		elif collider.masterObject.tag == "PaddleR":
			self.Bounce(1, -1)
		elif collider.masterObject.tag == "PaddleL":
			self.Bounce(1, -1)
		elif collider.masterObject.tag == "Wall_Top":
			self.Bounce(1, -1)
		elif collider.masterObject.tag == "Wall_Side":
			self.Bounce(-1, 1)
		elif collider.masterObject.tag == "DedWall":
			self.Reset()
		elif collider.masterObject.tag == "Point":
			self.Bounce(-1,-1)
			game.DeleteObject(collider.masterObject)
			print("deld")
	def Bounce(self, xfactor, yfactor):
		phy = self.masterObject.GetComponent(PhysicsObject)
		x = phy.velocity.x * xfactor
		y = phy.velocity.y * yfactor
		self.masterObject.GetComponent(PhysicsObject).velocity = Vector(x, y)
	def Reset(self):
		v = randint(-1, 1)
		if v == 0:
			v = 1
		self.masterObject.GetComponent(PhysicsObject).velocity.x = v
		v = randint(-1, 1)
		if v == 0:
			v = 1
		self.masterObject.GetComponent(PhysicsObject).velocity.y = v
		self.masterObject.GetComponent(Transform).position = Vector(1, 4)
