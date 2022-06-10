import shares
import pyb
import TaskMotor
import InterfaceTask
import TaskData
import TaskType
import stepper

def main():
    ''' @brief      The main program
        @details    Runs the main program and creates our shared variables for our other tasks to use 
    '''



    
    ## @brief           Shared variable for motor number
    #  @details         This variale allows us to use choose which motor to run
    MotorNum=shares.Share(True)
    
    ## @brief           Shared variable for the measured steps
    #  @details         This variable allows us to share angular velocity between files
    measured1=shares.Share(0)
    measured2=shares.Share(0)
    image=shares.Share(0)
    runs = shares.Share(False)
    type_runs = shares.Share(False)
    theta_1 = shares.Queue()
    theta_2 = shares.Queue()
    pen = shares.Queue()
    send_word = shares.Queue()
    
   
    ## @brief           Creates an object for our motor driver
    #  @details         This variable takes in the motor number, and duty
    #                   to choose which motor to run at a certain duty
    #MotorObj=MotorDriver.Motor(MotorNum)
    ## @brief           This creates an object for the closed loop control
    #  @details         This variable creates an object for closed loop control
    #                   so we can input a desired RPM and Kp value
    
    ## @brief           Creates an object for our motor driver
    #  @details         This variable takes in the timer number, for this motor driver
    #motordrive = MotorDriver.DRV8847(3)


   
    task1=InterfaceTask.InterfaceTask(500, image, type_runs, send_word)
    ## @brief           Variable for the third task (Task Motor)
    #  @details         This variable allows the input of period (microsec),
    #                   motor object, duty, motor driver, and motor number
    task2=TaskMotor.TaskMotor(500, MotorNum, theta_1, theta_2, pen, runs, type_runs, send_word)
    
    task3=TaskData.TaskData(500, image, theta_1, theta_2, pen, runs)
    task4 = TaskType.TaskType(500, theta_1, theta_2, pen, runs, type_runs, send_word)
    
    ## @brief           A list of tasks to run
    TaskList = [task1, task2,task3,task4]

    while(True):
        try:
            for task in TaskList:
                task.run()
            
        except KeyboardInterrupt:
            break
    
    print('Program Terminating')
    #pyb.Pin(pyb.Pin.cpu.A5, mode=pyb.Pin.OUT_PP)

if __name__=='__main__':
    main()



