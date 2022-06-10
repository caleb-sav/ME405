import pyb
import utime
import time


class InterfaceTask:
    ''' @brief      Interface with the user
        @details    Interfaces with the user to gather keyboard inputs that
                    control the program
    '''
    
    def __init__(self, period, image, type_runs, send_word):
        ''' @brief              Constructs the interface task.
            @details            The interface task is implemented as a finite state
                                machine.
            @param period       The period, in microseconds, between runs.
        '''     
        ## @brief           The initial state of the FSM
        #  @details         This variable allows us to set the initial state to 0
        self.S0_INIT = 0
        ## @brief           The first state of the FSM
        #  @details         This variable allows us to set the state to 1
        self.S1_WAIT_FOR_INPUT = 1
        ## @brief           The second state of the FSM
        #  @details         This variable allows us to set the state to 2
        self.S2_CIRCLE = 2
        ## @brief           The third state of the FSM
        #  @details         This variable allows us to set the state to 3
        self.S3_TRIANGLE = 3
        ## @brief           The fourth state of the FSM
        #  @details         This variable allows us to set the state to 4
        self.S4_CUSTOM = 4
        ## @brief           The fifth state of the FSM
        #  @details         This variable allows us to set the state to 5
        self.S5_TYPE = 5
        
        self.S6_STOP = 6
    
        self.period = period
        self.image = image
        self.type_runs = type_runs
        self.send_word = send_word
        
        
        ## @brief           Defines a time variable for next time
        #  @details         This variable allows us to compare time to next time,
        #                   and fall into the FSM
        self.NextTime = utime.ticks_add(utime.ticks_us(), self.period)
        ## @brief           Sets the initial state to zero
        #  @details         This variable allows us to move into the zero state of the FSM
        self.state = self.S0_INIT
        self.type_word = ""
        
        ## @brief           Interface with the keyboard
        #  @details         Allows us to take keyboard inputs, and use them in our
        #                   code as values.
        self.ser_port = pyb.USB_VCP()

        
    def run(self):
        ''' @brief          Runs the user inteface task.
            @details        The interface task is implemented as a finite state
                            machine.
        '''     
        ## @brief           Counts the time
        #  @details         Variable that counts the total time elapsed
        self.time = utime.ticks_us()
        if (utime.ticks_diff(self.time, self.NextTime) >= 0):
                if self.state == self.S0_INIT:
                    print('Press these buttons below to use the pen plotter:')
                    print('c: Plot a circle')
                    print('k: Plot a triangle')
                    print('b: Plot an uploaded image (custom.hpgl)')
                    print('t: Plot your own word (up to 9 letters)')
                    
                    self.state = self.S1_WAIT_FOR_INPUT
                    
                if self.state == self.S1_WAIT_FOR_INPUT:
                    
                    if self.ser_port.any():
                        ## @brief           Variable that is the user input
                        #  @details         Variable that is defined as the keyboard stroke
                        #                   pressed by the user
                        self.userinput = self.ser_port.read(1)
                        
                        if(self.userinput == b'c'):
                            print('Plotting circle')
                            self.state = self.S2_CIRCLE
                            
                        elif(self.userinput == b'k'):
                            print('Plotting triangle')
                            self.state = self.S3_TRIANGLE
                            
                            
                        elif(self.userinput == b'b'):
                            print('Plotting custom image')
                            self.state = self.S4_CUSTOM
                            
                            
                        elif(self.userinput == b't'):
                            print('Please enter your word')
                            self.input_state = 1
                            self.state = self.S5_TYPE
                            
                             
                        
                            
                        
                        
                        
                            
                           
                    
                elif self.state == self.S2_CIRCLE:
                    self.image.write(1)
                    self.state = self.S1_WAIT_FOR_INPUT
                    
                elif self.state == self.S3_TRIANGLE:
                    self.image.write(2)
                    self.state = self.S1_WAIT_FOR_INPUT 
                    
                elif self.state == self.S4_CUSTOM:
                    self.image.write(3)
                    self.state = self.S1_WAIT_FOR_INPUT
                    
                elif self.state == self.S5_TYPE:
                    
                    if self.input_state == 1:
                        
                            ## @brief           Variable that is the user input
                            #  @details         Variable that is defined as the keyboard stroke
                            #                   pressed by the user
                        
                        if self.ser_port.any():
                            
                            self.char_in2 = self.ser_port.read(1).decode()
                            
                            
                            if self.char_in2 =='\x7F':
                                self.send_word.get()
                                print(self.type_word)
                                self.input_state = 1
                                
                            elif self.char_in2 == '\r' or self.char_in2 == '\n':
                                self.input_state = 2

                            else:
                                self.type_word += self.char_in2
                                print(self.type_word)
                                self.send_word.put(str(self.char_in2))
                                self.input_state = 1
                                
                                
                                
                    elif self.input_state == 2:
                        print('Now Printing the word', self.type_word)
                        self.type_runs.write(True)
                        self.state = self.S1_WAIT_FOR_INPUT
                    
                elif self.state == self.S6_STOP:
                    self.Balance.write(False)
                    self.state = self.S1_WAIT_FOR_INPUT