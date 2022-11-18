import math
import random
from abc import abstractmethod
from tkinter import Tk, ttk
from PIL import Image, ImageDraw, ImageTk
from vect2d import Vect2D


class RGBAColor():
    def __init__(self, r:int=255, g:int=255, b:int=255, a:int=255, randomize:bool=False):
        self.__r = r
        self.__g = g
        self.__b = b
        self.__a = a

        if randomize:
            self.randomize_color()
        
        @property
        def r(self):
            return self.__r
        
        @property
        def g(self):
            return self.__g
        
        @property
        def b(self):
            return self.__b
        
        @property
        def a(self):
            return self.__a

        
    def randomize_color(self):
        self.__r = random.randint(0, 255)
        self.__g = random.randint(0, 255)
        self.__b = random.randint(0, 255)
        self.__a = random.randint(0, 255)


class Drawable():
    def __init__(self, border_color, fill_color, position:Vect2D, size:Vect2D):
        self.__border_color = border_color
        self.__fill_color = fill_color
        self.__position = position
        self.__size = size


    @abstractmethod
    def draw(self):
        pass


    @property
    def size(self):
        return self.__size
    
    @property
    def color(self):
        return self.__color
    
    @property
    def position(self):
        return self.__position


class Movable():
    def __init__(self, acceleration, max_speed, speed):
        self.__acceleration = acceleration
        self.__speed = speed
        self.__max_speed = max_speed


    def move(self, time):
        if self.__speed > self.__max_speed:
            self.__speed == self.__max_speed

        self.__position += self.__speed * time + self.__acceleration * 0.5 ** 2

    @property
    def max_speed(self):
        return self.__max_speed
class Touchable():
    def __init__(self):
        pass

    @abstractmethod
    def checkCollision(self):
        pass

class Updatable():
    def __init__(self):
        pass

    @abstractmethod
    def tick(self):
        pass

class App():
    def __init__(self):
        self.__gui = GUI(500,500)
        #self.__simulation = Simulation()
    
    
class GUI(Tk):
    
    def __init__(self, width, height):
        Tk.__init__(self)
        self.__main_frame = MainFrame(Vect2D(500,500), RGBAColor(0 ,0, 0), Vect2D(0,0)) 
        self.title('Boids')
        self.__width = width
        self.__height = height
        self.geometry(str(int(self.__width)) + 'x' + str(int(self.__height)))
        self.iconbitmap('boids.ico')
        
        self.mainloop()
               
    # GUI getters #    
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

     
class Entity(Drawable, Updatable):
    def __init__(self, border_color, fill_color, position, size):
        Drawable.__init__(self, border_color, fill_color, position, size)
        Updatable.__init__(self)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def tick(self):
        pass
     
class Simulation(Updatable):
    def __init__(self, sprites:list[Entity]):
        self.__sprites = sprites

    def tick(self):
        for sprite in self.__sprites:
            sprite.tick()


class MainFrame(ttk.Frame, Drawable):
    def __init__(self, border_color=None, fill_color=None, position=None, size:Vect2D=None):
        ttk.Frame.__init__(self, root=None, text=None)
        Drawable.__init__(self, border_color,  fill_color, position, size)
        self.__main_panel = ControlBar("Main Panel")
        self.__view_window = ViewWindow(size, fill_color)   
        self.__main_panel.grid(row=0, column=0, sticky='nsew')
        self.__view_window.grid(row=0, column=1, rowspan=3, sticky="nsew") 
        
        


class ControlBar(ttk.Frame):
    def __init__(self, title):
        ttk.Frame.__init__(self, title=None)
        self.__control_panel = StartStopPanel("Control")
        self.__param_panel = ParamPanel("Paramètre")
        self.__visual_param_panel = VisualParamPanel("Paramètre visuel")
        self.__control_panel.grid(row=0, column=0)
        self.__param_panel.grid(row=1, column=0)
        self.__visual_param_panel.grid(row=2, column=0)



class StartStopPanel(ttk.LabelFrame):
    def __init__(self, text): 
        ttk.LabelFrame.__init__(self, root=None, text=text)
        self.__start_button = ttk.Button(self, text="Start")
        self.__stop_button = ttk.Button(self, text="Stop")
        self.__next_button = ttk.Button(self, text="Next Step")
        self.__start_button.pack()
        self.__stop_button.pack()
        self.__next_button.pack()


