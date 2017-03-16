from sense_hat import SenseHat # Used in: Game.render()
import os # Used in: Script.loadExternalScript(), loadScriptForScriptClass()
import imp # Used in: Script.loadExternalScript()
import datetime # Used in: Game.run()
import time as t # Used in: Game.run()
import sys # Used in Script.loadScript()
import inspect # Used in Script.loadScript()
from pygame import * # Used in: various input

# Initlize sensehat and clear
sense = SenseHat()
sense.clear()
game = None
AUTO = -1

class Vector():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

class Component():
	def __init__(self, masterObject=None):
		self.enabled = True
		self.masterObject = masterObject
class SpriteRenderer(Component):
	def __init__(self, sprite):
		Component.__init__(self)
		self.sprite = sprite
class Transform(Component):
	def __init__(self, position=None):
		Component.__init__(self)
		if position is None:
			position = Vector()
		self.position = position
class PhysicsObject(Component):
	def __init__(self, mass=1, velocity=None, maxVelocity=1, decay=1):
		Component.__init__(self)
		self.mass = mass
		if velocity is None:
			self.velocity = Vector(0,0)
		self.decay = decay
		self.maxVelocity = maxVelocity
class Collider(Component):
	def __init__(self, points):	
		Component.__init__(self)	
		self.points = points

class Color():
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b

class Point():
	def __init__(self, vector, color):
		self.vector = vector
		self.color = color
class Sprite(Component):
	def __init__(self, points=[]):
		self.points = points
	def Load(location):
		if type(location) == Sprite:
			return
		fin = Sprite([])
		cwd = os.path.dirname(os.path.realpath(__file__))
		
		location = location.replace("[CWD]", cwd)
		fileatloc = open(location, 'r')
		for line in fileatloc:
			if "[" in line and "]" in line:
				vals = line.split("[")[1][:1]
				vals = line.split("]")[0][1:]
				x = int(vals.split(",")[0])
				y = int(vals.split(",")[1])
				if "=" in line:
					if "(" in line and ")" in line:
						vals = line.split("(")[1]
						vals = vals.split(")")[0]
						r, g, b = vals.split(",")
						r, g, b = int(r), int(g), int(b)
						fin.points.append(Point(Vector(x, y), Color(r, g, b)))
		return fin
class Script(Component):
	def __init__(self):
		Component.__init__(self)
	def loadScriptForScriptClass(location, arg=None):
		cwd = os.path.dirname(os.path.realpath(__file__))
		location = location.replace("[CWD]", cwd)
		mod = Script.loadExternalScript(location)
		class_ = getattr(mod, os.path.basename(location).replace(".py", ""))
		if issubclass(class_, Script):
			if arg is None:
				return class_()
			else:
				return class_(arg)
	def loadExternalScript(uri, absl=None):
		mod = None
		if not absl:
			uri = os.path.normpath(os.path.join(os.path.dirname(__file__), uri))
		path, fname = os.path.split(uri)
		mname, ext = os.path.splitext(fname)
		print("URI: " + uri)
		if os.path.exists(os.path.join(path,mname)+'.pyc'):
			try:
				return imp.load_compiled(mname, uri)
			except:
				pass
		if os.path.exists(os.path.join(path,mname)+'.py'):
			try:
				return imp.load_source(mname, uri)
			except Exception as e:
				print("ERROR: " + str(e))
				pass
		print(mod)
		return mod

class GameObject():
	def __init__(self, name, sprite=None, components=[]):
		self.components = []
		for comp in components:
			self.AddComponent(comp)
		self.name = name
		self.tag = None
		if sprite is not None:
			self.AddComponent(SpriteRenderer(sprite))
		self.AddComponent(Transform())
	def AddComponent(self, component):
		if issubclass(type(component), Component):
			for comp in self.components:
				if type(component) == type(comp):
					return
			component.masterObject = self
			self.components.append(component)
			if issubclass(type(component), Script):
				try:
					component.Start()
				except Exception as e:
					print(e)
					pass
		else:
			raise TypeError("Component must derive from 'Component' class")
	def RemoveComponent(self, comp_type):
		for comp in self.components:
			if type(comp) == component:
				components.remove(comp)
	def GetComponent(self, comp_type):
		for comp in self.components:
			if type(comp) == comp_type:
				#print(comp.masterObject.name + " got for " + str(comp_type))
				return comp
