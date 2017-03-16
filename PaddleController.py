from SenseEngine import *

class PaddleController(Script):
	def __init__(self):
		Script.__init__(self)
		game.AddInputCallback(K_RIGHT, self.MoveRight)
		game.AddInputCallback(K_LEFT, self.MoveLeft)
		
	def MoveRight(self):
		self.masterObject.GetComponent(Transform).position.x += 1
	def MoveLeft(self):
		self.masterObject.GetComponent(Transform).position.x -= 1
