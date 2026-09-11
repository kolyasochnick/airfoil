from math import cos, pi, atan, sin

        
    
def four_digit_airfoil_calculation(camber, Xcamber, thickness, a, b, c, d, e, N):
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
    

def five_digit_airfoil_calculation():
    pass



if __name__ == '__main__':
    print('Running calculation.py')
    
    
    
