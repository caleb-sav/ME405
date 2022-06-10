from pyb import Pin, Timer
from ulab import numpy


class dcDriver:
    """
    :ivar PWM_pin: Pin connected to the signal line for the servo.
    :vartype PWM_pin: pyb.Pin
    
    :ivar timer:    The timer number to be used for PWM. Set to Timer 2 by default.
    :vartype timer:       integer
    
    :ivar ch:       Channel number to be used for PWM. Set to Channel 1 by default.
    :vartype ch:       integer
                
    """
    def __init__(self, PWM_pin: Pin = Pin.cpu.A0, timer: int = 2, ch: int = 1):
        
    
        # Create Timer stuff
        tim = Timer(timer, freq = 50)
        self.PWM = tim.channel(ch, Timer.PWM, pin = PWM_pin, pulse_width = 1500) #<-- Pulse Width 1.5 ms.
        
        # Define the pulse widths for UP and DOWN.
        self.UP = 80000
        self.DOWN = 120000
        
    
    def up(self):
        """
        Sets the pen to the 'up' position.
        """
        self.PWM.pulse_width(self.UP)
    
    def down(self):
        """
        Sets the pen to the 'down' position.
        """
        self.PWM.pulse_width(self.DOWN)
       
    def toggle(self):
        """
        Toggles the pen between 'up' and 'down' positions.
        """
        if self.PWM.pulse_width() == self.UP:
            self.PWM.pulse_width(self.DOWN)
            
        else:
            self.PWM.pulse_width(self.UP)