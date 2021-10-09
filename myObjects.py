
class MyObject:
	def __init__ (self):
		self.port = None
		self.portdir = None
		self.shape = None
		self.shapedir = None
		self.layer = None
		self.x1 = None
		self.x2 = None
		self.y1 = None
		self.y2 = None
		# offset before scale
		self.xoffset = 0
		self.yoffset = 0
		# scale tgif(1 cm = 50 unit) to lef(6 um)
		self.xscale = 1 / 100 * 12 
		self.yscale = 1 / 100 * 12 
		self.unitHeight = 13.5 * 100
		self.unitWidth = 3 * 100
		# finish flag. not lef out "NO", lef out "DONE"
		self.done = "NO"
	
	def set_port(self, port):
		self.port = port
		if((port == 'Q') or (port == 'QN') or (port == 'Y') or (port == 'YB')):
			self.portdir = 'OUTPUT'
		else:
			self.portdir = 'INPUT'

	def add_poly(self, port, layer, x1, x2, y1, y2):
		self.port = port
		self.layer = layer
		if(int(x1) < int(x2)):
			self.x1 = int(x1)
			self.x2 = int(x2)
		else:
			self.x1 = int(x2)
			self.x2 = int(x1)
		if(int(y1) < int(y2)):
			self.y1 = int(y1)
			self.y2 = int(y2)
		else:
			self.y1 = int(y2)
			self.y2 = int(y1)
		self.shape = "line"
		if(x1 == x2):
			self.shapedir = "vertical"
		elif(y1 == y2):
			self.shapedir = "horizontal"
	
	def poly2path(self, width, box):
		tmp_x1 = self.x1
		tmp_y1 = self.y1
		tmp_x2 = self.x2
		tmp_y2 = self.y2
		self.x1 = (int(tmp_x1) + int(self.xoffset)) * self.xscale - width / 2
		self.x2 = (int(tmp_x2) + int(self.xoffset)) * self.xscale + width / 2
		# reverse y1 and y2
		self.y2 = ((self.unitHeight) - (int(tmp_y1) + int(self.yoffset))) * self.yscale + width / 2
		self.y1 = ((self.unitHeight) - (int(tmp_y2) + int(self.yoffset))) * self.yscale - width / 2
		if(self.x1 < box.x1):
			self.x1 = box.x1
		if(self.y1 < box.y1):
			self.y1 = box.y1
		if(self.x2 > box.x2):
			self.x2 = box.x2
		if(self.y2 > box.y2):
			self.y2 = box.y2
		self.shape = "path"
	
	def add_box(self, port, layer, x1, y1, x2, y2):
		self.port = port
		self.layer = layer
		if(int(x1) < int(x2)):
			self.x1 = int(x1)
			self.x2 = int(x2)
		else:
			self.x1 = int(x2)
			self.x2 = int(x1)
		if(int(y1) < int(y2)):
			self.y1 = int(y1)
			self.y2 = int(y2)
		else:
			self.y1 = int(y2)
			self.y2 = int(y1)
		#print("rect: "+str(x1)+","+str(y1)+" "+str(x2)+","+str(y2)+"\n")
		self.shape = "rectangle"

	def box2rect(self):
		tmp_x1 = self.x1
		tmp_y1 = self.y1
		tmp_x2 = self.x2
		tmp_y2 = self.y2
		self.x1 = (int(tmp_x1) + int(self.xoffset)) * self.xscale
		self.x2 = (int(tmp_x2) + int(self.xoffset)) * self.xscale
		# box is not need to rotate
		#self.y1 = ((self.unitHeight) - (int(tmp_y1) + int(self.yoffset))) * self.yscale
		#self.y2 = ((self.unitHeight) - (int(tmp_y2) + int(self.yoffset))) * self.yscale
		self.y1 = ( (int(tmp_y1) + int(self.yoffset))) * self.yscale
		self.y2 = ( (int(tmp_y2) + int(self.yoffset))) * self.yscale
		self.shape = "path"
	
	def eps2lef(self):
		self.x1 = (self.x1 * self.xscale) + self.xoffset
		self.y1 = (self.y1 * self.yscale) + self.yoffset
		self.x2 = (self.x2 * self.xscale) + self.xoffset
		self.y2 = (self.y2 * self.yscale) + self.yoffset
		self.shape = "rectangle"
