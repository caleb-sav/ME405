from ulab import numpy
from pyb import UART

class TaskData:
    def __init__(self, period, image, theta_1, theta_2, pen, runs):
        self.period=period
        self.image = image
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.pen = pen
        self.runs = runs
        self.calculated = True
        
    def run(self):
        if self.image.read() == 1:
            print('opening circle')
            with open('circle.hpgl') as f:
                lines = f.readlines()
            self.image.write(0)
            self.calculated = False
        elif self.image.read() == 2:
            print('opening line')
            with open('line.hpgl') as f:
                lines = f.readlines()
            self.image.write(0)
            self.calculated = False
        elif self.image.read() == 3:
            print('Opening custom image')
            with open('custom.hpgl') as f:
                lines = f.readlines()
            self.image.write(0)
            self.calculated = False
            
        if self.calculated == False:
        
        
        
            movement = []
            ser = UART(2, 115200)
            
            def move(draw, vals):
                x = []
                y = []
                
                vals = vals.strip('PUD').split(',')
                
                
                for h in range(len(vals)>>1):
                    x.append(int(vals[2*h]))
                    y.append(int(vals[2*h + 1]))
                    
                shape = [draw, x, y]
                
                return shape
                    
                    
                
            
            
            
                
            lines = lines[0].split(';')
            
            for n in lines:
                command = n[0:2]
                
                if command == 'IN':
                    pass
                elif command == 'PU':
                    draw = False
                    
                    if len(n) > 2:
                        movement.append(move(draw, n))
                        
                        
                elif command == 'SP':
                    pen = int(n[2])
                    
                elif command == 'PD':
                    draw = True
                    
                    if len(n) > 2:
                        movement.append(move(draw, n))
                        pass
                
            
            xpic = []
            ypic = []
            xin = []
            yin = []
            tracex = []       # x values for the trail of pen
            tracey = []       # y values for the trail of pen
            #============ Define Constants ============
            n_a = 12     # Number of teeth (or diameter) on the small gear
            n_b = 80    # Number of teeth (or diameter) on the large gear
            P = 19.79      # Pitch of the lead screw (rad/in)
            
            k = (n_a/(P*n_b))**2    # Constant converting motor rotaiont (rad) to actuator extention (in)
            theta = [800,800]   #initial guess for theta
            theta_calc = []
            for p in range(len(movement)):
                xin += movement[p][1]
                yin += movement[p][2] 
            for x in xin:
                xpic.append((x/max(xin)*2)+5)
            
            for y in yin:
                ypic.append((y*(max(yin)/max(xin))/max(yin)*2)+6.5)
            
            # Function for g, also known as forward kinematics
            def g(pos, theta):
                # forwad kinematics
                func = [((k/20)*(theta[1])**2 - (k/20)*(theta[0])**2 +5),(numpy.sqrt(k*theta[1]**2-((k/20)*(theta[1])**2 - (k/20)*(theta[0])**2 +5)**2))]
                ans = numpy.array([[0],[1]])
                ans[0] = (pos[0] - func[0])
                ans[1] = (pos[1] - func[1])
                return ans
                pass
            
            
            # Function for the partial derivitave of g, simply just the negative of the jacobian
            def dg_dtheta(theta):
                # Partial derivative of g
                dg = numpy.array([[0,0],[0,0]])
                dg[0,0] = -(-k/10)*theta[0]
                dg[0,1] = -(k/10)*theta[1]
                dg[1,0] = -(-k*theta[0]*((k/20)*((theta[0])**2 - (theta[1])**2)-5))/(10*numpy.sqrt(k*(theta[1])**2-((k/20)*((theta[0])**2 - (theta[1])**2)-5)**2))   
                dg[1,1] = -(2*k*theta[1] + (k/100)*theta[1]*((k)*((theta[0])**2-(theta[1])**2)-100))/(2*numpy.sqrt(k*(theta[1])**2-0.0025*((k)*((theta[0])**2 - (theta[1])**2)-100)**2))  
                return dg
            
            
            # Function for Newton-Raphson Method
            def NewtonRaphson(fnc, jacobian, guess, thresh, targ):
                #set guess theta
                theta = numpy.array(guess)
                
                # Itterate until theta caluated pen point is close enough to the desired value
                while numpy.linalg.norm(fnc(targ, theta)) > thresh:
                    theta = theta - numpy.dot(numpy.linalg.inv(jacobian(theta)),fnc(targ, theta))
                # Get the Point of pen after itteration
                act = [((k/20)*(theta[1,0])**2 - (k/20)*(theta[0,0])**2 +5),(numpy.sqrt(k*theta[1,0]**2-((k/20)*(theta[1,0])**2 - (k/20)*(theta[0,0])**2 +5)**2))]
                self.theta_1.put(theta[0][0])
                self.theta_2.put(theta[1][0])
                print(theta[0][0])
                print(theta[1][0])
                print(act)
                pass
            
            
            # Function that Runs the Newton-Raphson for the shape desired
            def draw(i):
                x = xpic[i-1]
                y = ypic[i-1]
                print(i,'/',len(xpic))
                # Run the NewtonRaphson Method for the points of a circle
                pos = [x,y]
                theta_calc = (NewtonRaphson(g,dg_dtheta,theta,.01,pos))
                return theta_calc
            
            #print(len(xpic))
            [draw(i) for i in range(len(xpic))]
            #print(theta_send)
            print("Theta Calculation Complete")
            # print(theta_send)


            
            for p in range(len(movement)):
                for l in range(len(movement[p][1])):
                    if movement[p][0] == True:
                        self.pen.put(True)
                    elif movement[p][0] == False:
                        self.pen.put(False)
            self.calculated = True
            self.runs.write(True)
            

            
            