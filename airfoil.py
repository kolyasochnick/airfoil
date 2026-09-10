from math import cos, pi, atan, sin
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from visualizer import AirfoilVisualizer

class Airfoil:
    def __init__(self, camber=0.04, Xcamber=0.4, thickness=0.15, a=0.29690, b=0.126, c=0.3516, d=0.2843, e=0.10150):
        
        self.camber: float = camber # camber - выпуклость 0 : 0.1
        self.Xcamber: float = Xcamber # Xcamber - координата с максимальным Y для кривой выпуклости 0:1
        self.thickness: float = thickness # thickness - толщина 0:1
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
    
    def calculate(self):
            return self.four_digit_airfoil_calculate(self.camber, 
                               self.Xcamber, 
                               self.thickness, 
                               self.a,
                               self.b,
                               self.c, 
                               self.d,
                               self.e,
                               N=100)
    
    def safe(self, event):
        name = 'NACA' + str(int(self.camber * 100)) + str(int(self.Xcamber * 10)) + str(int(self.thickness* 100))
        path = f'airfoils_nums/{name}.txt'
        
        upper, lower, _ = self.calculate()
        
        with open(path, 'w', encoding='utf-8') as f:
            for point in upper:
                f.write(f'{point[0]} {point[1]}\n')

            for point in lower:
                f.write(f'{point[0]} {point[1]}\n')
        print(f'Точки данного профиля сохранены по {path}')
        
        
    def four_digit_airfoil_calculate(self, camber, Xcamber, thickness, a=0.29690, b=0.126, c=0.3516, d=0.2843, e=0.10150, N=100):
        upper_surface_points = [] 
        lower_surface_points = []
        mean_line = []
        for i in range(1, N + 1):
            angle_of_sector = pi / (2 * (N - 1))
            current_Xpoint = 1 - cos((i - 1) * angle_of_sector)
    
            thickness_value = 5 * thickness * (a * current_Xpoint ** 0.5 -
                                                             b * current_Xpoint -
                                                             c * current_Xpoint ** 2 + 
                                                             d * current_Xpoint ** 3 - 
                                                             e * current_Xpoint ** 4)
            
    
            if current_Xpoint > Xcamber:
                Y_of_mean_line =  camber * ((1 - 2 * Xcamber) + 2 * Xcamber * current_Xpoint - current_Xpoint ** 2)/ (1 - Xcamber) ** 2 
                slope_mean_line = 2 * camber * (Xcamber - current_Xpoint) / (1 - Xcamber) ** 2
    
            else: 
                Y_of_mean_line =  camber * ((2 * Xcamber - current_Xpoint) * current_Xpoint)/ Xcamber ** 2 
                slope_mean_line = 2 * camber / Xcamber * (1 - (current_Xpoint / Xcamber))
    
            ordinate_rotation_angle = atan(slope_mean_line)
    
            upper_surface_X = current_Xpoint - thickness_value * sin(ordinate_rotation_angle)                
            upper_surface_Y = Y_of_mean_line +  thickness_value * cos(ordinate_rotation_angle)
        
            lower_surface_X = current_Xpoint + thickness_value * sin(ordinate_rotation_angle)
            lower_surface_Y = Y_of_mean_line - thickness_value * cos(ordinate_rotation_angle)
    
            upper_surface_points.append((round(upper_surface_X, 4), round(upper_surface_Y, 4)))
            lower_surface_points.append((round(lower_surface_X, 4), round(lower_surface_Y, 4)))
            
            mean_line.append((current_Xpoint, Y_of_mean_line))
                
        return upper_surface_points, lower_surface_points, mean_line
    
        
airfoil = Airfoil()

visualizer = AirfoilVisualizer(airfoil)
visualizer.show_with_sliders()