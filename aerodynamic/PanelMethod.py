import numpy as np
from typing import List, Tuple
from airfoil import Airfoil

# (x1, y1) (x2, y2)
# array((x2-x1)/2, (y2-y1)/2)

import matplotlib.pyplot as plt

def create_normals_of_panels(points, surface=1):
    
    points_of_normals = []
    px, py = points[0]
    for x,y in points[1:]:
        
        xc = (x + px)/2
        yc = (y + py)/2
        
        dx = (x - px) 
        dy = (y - py) 
        
        length = (dx**2 + dy**2)**0.5
        
        # Одинаковая длина вектора для всех панелей
        # tx = dx / length
        # ty = dy / length

        # nx = -surface * ty
        # ny = surface * tx
        
        # Длина вектора относительно длины панели
        nx = -surface * dy
        ny = surface * dx
        
        points_of_normals.append(((px, py, x, y),(xc, yc, nx, ny)))
        
        px = x
        py = y
    
    return points_of_normals
        
        
airfoil = Airfoil()
upper_points, lower_points, _= airfoil.calculate(N=30)

for points, normals in create_normals_of_panels(upper_points): 
    px, py, x, y = points
    xc, yc, nx, ny = normals
    plt.plot([px, x], [py, y])
    plt.quiver(xc, yc, nx, ny, angles='xy', scale_units='xy', scale=1)

for points, normals in create_normals_of_panels(lower_points, surface=-1): 
    px, py, x, y = points
    xc, yc, nx, ny = normals
    plt.plot([px, x], [py, y])
    plt.quiver(xc, yc, nx, ny, angles='xy', scale_units='xy', scale=1)
    

plt.xlim(-1, 3)
plt.ylim(-1, 3)
plt.axis('equal')
plt.grid()
plt.show()