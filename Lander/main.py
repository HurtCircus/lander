from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock


class LanderGame(Widget):
    ship = ObjectProperty(None)
    surface = ObjectProperty(None)
    fuel_level_lbl = ObjectProperty(None)
    
    def update(self, dt):
        self.set_fuel_level_lbl()
        self.ship.move(self.surface.get_gravity(), self.surface.get_friction())
        self.surface.landed(self.ship)
        
    def set_fuel_level_lbl(self):
        curr_fuel_level = self.ship.get_fuel_level()
        
        if curr_fuel_level < 0:
            self.fuel_level_lbl.text = "0.0"
        else:
            self.fuel_level_lbl.text = str(self.ship.get_fuel_level())

    
class Ship(Widget):
    fuel_level = NumericProperty(500.00)
    thrust = NumericProperty(0.09)
    thrust_on = BooleanProperty(False)
    thrust_consumption = NumericProperty(-1.00)
    side_thrust_left = NumericProperty(-0.03)
    side_thrust_left_on = BooleanProperty(False)
    side_thrust_right = NumericProperty(0.03)
    side_thrust_right_on = BooleanProperty(False)
    side_thrust_consumption = NumericProperty(-0.01)
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)
    velocity = ReferenceListProperty(vel_x, vel_y)
    
    # moves the ship one step
    def move(self, grav, friction):
        self.pos = Vector(self.velocity) + self.pos
        
        if self.thrust_on and self.get_fuel_level() > 0:
            self.vel_y += self.thrust
            self.fuel_decrement(self.thrust_consumption)
        elif self.side_thrust_left_on and self.get_fuel_level() > 0:
            self.vel_x += self.side_thrust_left
            self.fuel_decrement(self.side_thrust_consumption)
        elif self.side_thrust_right_on and self.get_fuel_level() > 0:
            self.vel_x += self.side_thrust_right
            self.fuel_decrement(self.side_thrust_consumption)           
            
        self.vel_x *= (1 - friction)
        self.vel_y *= (1 - friction)
        self.vel_y -= grav
        
            
    def get_velocity(self):
        return self.velocity
    
    def get_fuel_level(self):
        return self.fuel_level
    
    def set_velocity(self, vel):
        self.velocity = vel
        
    def set_thrust_on(self):
        self.thrust_on = True
        
    def set_thrust_off(self):
        self.thrust_on = False
        
    def set_side_thrust_left_on(self):
        self.side_thrust_left_on = True
        
    def set_side_thrust_left_off(self):
        self.side_thrust_left_on = False
        
    def set_side_thrust_right_on(self):
        self.side_thrust_right_on = True
        
    def set_side_thrust_right_off(self):
        self.side_thrust_right_on = False
        
    def set_fuel_level(self, fuel_lvl):
        self.fuel_level += fuel_lvl
        
    def fuel_decrement(self, consumption):
        self.set_fuel_level(consumption)
        
class Surface(Widget):
    gravity = NumericProperty(0.03)
    friction = NumericProperty(0.01)
    ship = ObjectProperty(None)
    game = ObjectProperty(None)
    
    def get_gravity(self):
        return self.gravity
    
    def get_friction(self):
        return self.friction
    
    def landed(self, ship):
        if self.collide_widget(ship):
            self.gravity = 0
            ship.set_velocity([0, 0])
    
class LanderApp(App):
    def build(self):
        lander_game = LanderGame()
        #game.serve_ball()
        Clock.schedule_interval(lander_game.update, 1.0/60.0)
        
        return lander_game

if __name__ == '__main__':
    LanderApp().run()