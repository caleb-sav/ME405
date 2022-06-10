import pyb
import time
from math import pi
import shares

class Stepper:
    """

    
    :ivar ENN:      The pin associated with the enable pin on the driver.
    :vartype ENN:   pyb.Pin
    
    :ivar CS:       The pin associated with the chip select for the driver.
    :vartype CS:    pyb.pin
    
    :ivar SCK:      The timer object used for synchronizing the stepper motor. 
                    Its frequency is used in calculated velocity and acceleration values.
    :vartype SCK:   pyb.Timer
    
    :ivar CLK:      Clock channel of the timer object.
    
    :ivar spi:      SPI object used in communicating with the driver. The pins and timers involved are set up by default by the SPI module.
    :vartype spi:   pyb.SPI
    
    :ivar usrs:     Microstep resolution (:math:`\mu` Step ReSolution). This is a setting of 
                    the Step/Direction, often selected by bridging jumpers. It determines 
                    how many microsteps each motor step is subdivided into.                
    :vartype usrs:  integer
    
    :ivar k:        Number of steps for one revolution of the motor. This is a function of 
                    the physical motor used.
    :vartype k:     integer
    
    :ivar PULSE_div:    A parameter that subdivides the clock frequency, defining the maximum 
                        step pulse rate. PULSE_div divides the clock frequency by :math:`2^{PULSE_{div}}`
    :vartype PULSE_div: integer
    
    :ivar RAMP_div:     Similar to PULSE_div, RAMP_div scales the accleration parameters instead 
                        of the velocity.
    :vartype RAMP_div:  integer
    
    :ivar name:     A name for each instance of the class, used for debugging.
    :vartype name:  string
    
    """
    
    def __init__(self,
                 ENN: pyb.Pin,
                 #SCK: pyb.Pin,
                 CS:  pyb.Pin,
                 SCK: pyb.Timer,
                 CLK: pyb.Timer.channel,
                 spi: pyb.SPI,
                 usrs: int = 8,
                 k: int = 48,
                 PULSE_div: int = 4,        # That's the value that actually gets written.
                 RAMP_div: int = 4,         # Same here
                 name: str = "Motor"):
        
        
        # Assign attributes
        self.ENN = pyb.Pin(ENN, mode=pyb.Pin.OUT_PP, value=1)
        self.usrs = usrs
        self.k = k
        self.PULSE_div = PULSE_div
        self.RAMP_div = RAMP_div
        self.f = SCK.freq()
        
        
        # Set up SPI
        self.nCS = CS
        self.spi = spi
    
    
    def _posToByte(self, pos):          # Converts radians to a binary value
        """
        Converts an angle in radians to a binary value. The following equation is used.
        
        .. math:: 
            byte=\\frac{pos \\cdot k \\cdot usrs}{2\\pi}
        
        :param pos:     Position (in radians)
        :type pos:      float
        :return:        Position (as a binary value)
        :rtype:         integer
        
        """
        
        byte = pos*self.k*self.usrs/(2*pi)
        
        return int(byte)
    
    def _byteToPos(self, byte):     # Converts a binary value to radians
        """
        Converts a binary value back into an angle (in radians). The following equation is used.
        
        .. math::
            pos = \\frac{byte \\cdot 2\\pi}{k \\cdot usrs}
            
        :param byte:    Position (as a binary value)
        :type byte:     binary or integer
        :return:        Position (in radians)
        :rtype:         float
        """
        
        pos = byte*2*pi/(self.k*self.usrs)
        
        return pos
    
    def _velToByte(self, vel):       # Converts rad/s to a binary value
        """
        Converts an angular velocity in radians/sec to a binary value. The following equation is used.
        
        .. math:: 
            byte=\\frac{vel \\cdot k \\cdot usrs \\cdot 2^{PULSE_{div}} \\cdot 2048 \\cdot 32}{f \\cdot 2\\pi}
        
        :param pos:     Velocity (in radians/sec)
        :type pos:      float
        :return:        Velocity (as a binary value)
        :rtype:         integer
        
        """
        
        byte = vel*self.usrs*self.k*(2**self.PULSE_div)*2048*32/(self.f*2*pi)
        
        return int(byte)

    def _byteToVel(self, byte):      # Converts a binary value to rad/s
        """
        Converts a binary value back into an angular velocity (in radians/sec). The following equation is used.
        
        .. math::
            pos = \\frac{byte \\cdot f \\cdot 2\\pi}{k \\cdot usrs \\cdot 2^{PULSE_{div}} \\cdot 2048 \\cdot 32}
            
        :param byte:    Velocity (as a binary value)
        :type byte:     binary or integer
        :return:        Velocity (in radians)
        :rtype:         float
        
        """
        
        vel = int(byte)*self.f*2*pi/(self.usrs*self.k*(2**self.PULSE_div)*2048*32)
        
        return int(vel)
    
    def _accToByte(self, acc):       # Converts rad/s^2 to a binary value
        byte = acc*self.usrs*self.k*(2**self.PULSE_div)*(2**self.RAMP_div)*2**29/(self.f**2*2*pi)
        
        return int(byte)
    
    def _byteToAcc(self, byte):      # Converts a binary value to rad/s^2
        
        acc = int(byte)*self.f**2*2*pi/(self.usrs*self.k*(2**self.PULSE_div)*(2**self.RAMP_div))
        
        return int(acc)
    
    def _P_calc(self, A_max):
        """
        Calculates appropriate values for :math:`P_{mul}` and :math:`P_{div}`, which 
        are timing parameters for controlling motor stepping. First, the following 
        ratio is calculated.
        
        .. math::
            p = \\frac{0.99 A_{max}}{128 \\cdot 2^{RAMP_{div} - PULSE_{div}}}
            
        Next, starting at 0, integers are substituted for :math:`P_{div}` in the equation 
        below until :math:`P_{mul}` is acceptably between 128 and 255.
        
        .. math::
            P_{mul} = p \\cdot 2^{3 + P_{div}}
            
        At this point, the values of :math:`P_{mul}` and :math:`P_{div}` returned.
        
        :param A_max:   Maximum allowable acceleration (as a binary value)
        :type A_max:    binary
        :return:        :math:`P_{mul}`, :math:`P_{div}` in that order.
        :rtype:         tuple
        """
        p = A_max*0.99/(128*2**(self.RAMP_div - self.PULSE_div))
        
        for P_div in range(14):
            P_mul = p*2**(3+P_div)
            
            if P_mul >= 128 and P_mul <= 255:
                
                return int(P_mul), int(P_div)
            
    
    def _config(self,
                R_M: bytes = 0b00,
                REF_CONF: bytes = 0b1100,
                Vmin: int = 15,
                Vmax: int = 15,
                Amax: int = 500,
                save: bool = True):
        """
        Configures settings on the driver by writing to various registers via SPI.
        
        .. note::
           The specific addresses are hard coded for the TMC4210 stepper driver. 
           If a different driver is used, pleas modify the addresses accordingly!
        
        The R_M bits are used to select the mode as follows.
        
        .. list-table:: Mode Selection
           :widths: 10 50
           :header-rows: 1
           
           * - R_M
             - Mode
           * - 00
             - Ramp Mode: Driver controls velocity and acceleration to reach a 
               target position.
           * - 01
             - Soft Mode: Similar to ramp mode, but approaches the target more 
               gently.
           * - 10
             - Velocity Mode: Driver controls acceleration to reach a target 
               velocity.
           * - 11
             - Hold Mode: The driver controls only step and direction, leaving 
               the microcontroller in full control of the velocity and acceleration.
        
        For configuring the reference switches using REF_CONF, please consult the 
        driver datasheet.
        
        :param R_M:     Mode selection.
        :type R_M:      bytes
        :param REF_CONF:    Reference switch configuration
        :type REF_CONF:     bytes
        :param Vmin:    Minimum velocity before stopping (radians/sec)
        :type Vmin:     float
        :param Vmax:    Maximum velocity allowed (radians/sec)
        :type Vmax:     float
        :param Amax:    Maximum acceleration allowed (radians/sec^2)
        :type Amax:     float
        :param save:    Determines whether the current configuration settings are 
                        saved as attributes. On by default, switched off for temporary 
                        setting changes.
        :type save:     boolean
        """
        
        if save:
            self.R_M = R_M
            self.REF_CONF = REF_CONF
            self.Vmin = Vmin
            self.Vmax = Vmax
            self.Amax = Amax
        
        
        #================== Set Ramp Mode (R_M) ==================
        baRamp = bytearray([0b00010100,   # Set RampMode
                             0b00000000,
                             0b00000000 | REF_CONF,
                             0b00000000 | R_M])
        
        
        #================== Set IF_CONFIG (en_sd) ==================
        baIF= bytearray([0b01101000, # Enable en_sd (never changes))
                        0b00000000,
                        0b00000000,
                        0b00100000])
         
        #================== Set V_min ==================
        baVmin = bytearray([0b00000100, # Set V_min
                            0b00000000,
                            0b00000000 | self._velToByte(Vmin)>>8,
                            0b00000000 | (self._velToByte(Vmin) & 0b0000000011111111)])
        
        
        #================== Set V_max ==================
        baVmax = bytearray([0b00000110, # Set V_max
                            0b00000000,
                            0b00000000 | self._velToByte(Vmax)>>8,
                            0b00000000 | (self._velToByte(Vmax) & 0b0000000011111111)])
        

        #================== PULSE_div and RAMP_div ==================
        baDiv = bytearray([0b00011000, # Set PulseDiv and RampDiv
                           0b00000000,
                           0b00000000 | self.PULSE_div<<4 | self.RAMP_div,
                           0b00000000])
        
        #================== Set A_max ==================
        baAmax = bytearray([0b00001100, # Set A_max
                            0b00000000,
                            0b00000000 | self._accToByte(Amax)>>8,
                            0b00000011 | (self._accToByte(Amax) & 0b0000000011111111)])
        
        #================== Set P_mul and P_div ==================
        
        P_mul, P_div = self._P_calc(self._accToByte(Amax))
        
        baP = bytearray([0b00010010, 
                         0b00000000,
                         0b00000000 | P_mul,
                         0b00000000 | P_div])
        
        
        
        self.nCS.low()
        self.spi.send_recv(baIF)
        self.nCS.high()
        
        self.nCS.low()
        self.spi.send_recv(baVmax)
        self.nCS.high()
        
        self.nCS.low()
        self.spi.send_recv(baVmin)
        self.nCS.high()
        
        self.nCS.low()
        self.spi.send_recv(baDiv)
        self.nCS.high()
        
        self.nCS.low()
        self.spi.send_recv(baP)
        self.nCS.high()
        
        self.nCS.low()
        self.spi.send_recv(baAmax)
        self.nCS.high()
        
        self.nCS.low()
        self.spi.send_recv(baRamp)
        self.nCS.high()
        
        return REF_CONF, R_M
        
    def enable(self):
        """
        Enables the motor by setting the enable pin to low.

        """
        self.ENN.value(0)
    
    def disable(self):
        """
        Disables the motor by setting the enable pin to high.

        """
        self.ENN.value(1)
    
    def setTargX(self, X: int):
        """
        Defines an angle for the motor to move toward.
        
        :param X: Desired angle (in radians)
        :type X: integer

        """
        
        baX = bytearray([0b00000000,
                         0b00000000 | self._posToByte(X)>>16,
                         0b00000000 | self._posToByte(X)>>8,
                         0b00000000 | self._posToByte(X) & 0b11111111])

        
        self.nCS.low()
        data = self.spi.send_recv(baX)
        self.nCS.high()


        #for idx,byte in enumerate(data): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
    
    def setTargV(self, V: int):
        '''
        During hold mode or velocity mode, this method sets the desired velocity.
        
        :param V: Desired velocity (in radians/sec)
        :type V: integer
        '''
        # print(self._velToByte(V))
        
        baV = bytearray([0b00001000,
                         0b00000000,
                         0b00000000 | self._velToByte(V)>>8,
                         0b00000000 | self._velToByte(V) & 0b11111111])

        
        self.nCS.low()
        data = self.spi.send_recv(baV)
        self.nCS.high()
    
    
    def setActX(self, Xact: int):
        '''
        Redefines the current position of the motor for calibration. To prevent 
        the motor from moving during this process, the driver is first reconfigured 
        to velocity mode, then the new value is written to both the X_ACTUAL 
        and the X_TARGET register. Finally, the driver is reconfigured back to 
        whatever settings were previously used.
        
        :param Xact: Motor angle to be written.
        :type Xact: integer
        '''
        
        
        
        baActX  = bytearray([0b00000010,   
                             0b00000000 | self._posToByte(Xact)>>16,
                             0b00000000 | self._posToByte(Xact)>>8,
                             0b00000000 | self._posToByte(Xact) & 0b11111111])
        
        baOMode = bytearray([0b00010100,   # Set RampMode
                             0b00000000,
                             0b00000000 | self.REF_CONF,
                             0b00000000 | self.R_M])
        #print("this is baActX",baActX)
        # First, change the mode to velocity mode.
        self._config(R_M=0b10, save=False)
        
        # Write to the Actual X register
        self.nCS.low()
        self.spi.send_recv(baActX)
        self.nCS.high()
        
        # Reset the target X so it doesn't try to move.
        self.setTargX(Xact)
        
        # Return to the previous settings
        self._config(self.R_M, self.REF_CONF, self.Vmin, self.Vmax, self.Amax)
        
        
        
    
    def readX(self):
        '''
        Reads the current angle of the motor.
        
        .. note::
           The motor does not contain any kind of sensor. Position is determined 
           by dead-reckoning, so the value here only describes where the driver 
           thinks it's put the motor. If the motor is turned externally, or if 
           the motor drops steps due to excessive resistance or acceleration, this 
           value will not be accurate!
           
        
        
        :return: The current angle (in radians)
        :rtype: float
        '''
        baxread = bytearray([0b00000011,
                             0b00000000,
                             0b00000000,
                             0b00000000])
        
        self.nCS.low()
        data = self.spi.send_recv(baxread)
        self.nCS.high()
        
        # for idx,byte in enumerate(data): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
        
        val = data[1]<<16 | data[2]<<8 | data[3]
        
        #print(self._byteToPos(val))
        
        return self._byteToPos(val)
    
    def homeInit(self):
        """
        Arms the homing procedure. Once this method is called, the motor can be driven into the reference 
        switch. Not tested, not implimented.
        """
        
        baDum = bytearray([0b00011101,
                           0b11111111,
                           0b11111111,
                           0b11111111])
        
        self.nCS.low()
        data = self.spi.send_recv(baDum)
        self.nCS.high()
        
    def getLp(self):
        """
        Returns the value of the lp bit, which indicates whether the reference switch is activated. 
        Not tested, not implimented.
        
        :return:    Value of the lp bit; 0 for not active, 1 for active.
        :rtype:     bytes
        """
        
        baLp = bytearray([0b00010101,   # Get the value for lp
                          0b00000000,
                          0b00000000,
                          0b00000000])
        
        self.nCS.low()
        data = self.spi.send_recv(baLp)
        self.nCS.high()
        
        lp = data[1] & 0b00000001
        
        return lp
        
    def test(self):
        
        
        batest = bytearray([0b00010101,
                        0b00000000,
                        0b00000000,
                        0b00000000])

        self.nCS.low()
        datatest = self.spi.send_recv(batest)
        self.nCS.high()
        
        print('ba:')
        for idx,byte in enumerate(datatest): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
        
        
        
        batest = bytearray([0b01101001,
                        0b00000000,
                        0b00000000,
                        0b00000000])

        self.nCS.low()
        datatest = self.spi.send_recv(batest)
        self.nCS.high()
        
        print('baen:')
        for idx,byte in enumerate(datatest): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
        
        
        
        batest = bytearray([0b00000101,
                            0b00000000,
                            0b00000000,
                            0b00000000])

        self.nCS.low()
        datatest = self.spi.send_recv(batest)
        self.nCS.high()
        
        print('baVmin:')
        for idx,byte in enumerate(datatest): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
        
        
        
        batest = bytearray([0b00000111,
                            0b00000000,
                            0b00000000,
                            0b00000000])

        self.nCS.low()
        datatest = self.spi.send_recv(batest)
        self.nCS.high()
        
        print('baVmax:')
        for idx,byte in enumerate(datatest): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
        
        batest = bytearray([0b00011001,
                            0b00000000,
                            0b00000000,
                            0b00000000])

        self.nCS.low()
        datatest = self.spi.send_recv(batest)
        self.nCS.high()
        
        print('baDiv:')
        for idx,byte in enumerate(datatest): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
        
        batest = bytearray([0b00001101,
                            0b00000000,
                            0b00000000,
                            0b00000000])

        self.nCS.low()
        datatest = self.spi.send_recv(batest)
        self.nCS.high()
        
        print('baAmax:')
        for idx,byte in enumerate(datatest): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")
        
        
        
        batest = bytearray([0b00010011,
                            0b00000000,
                            0b00000000,
                            0b00000000])

        self.nCS.low()
        datatest = self.spi.send_recv(batest)
        self.nCS.high()
        
        print('baP:')
        for idx,byte in enumerate(datatest): print(f"b{3-idx}: {byte:#010b} {byte:#04x}")