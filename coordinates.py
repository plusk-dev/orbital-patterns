class Matrix():
	def __init__(self, screen) -> None:
		self.width = screen.get_width()
		self.height = screen.get_height()
		self.origin = ((self.width/2), (self.height/2))

	def coords(self, x,y):
		return (self.origin[0]+x, self.origin[1]-y)