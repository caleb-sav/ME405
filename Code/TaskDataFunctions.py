def g(pos, theta):
    """
    This function represents the forward kinematics for the system. It accepts a target 
    position in X Y coordinates, as well as positions of the two motors, and returns an 
    error value: the difference between them.
    
    .. math:: err = \\bar{X}_{targ} - \\bar{f}(\\theta)
    
    where
    
    .. math:: 
        
        f_x(\\theta_1, \\theta_2) &= \\frac{k \\left(\\theta_{2}^2 - \\theta_{1}^2\\right)}{2 l}  + \\frac{l}{2}
        
        
        f_y(\\theta_1, \\theta_2) &= \\sqrt{k \\theta_{2}^2 - \\left(\\frac{k \\left(\\theta_{2}^2 - \\theta_{1}^2\\right)}{2 l}  + \\frac{l}{2}\\right)^2}
    
    where :math:`k` refers to the conversion factor between motor angle and power screw 
    position, and :math:`l` refers to the distance between the two pivot points; 
    10 inches in our case. K is derived on the Mechanical Design page under Analysis.
    
    :param pos: Target position in X Y coordinates
    :param theta: A set of theta values describing the position of the motors.
    """
    #,(numpy.sqrt(k*theta[1]**2-((k/20)*(theta[1])**2 - (k/20)*(theta[0])**2 +5)**2))]
    pass


# Function for the partial derivitave of g, simply just the negative of the jacobian
def dg_dtheta(theta):
    """
    Partial derivative of position with respect to theta. This is the negative of the 
    jacobian, and is passed into the Newton-Raphson function. It is calculated from 
    the motor positions (in radians) using the following equations
    
    .. math::
        
       \\frac{\\partial g}{\\partial \\bar{\\theta}} = \\begin{bmatrix}
       f_{0,0} & f_{0,1}\\


       f_{1,0} & f_{1,1}
        
       \\end{bmatrix}
       
    
    where
    
    .. math::
       
       f_{0,0} &= \\frac{k \\theta_1}{l} \\
           
    
       f_{0,1} &= \\frac{-k \\theta_2}{l} \\
           
       
       f_{1,0} &= \\frac{k \\theta_1 \\left( \\frac{k (\\theta_{1}^2 - \\theta_2^2)}{2 l} - \\frac{l}{2} \\right)}{l\\sqrt{k\\theta_2^2- \\left( \\frac{k (\\theta_1^2 - \\theta_2^2)}{2 l} - \\frac{l}{2} \\right)^2}} \\
           
      
       f_{1,1} &= -\\frac{2k\\theta_2 + \\frac{k\\theta_2}{l^2} \\left(k(\\theta_1^2-\\theta_2^2)-l^2 \\right)}{2\\sqrt{k\\theta_2^2- \\left(\\frac{k(\\theta_1^2 - \\theta_2^2)-l^2}{2l}\\right)^2}}
       
    In these equations, :math:`l` refers to the distance between the pivots (10 in) 
    and :math:`k` is the coefficient which converts motor angle to linear position of the arm. 
    The derivation of :math:`k` can be found under Analysis section on the Mechanical Design page.
    
    :param theta: The set of the two motor angles (in radians)
    """
    # dg[0,0] = -(-k/10)*theta[0]
    # dg[0,1] = -(k/10)*theta[1]
    # dg[1,0] = -(-k*theta[0]*((k/20)*((theta[0])**2 - (theta[1])**2)-5))/(10*numpy.sqrt(k*(theta[1])**2-((k/20)*((theta[0])**2 - (theta[1])**2)-5)**2))   
    # dg[1,1] = -(2*k*theta[1] + (k/100)*theta[1]*((k)*((theta[0])**2-(theta[1])**2)-100))/(2*numpy.sqrt(k*(theta[1])**2-0.0025*((k)*((theta[0])**2 - (theta[1])**2)-100)**2))
    
    pass


# Function for Newton-Raphson Method
def NewtonRaphson(fnc, jacobian, guess, thresh, targ):
    """
    Determines the roots (or zeros) of a function by iteratively solving the equation 
    while varying the inputs until the result equals zero. More specifically, each 
    each iteration is solved using
    
    .. math::
        x_{n+1} = x_n - \\frac{f(x_n)}{\\frac{\\partial f}{\\partial x}}
        
    This approaches the x-intercept of the function with every iteration.
    
    .. image:: ../Images/NewtonRaphson.png
       :width: 5 in
       :align: center
       
    It is important to note that this method relies on a somewhat accurate initial 
    initial guess, otherwise the algorithm could converge on the wrong zero point.
    
    """
    pass


# Function that Runs the Newton-Raphson for the shape desired
def draw(i):
    """
    Runs the Newton-Raphson function for each of the X Y points in the desired drawing.
    
    :param i: Iterator to move through the list of X Y points.
    :return theta_calc: The resulting motor angles from the Newton-Raphson function.
    """
    pass

def move(draw, vals):
    """
    Groups a set of X Y points into a 'shape,' returning a set of points and a True/False 
    value representing pen-up or pen-down.
    
    :param draw: Indicates if the pen should be up or down for this shape.
    :type draw:  boolean
    
    :param vals: The .hpgl row that contains the points for the shape.
    :type vals: string
    
    :return: A list of the form [Pen up/down value, X values, Y values].
    :rtype:  list
    """
    x = []
    y = []
    
    vals = vals.strip('PUD').split(',')
    
    
    for h in range(len(vals)>>1):
        x.append(int(vals[2*h]))
        y.append(int(vals[2*h + 1]))
        
    shape = [draw, x, y]
    
    return shape