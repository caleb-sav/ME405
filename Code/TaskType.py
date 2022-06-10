
from ulab import numpy
from pyb import UART
class TaskType:
    def __init__(self, period, theta_1, theta_2, pen, runs, type_runs, send_word):
        self.period=period
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.pen = pen
        self.runs = runs
        self.type_runs = type_runs
        self.send_word = send_word
        self.calculated = True
        self.n = 0
    def run(self):
        
        if self.type_runs.read() == True:
            if self.send_word.num_in() > 0:
                if self.n == 0:
                    if self.send_word.num_in() <= 3:
                        self.size = 3
                    elif self.send_word.num_in() == 4:
                        self.size = 2.
                    elif self.send_word.num_in() == 5:
                        self.size = 1.8
                    elif self.send_word.num_in() == 6:
                        self.size = 1.3
                    elif self.send_word.num_in() == 7:
                        self.size = 1.2
                    elif self.send_word.num_in() == 8:
                        self.size = 1.1
                    elif self.send_word.num_in() == 9:
                        self.size = 1
                    
                self.letter = self.send_word.get()
                
                if self.letter == "a":
                    print('Typing A')
                    with open('A.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "b":
                    print('Typing B')
                    with open('B.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "c":
                    print('Typing C')
                    with open('C.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "d":
                    print('Typing D')
                    with open('D.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "e":
                    print('Typing E')
                    with open('E.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "f":
                    print('Typing F')
                    with open('F.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "g":
                    print('Typing G')
                    with open('G.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "h":
                    print('Typing H')
                    with open('H.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "i":
                    print('Typing I')
                    with open('I.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "j":
                    print('Typing J')
                    with open('J.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "k":
                    print('Typing K')
                    with open('K.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "l":
                    print('Typing L')
                    with open('L.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "m":
                    print('Typing M')
                    with open('M.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "n":
                    print('Typing N')
                    with open('N.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "o":
                    print('Typing O')
                    with open('O.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "p":
                    print('Typing P')
                    with open('P.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "q":
                    print('Typing Q')
                    with open('Q.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "r":
                    print('Typing R')
                    with open('R.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "s":
                    print('Typing S')
                    with open('S.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "t":
                    print('Typing T')
                    with open('T.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "u":
                    print('Typing U')
                    with open('U.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "v":
                    print('Typing V')
                    with open('V.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "w":
                    print('Typing W')
                    with open('W.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "x":
                    print('Typing X')
                    with open('X.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "y":
                    print('Typing Y')
                    with open('Y.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False
                elif self.letter == "z":
                    print('Typing Z')
                    with open('Z.hpgl') as f:
                        lines = f.readlines()
                    self.calculated = False

                
            else:
                self.type_runs.write(False)
            
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
                xpic.append((x/max(xin)*self.size)+1.5 + self.n*self.size)
            
            for y in yin:
                ypic.append((y*(max(yin)/max(xin))/max(yin)*self.size)+4.5)
            
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

            
            self.pen.put(False)
            for p in range(len(movement)):
                for l in range(len(movement[p][1])):
                    if movement[p][0] == True:
                        self.pen.put(True)
                    elif movement[p][0] == False:
                        self.pen.put(False)
            self.calculated = True
            self.type_runs.write(False)
            self.runs.write(True)
            self.n += 1
            

            
            