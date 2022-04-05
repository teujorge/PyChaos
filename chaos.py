import random

from time import sleep

import pyglet
from pyglet.window import key
from pyglet.window import mouse

from pyglet import clock


class Point:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y


class Piglet(pyglet.window.Window):

    def __init__(self, mode="triangle", dots=0) -> None:

        # default window
        self.window = super()
        self.window.__init__()

        # internally openGL primatives (for circles)
        self.batch = pyglet.graphics.Batch()

        # chaos game
        self.mode = mode
        if self.mode == "triangle":
            # triangle
            self.vertices = [ Point(50, 50), Point(self.window.width//2, self.window.height - 50), Point(self.window.width - 50, 50), Point(1000,1000) ]
        elif self.mode == "square":
            # square
            self.vertices = [ Point(50, 50), Point(self.window.width-50, 50), Point(self.window.width - 50, self.window.height-50), Point(50, self.window.height-50) ]
        self.circles = []

        # initial point
        self.choice = -1
        self.current = self.random_point(self.window.width, self.window.height)
        circle = pyglet.shapes.Circle(self.current.x, self.current.y, 2, color=(200, 200, 180), batch=self.batch)
        self.circles.append(circle)

        # display vertices text
        self.pointA = pyglet.text.Label(
            'A',
            font_name='Times New Roman',
            font_size=24,
            x=self.vertices[0].x, y=self.vertices[0].y,
            anchor_x='center', anchor_y='center'
        )
        self.pointB = pyglet.text.Label(
            'B',
            font_name='Times New Roman',
            font_size=24,
            x=self.vertices[1].x, y=self.vertices[1].y,
            anchor_x='center', anchor_y='center'
        )
        self.pointC = pyglet.text.Label(
            'C',
            font_name='Times New Roman',
            font_size=24,
            x=self.vertices[2].x, y=self.vertices[2].y,
            anchor_x='center', anchor_y='center'
        )
        self.pointD = pyglet.text.Label(
            'C',
            font_name='Times New Roman',
            font_size=24,
            x=self.vertices[3].x, y=self.vertices[3].y,
            anchor_x='center', anchor_y='center'
        )

        # display point counter
        self.infographic = pyglet.text.Label(
            'ct:  ',
            font_name='Times New Roman',
            font_size=12,
            x=100, y=self.window.height-20,
            anchor_x='center', anchor_y='center'
        )

        if dots==0:
            # start clock
            pyglet.clock.schedule_interval(self.update, 0.1)
        else:
            # init with circles
            self.add_circles(dots)
            self.infographic.text = "ct: " + str(dots)
    # end init

    # display window
    def start(self):
        # default event loop
        pyglet.app.run()

    # use a decorator to redraw contents
    # @window.event
    def on_draw(self):
        self.window.clear()
        self.pointA.draw()
        self.pointB.draw()
        self.pointC.draw()
        self.pointD.draw()
        self.infographic.draw()

        ct = 0
        self.infographic.text = "ct: " + str(ct)
        for circle in self.circles:
            circle.draw()
            ct+=1
            self.infographic.text = "ct: " + str(ct)

    # list of circles
    def add_circles(self, num):
        for i in range(num):
            # class Circle(x, y, radius, segments=None, color=(255, 255, 255), batch=None, group=None)
            self.choice = self.random_vertex(self.choice)
            self.current = self.mid_point( self.current , self.vertices[self.choice] )
            circle = pyglet.shapes.Circle(self.current.x, self.current.y, .75, color=(200, 200, 80), batch=self.batch)
            if not circle in self.circles:
                self.circles.append(circle)
            # self.circles.append(circle)

    # clock to update and add circles overtime
    def update(self, dt):
        self.add_circles(1)
        # print("update")
        pass

    # attach keyboard events
    # @window.event
    def on_key_press(self, symbol, modifiers):
        if symbol == key.A:
            self.add_circles(100)
        else:
            print()
            print("mod:", modifiers)
            print("key:", symbol)

    # get middle of two points
    def mid_point(self, p1:Point, p2:Point) -> Point:
        x = (p1.x + p2.x)/2
        y = (p1.y + p2.y)/2
        return Point( x , y )

    # get a random vertex
    def random_vertex(self, previous) -> int:
        if self.mode == "triangle":
            choice = random.randint(0, 2) # triangle
        elif self.mode == "square":
            choice = random.randint(0, 3) # square
            while choice == previous:
                choice = random.randint(0, 3) # square
        return choice

    # get random point
    def random_point(self, x_lim, y_lim) -> Point:
        x = random.randint(0, x_lim)
        y = random.randint(0, y_lim)
        return Point( x , y )



