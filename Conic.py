
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np

class Conic :
    _x_initial, _y_initial = 0, 0
    def __init__ (self, a, b=None, h=0, k=0):
        """
        Define a Conic section
        a = Cemi-major axis
        b = Cemi-minor axis, if not provided, b will be equal to a (circle)
        h = x co-ordinate of the center
        k = y co-ordinate of the center
        """
        if b==None:
            b=a
        self.cemimajor_axis = a
        self.cemiminor_axis = b
        self._x_center, self._y_center = h, k
        self.center = (self._x_center, self._y_center)
        
    def translate(self, shift=(0,0)):                 # Shifts the midpoint of conic.
        self._x_center = self._x_center + shift[0]    
        self._y_center = self._y_center + shift[1]
        self.center = (self._x_center, self._y_center)
     
    def rotate(self, angle=0):                    # Rotation remaining center point fixed.
        if angle!=0:                              # reset to zero, if previously rotated.
            self._x = self._x_initial
            self._y = self._y_initial
        self.angle = angle                        # In degrees.
        theta = np.deg2rad(self.angle)            # Converting into radians.
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta),  np.cos(theta)]])
        R_11, R_12 = rotation_matrix[0][0], rotation_matrix[0][1]
        R_21, R_22 = rotation_matrix[1][0], rotation_matrix[1][1]
        self._x = self._x_initial*R_11 + self._y_initial*R_12   # x-coordinates of locus after rotating.
        self._y = self._x_initial*R_21 + self._y_initial*R_22   # y-coordinates of locus after rotating.
        
    def draw(self, c='b', zoom=100, midpoint=True):
        """Drawing the conic section"""
        fig_size = list(map(lambda x:x*zoom/100, plt.rcParams.get('figure.figsize')))
        try:                      # If it is transformed.
            x_points = self._x + self._x_center
            y_points = self._y + self._y_center
        except AttributeError:    # If it is NOT transformed.
            x_points = self._x_initial + self._x_center
            y_points = self._y_initial + self._y_center
        
        fig1 = plt.figure(1, figsize=fig_size)
        plt.plot(x_points,y_points,c)
        if midpoint==True:         # To plot the Middle point.
            plt.plot(self._x_center, self._y_center, marker='o', markersize=5)
        plt.grid() 
        plt.axis("scaled")

class Ellipse(Conic):
    def __init__ (self, a, b=None, h=0, k=0):
        super().__init__ (a, b, h, k)
        self.edges = int((2*(self.cemimajor_axis + self.cemiminor_axis) + 50))
        t = 2*np.pi*(np.linspace(0,1,self.edges))
        self._x_initial = self.cemimajor_axis*(np.cos(t))
        self._y_initial = self.cemiminor_axis*(np.sin(t))

class Circle(Conic):
    def __init__ (self, r, h=0, k=0):
        super().__init__ (0,0, h, k)
        delattr(self, 'cemimajor_axis')
        delattr(self, 'cemiminor_axis')
        self.radius = r
        self.edges = int((4*(self.radius) + 50))
        t = 2*np.pi*(np.linspace(0,1,self.edges))
        self._x_initial = self.radius*(np.cos(t))
        self._y_initial = self.radius*(np.sin(t))
        
class Hyperbola(Conic):
    def __init__ (self, a, b=None, h=0, k=0):
        super().__init__ (a, b, h, k)
        self.edges = int((4*(self.cemimajor_axis + self.cemiminor_axis) + 100))
        t = 2*np.pi*(np.linspace(0,1,self.edges))
        self._x_initial = self.cemimajor_axis*(1/np.cos(t))
        self._y_initial = self.cemiminor_axis*(np.tan(t))
        
    def draw(self, c='b'):
        super().draw(c, midpoint=False)
        plt.xlim((self._x_center-10*self.cemimajor_axis), (self._x_center+10*self.cemimajor_axis))
        plt.ylim((self._y_center-10*self.cemiminor_axis), (self._y_center+10*self.cemiminor_axis))
        
class Parabola(Conic):
    def __init__ (self, p, h=0, k=0):
        super().__init__ (None, None, h, k)
        delattr(self, 'cemimajor_axis')
        delattr(self, 'cemiminor_axis')
        self.vertex = (h, k)
        self.rate = p
        self.edges = 300 #int((4*(self.cemimajor_axis + self.cemiminor_axis) + 100))
        t_rev = np.linspace(10,0,self.edges)
        x_upper = p*np.square(t_rev)
        y_upper = 2*p*t_rev
        x_lower = (p*np.square(t_rev[::-1]))
        y_lower = -2*p*t_rev[::-1]
        self._x_initial = np.concatenate([x_upper,x_lower])
        self._y_initial = np.concatenate([y_upper,y_lower])