class Game():
	running = False
	gameObjects = []
	
	# 'Constants'
	FPS = 5
	GRAVITY = 1
	MS_PER_FRAME=None
	inputs = [] # (Keycode, Callback)
	def __init__(self):
		global game
		self.MS_PER_FRAME = 1000/self.FPS
		game = self
	def FindGameObjectOfName(self, name):
		for gObj in self.gameObjects:
			if gObj.name == name:
				return gObj
	def FindGameObjectsOfName(self, name):
		objects = []
		for gObj in self.gameObjects:
			if gObj.name == name:
				objects.append(gObj)
		return objects
	def FindObjectOfType(self, findType):
		for gObj in self.gameObjects:
			for comp in gObj.components:
				if type(comp) == findType:
					return comp
	def FindObjectsOfType(self, findType):
		objects = []
		for gObj in self.gameObjects:
			for comp in gObj.components:
				if type(comp) == findType:
					objects.append(comp)
					break
		return objects
	def FindScripts(self):
		scripts = []
		for gObj in self.gameObjects:
			for comp in gObj.components:
				if issubclass(type(comp), Script):
					scripts.append(comp) 
		return scripts
	def AddObject(self, gameObject):
		if not type(gameObject) == GameObject:
			raise TypeError("You can only add objects of the 'GameObject' class may be added") 
		self.gameObjects.append(gameObject)
	def DeleteObject(self, gameObject):
		self.gameObjects.remove(gameObject)
	def render(self):
		activePixels = []
		for renderObj in self.FindObjectsOfType(SpriteRenderer):
			#print(renderObj.masterObject.name)
			if renderObj.enabled:
				for point in renderObj.sprite.points:
					try:
						if not sense.get_pixel(point.vector.x + renderObj.masterObject.GetComponent(Transform).position.x, point.vector.y + renderObj.masterObject.GetComponent(Transform).position.y) == (point.color.r, point.color.g, point.color.b):
							sense.set_pixel(point.vector.x + renderObj.masterObject.GetComponent(Transform).position.x, point.vector.y + renderObj.masterObject.GetComponent(Transform).position.y, (point.color.r, point.color.g, point.color.b))
							activePixels.append(Point(Vector(point.vector.x + renderObj.masterObject.GetComponent(Transform).position.x, point.vector.y + renderObj.masterObject.GetComponent(Transform).position.y), point.color))
					except ValueError as e:
						continue
					except Exception as e:
						print("RenderError: " + str(e))
						continue
		for x in range(8):
			for y in range(8):
				if sense.get_pixel(x,y) == [0,0,0]:
					continue
				inList = False
				for point in activePixels:
					if (point.vector.x, point.vector.y) == (x, y):
						inList = True
				if not inList:
					sense.set_pixel(x,y,0,0,0)				
	def script(self):
		for scriptObject in self.FindScripts():
			if scriptObject.enabled:
				try:
					scriptObject.Update()
				except Exception as e:
					pass
	def AddInputCallback(self, keycode, callback):
		self.inputs.append((keycode, callback))
	def RemoveInputCallback(self, keycode, callback):
		self.inputs.remove(keycode, callback)
	def GetColliderAt(self, position):
		x = position.x
		y = position.y
		
		for col in self.FindObjectsOfType(Collider):
			for point in col.points:
				if point.vector.x + col.masterObject.GetComponent(Transform).position.x == x and point.vector.y + col.masterObject.GetComponent(Transform).position.y == y:
					return col
	def physics(self):
		for physicsObj in self.FindObjectsOfType(PhysicsObject):
			#print(physicsObj.velocity.y)
			if physicsObj.enabled:	
				physicsObj.velocity.y += self.GRAVITY
				if physicsObj.masterObject.GetComponent(Collider) is not None:
					col = physicsObj.masterObject.GetComponent(Collider)
					for point in col.points:
						x = point.vector.x + physicsObj.masterObject.GetComponent(Transform).position.x + physicsObj.velocity.x
						y = point.vector.y + physicsObj.masterObject.GetComponent(Transform).position.y + physicsObj.velocity.y
						colat = self.GetColliderAt(Vector(x, y))
						if colat is not None:
							if not colat.masterObject == physicsObj.masterObject:
								# Call OnColision() in scripts
								for script in self.FindScripts():
									try:
										script.OnCollision(colat)
									except Exception as e:
										pass
								physicsObj.veloicty = Vector(0,0)
								return
				physicsObj.masterObject.GetComponent(Transform).position.x += physicsObj.velocity.x
				physicsObj.masterObject.GetComponent(Transform).position.y += physicsObj.velocity.y
					
	def events(self):
		for evt in event.get():
			if evt.type == KEYDOWN:
				for input_ in self.inputs:
					if evt.key == input_[0]:
						input_[1]()
	def run(self):
		running = True
		print("Game init")
		init()
		display.set_mode((100,100))
		
		print(self.gameObjects[1].name)
		while True:
			display.flip()
			start = datetime.datetime.now()

			# Event Handling
			self.events()		
			# Call Update() in all scripts
			self.script()
			# Render to sense
			self.render()
			# Calculate Physics
			self.physics()
				
			timediff = start + datetime.timedelta(seconds=self.MS_PER_FRAME)
			timediff -= datetime.datetime.now()
			timediff = timediff.total_seconds() / 1000
			t.sleep(timediff)
		running = False
