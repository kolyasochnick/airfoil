from visualizer import AirfoilVisualizer
from calculatuion import four_digit_airfoil_calculation

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
            return four_digit_airfoil_calculation(self.camber, 
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
    
        
airfoil = Airfoil()

visualizer = AirfoilVisualizer(airfoil)
visualizer.show_with_sliders()