class ViewWindow(ttk.Label, Drawable):
    def __init__(self, border_color=None, fill_color=None, position=None, size=None):
        ttk.Label.__init__(self, root=None, text=None)
        Drawable.__init__(self, border_color, fill_color, position, size)
        self.__image = Image.new('RGBA', (int(400), int(100)), (0, 0, 0))
        self.__image_draw = ImageDraw.Draw(self.__image)
        self.__image_tk = ImageTk.PhotoImage(self.__image)
        self.__image_label = ttk.Label(self, image=self.__image_tk)
        self.__image_label.grid(row=0, column=0, sticky='ns')
        self.__image_label.columnconfigure(0, minsize=600, weight=1)



class ParamPanel(ttk.LabelFrame):
    def __init__(self, title):
        ttk.LabelFrame.__init__(self, root=None, text=title)
        self__test_btn = ttk.Button(self, text="Test")
        self__test_btn.pack()
        


class VisualParamPanel(ttk.LabelFrame):
     def __init__(self, title):
        ttk.LabelFrame.__init__(self, root=None, text=title)
        self__test_btn = ttk.Button(self, text="Test")
        self__test_btn.pack()

class SimParamPanel(ParamPanel):
    def __init__(self):
        pass    

    @abstractmethod
    def draw(self):
        pass
    
    @property
    def sprites(self):
        return self.__sprites
    

    
    @abstractmethod
    def check_collision(self):
        pass
    
class Circle(Entity, Touchable):
    def __init__(self, border_color, fill_color, position:Vect2D, radius:int):
        Entity.__init__(self, border_color=border_color, fill_color=fill_color, position=position, size=(radius*2, radius*2))

        self.__radius = radius

    def check_collision(self):
        Touchable.check_collision() 

    def draw(self):
        return ([(self.__position.x - self.__radius, self.__position.y - self.__radius), self.__position.x + self.__radius, self.__position.y + self.__radius], self.__fill_color, self.__border_color)

    def tick(self, time):
        self.move(time)

class StaticCircle(Circle):
    def __init__(self):
        Circle.init(self)


class SteeringBehavior():
    def __init__(self, attraction_repulsion_force=1, distance_to_target=None):
        self.__attraction_repulsion_force = attraction_repulsion_force
        self.__distance_to_target = distance_to_target
        self.__resulting_direction = None

    @abstractmethod    
    def behave(self, origin_entity:Entity, target_entity:Entity):
        pass  
    
class CollisionAvoidance(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, origin_entity: Entity, target_entity: Entity):
        return super().behave(origin_entity, target_entity)
 
    
class Wander(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, origin_entity: Entity, target_entity: Entity):
        return super().behave(origin_entity, target_entity)
 
    
class FleeArrival(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
 
    
class Seek(SteeringBehavior):
    def __init__(self):
        super().__init__(self)
        
    def behave(self, this_entity: Entity, target_entity: Entity):
        return super().behave(this_entity, target_entity)
    
class Piloted():
    def __init__(self, slowing_distance:int, steering_force:Vect2D, desired_speed:Vect2D, steering_behaviors:list[SteeringBehavior], acceleration:Vect2D, max_steering_force:Vect2D):
        self.__slowing_distance = slowing_distance
        self.__steering_force = steering_force
        self.__desired_speed = desired_speed
        self.__steering_behaviors = steering_behaviors
        self.__max_steering_force = max_steering_force

    def steer(self, target_entity=None):
        for steering_behavior in self.__steering_behaviors:
            self.__steering_force += steering_behavior.behave(self, target_entity)
        
        if self.__steering_force.length > self.max_speed:
            self.__steering_force.length = self.max_speed
        


class DynamicCircle(Circle, Movable, Piloted):
    def __init__(   self,
                    border_color=RGBAColor(randomize=True),
                    fill_color=RGBAColor(randomize=True),
                    position=Vect2D(random.randrange(0,100),random.randrange(0,100)),
                    radius=random.randrange(5,10),
                    acceleration=Vect2D(0,100),
                    speed=Vect2D(random.randrange(-10,10),random.randrange(-10,10)),
                    max_speed=1,
                    slowing_distance=10,
                    steering_force=Vect2D(0,0),
                    steering_behaviors=None,
                ):

        Circle.__init__(border_color, fill_color, position, radius)
        Movable.__init__(acceleration, max_speed, speed)
        Piloted.__init__(slowing_distance, steering_force, steering_behaviors, )

    def move(self, time):
        Movable.move(time)
    


def main():
    App()


if __name__ == '__main__':
    main()