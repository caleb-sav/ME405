import utime
import time
from pyb import Pin, SPI, Timer
import stepper
import dcDriver

class TaskMotor:
    
    def __init__(self,period, MotorNum, theta_1, theta_2, pen, runs,type_runs, send_word):
        ## @brief           Defines the period of the encoder 
        #  @details         Defines the period of the encoder as the largest 16 bit 
        #                   number, 65,535
        self.period=period
        
        ## @brief           Defines the count used to run the task
        #  @details         Uses onboard Utime timer to create a count to be 
        #                   sure our task is running on time
        self.count=utime.ticks_us()
        ## @brief           Allows us to choose which motor to run
        #  @details         We can input the motor number (1 or 2) for the motor 
        #                   we want to run
        self.MotorNum = MotorNum
        ## @brief           This creates an object from motor driver for each motor
        #  @details         This variable creates an object from the motor driver,
        #                   which will allow us to utilize multiple motors without
        #                   creating multiple files
        #self.MotorObj=MotorObj

        ## @brief           Creates an object for our motor driver
        #  @details         This variable takes in the timer number, to fully
        #                   define our motor driver
        #self.motordrive=motordrive
        ## @brief           Enables the motor driver
        #  @details         This variable enables the motor driver so that we can 
        #                   actually run the motor for a given duty cycle
        
        
        #self.motordrive.enable()
        
        ## @brief           Variable for the current time
        #  @details         This variable allows us to count using the onboard timer
        self.count=utime.ticks_us()
        
        
        self.state=0
        
        
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.pen = pen
        self.runs = runs
        self.type_runs = type_runs
        self.send_word = send_word
        
    def run(self):
        ''' @brief              Runs the functions in TaskMotor
            @details            This function is responsible for running the functions 
                                in Motor Task and actually allows the motors to run
        '''
        if self.count>=self.period:
            self.count+=self.period
        
            if self.state==0:
                    self.thresh = 6  # [rad] How close the motor needs to be to the target before it continues to the next point.
                    
                    ENN1 = Pin.cpu.C3
                    ENN2 = Pin.cpu.C2
                    CLK = Pin.cpu.C7
                    CS1 = Pin(Pin.cpu.B6, mode=Pin.OUT_PP, value=1)
                    CS2 =Pin(Pin.cpu.B0, mode=Pin.OUT_PP, value=1)
    
                    tim = Timer(3, period = 3, prescaler = 0)
                    clk = tim.channel(2, pin=CLK, mode=Timer.PWM, pulse_width=2)
    
                    spi = SPI(2, SPI.CONTROLLER, baudrate=1000000, polarity=1, phase=1)
                    
                    self.motor1 = stepper.Stepper(ENN1, CS1, tim, clk, spi)
                    self.motor2 = stepper.Stepper(ENN2, CS2, tim, clk, spi)
                    self.motor1._config(Vmax = 30)
                    self.motor2._config(Vmax = 30)
                    self.motor1.setActX(0)
                    self.motor2.setActX(0)
                    self.motor1.setActX(1154)
                    self.motor2.setActX(1753)
                    self.pen_ud = dcDriver.dcDriver()
                    
                    self.pen_ud.down()
                    time.sleep(1)
                    self.pen_ud.up()
                    self.n = 1
                    self.state=1
                    
            elif self.state==1:
                if self.runs.read() == True:
                        #print('running the motors')
                        self.motor1.enable()
                        self.motor2.enable()
                        self.state=2
                else:
                    self.motor1.disable()
                    self.motor2.disable()
                    
                    
                   
            elif self.state==2:
                
                if self.theta_2.num_in() > 0:
                    self.target1 = self.theta_1.get()
                    self.target2 = self.theta_2.get()
                    #print(f'Next point: {self.target1}, {self.target2}')
                    
                    self.motor1.setTargX(self.target1)
                    self.motor2.setTargX(self.target2)
                    pens= self.pen.get()
                    print("want = ,",(self.target1),(self.target2))
                    print("have =", self.motor1.readX(),self.motor2.readX())
                    if pens == False:
                        self.motor1._config(Vmax = 30)
                        self.motor2._config(Vmax = 30)
                        print(" ")
                        print("PEN IS GOING TO BE UP LETS MOVE")
                        print(" ")
                        self.pen_ud.up()
                    elif pens == True:
                        if self.n < 3:
                            self.n += 1
                        else:
                            self.motor1._config(Vmax = 25)
                            self.motor2._config(Vmax = 25)
                            print("pen down")
                            self.pen_ud.down()
                    self.state=3
                elif self.send_word.num_in() > 0:
                    for i in range(self.pen.num_in()):
                        self.pen.get()
                    self.pen_ud.up()
                    self.n = 1
                    self.type_runs.write(True)
                    self.runs.write(False)
                else:
                    print("picture is done")
                    self.pen_ud.up()
                    self.motor1.setTargX(1154)
                    self.motor2.setTargX(1753)
                    
                    
            
            
            
            
            
            elif self.state==3:
                diff1 = abs(self.motor1.readX() - self.target1)
                diff2 = abs(self.motor2.readX() - self.target2)
                 
                if diff1 <= self.thresh and diff2 <= self.thresh:
                    print("next point")
                    self.state = 1
                
                
                    

           
        