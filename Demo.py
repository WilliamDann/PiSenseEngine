from SenseEngine import *
from PaddleController import *

class Demo(Game):
	def __init__(self):
		Game.__init__(self)
		self.GRAVITY = 0
		self.FPS = 1
		
		self.paddle = Sprite.Load("[CWD]/paddle")
		self.ball = Sprite.Load("[CWD]/ball")
		
		self.wallTop = Sprite.Load("[CWD]/wallTop")
		self.wallSide = Sprite.Load("[CWD]/wallSide")
		
		pc = Script.loadScriptForScriptClass("[CWD]/PaddleController.py")
		g = GameObject("PaddleR", self.paddle, [pc, Collider(self.paddle.points)])
		g.GetComponent(Transform).position = Vector(2, 7)
		g.tag = "PaddleR"
		self.AddObject(g)
		pc = Script.loadScriptForScriptClass("[CWD]/PaddleController.py")
		g = GameObject("PaddleMid", self.paddle, [pc, Collider(self.paddle.points)])
		g.GetComponent(Transform).position = Vector(3, 7)
		g.tag = "PaddleMid"
		self.AddObject(g)
		pc = Script.loadScriptForScriptClass("[CWD]/PaddleController.py")
		g = GameObject("PaddleMid", self.paddle, [pc, Collider(self.paddle.points)])
		g.GetComponent(Transform).position = Vector(2, 7)
		g.tag = "PaddleMid"
		self.AddObject(g)
		pc = Script.loadScriptForScriptClass("[CWD]/PaddleController.py")
		g = GameObject("PaddleMid", self.paddle, [pc, Collider(self.paddle.points)])
		g.GetComponent(Transform).position = Vector(4, 7)
		g.tag = "PaddleMid"
		self.AddObject(g)
		pc = Script.loadScriptForScriptClass("[CWD]/PaddleController.py")
		g = GameObject("PaddleR", self.paddle, [pc, Collider(self.paddle.points)])
		g.GetComponent(Transform).position = Vector(5, 7)
		g.tag = "PaddleL"
		self.AddObject(g)
		
		bc = Script.loadScriptForScriptClass("[CWD]/BallController.py")
		b = GameObject("Ball", self.ball, [PhysicsObject(decay=0), bc, Collider(self.ball.points)])
		b.GetComponent(Transform).position = Vector(1, 4)
		b.tag = "Ball"
		self.AddObject(b)
		
		walltop = GameObject("TopWall", self.wallTop, [Collider(self.wallTop.points)])
		walltop.GetComponent(Transform).position = Vector(0, -1)
		walltop.tag = "Wall_Top"
		self.AddObject(walltop)
		
		walltop = GameObject("DedWall", self.wallTop, [Collider(self.wallTop.points)])
		walltop.GetComponent(Transform).position = Vector(0, 8)
		walltop.tag = "DedWall"
		self.AddObject(walltop)
		
		walls1 = GameObject("Side1Wall", self.wallSide, [Collider(self.wallSide.points)])
		walls1.GetComponent(Transform).position = Vector(-1, 0)
		walls1.tag = "Wall_Side"
		self.AddObject(walls1)
		
		walls2 = GameObject("SideWall2", self.wallSide, [Collider(self.wallSide.points)])
		walls2.GetComponent(Transform).position = Vector(8, 0)
		walls2.tag = "Wall_Side"
		self.AddObject(walls2)
		
		for x in range(8):
			for y in range(3):
				sp = Sprite([Point(Vector(0,0), Color(255,0,255))])
				point = GameObject("Point", sp, [Collider(sp.points)])
				point.tag = "Point"
				
				point.GetComponent(Transform).position = Vector(x, y)
				self.AddObject(point)
		
		self.run()

if __name__ == "__main__":
	Demo()
