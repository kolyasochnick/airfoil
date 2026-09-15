import numpy as np


def create_panels(points):
    panels = []
    control_points = []

    for p1, p2 in zip(points[:-1], points[1:]):
        x1, y1 = p1
        x2, y2 = p2

        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy)
        theta = np.arctan2(dy, dx)

        panels.append([x1, y1, x2, y2, length, theta])
        control_points.append([(x1 + x2) / 2, (y1 + y2) / 2])

    return np.array(panels), np.array(control_points)

        
def inf_coefficient(panels, control_points):
    m = len(panels)
    normal_matrix = np.zeros((m, m + 1))
    tang_matrix = np.zeros((m, m + 1))

    for i in range(m):
        xi, yi = control_points[i]
        theta_i = panels[i, 5]

        for j in range(m):
            
            if i == j:
                Cn1, Cn2 = -1.0, 1.0
                Ct1, Ct2 = 0.5 * np.pi, 0.5 * np.pi
            else:
                Xj, Yj, _, _, Sj, theta_j = panels[j]
                dx, dy = xi - Xj, yi - Yj

                A = -dx * np.cos(theta_j) - dy * np.sin(theta_j)
                B = dx**2 + dy**2
                C = np.sin(theta_i - theta_j)
                D = np.cos(theta_i - theta_j)
                E = dx * np.sin(theta_j) - dy * np.cos(theta_j)

                F = np.log(1 + (Sj**2 + 2 * A * Sj) / B)
                G = np.arctan2(E * Sj,B + A * Sj)
                
                Q = (dx * np.cos(theta_i - 2 * theta_j) - dy * np.sin(theta_i - 2 * theta_j))
                P = (dx * np.sin(theta_i - 2 * theta_j) + dy * np.cos(theta_i - 2 * theta_j))

                Cn2 = D + 0.5 * Q * F / Sj - (A * C + D * E) * G / Sj
                Cn1 = 0.5 * D * F + C * G - Cn2
                
                Ct2 = C + 0.5 * P * F / Sj + (A * D - C * E) * G / Sj
                Ct1 = 0.5 * C * F - D * G -  Ct2

            normal_matrix[i, j] += Cn1
            normal_matrix[i, j + 1] += Cn2
                
            tang_matrix[i, j] += Ct1
            tang_matrix[i, j + 1] += Ct2
                
    return normal_matrix, tang_matrix
            

def solve_gamma(normal_matrix, panels, alpha):
    m = len(panels)

    matrix = np.zeros((m + 1, m + 1))
    matrix[:m] = normal_matrix
    matrix[m, 0] = 1
    matrix[m, -1] = 1

    rhs = np.zeros(m + 1)
    rhs[:m] = np.sin(panels[:, 5] - alpha)
    
    return np.linalg.solve(matrix, rhs)


def solve_velocity(tang_matrix,panels, alpha, gamma):
    m = len(panels)
    
    velocity = np.zeros(m)
    velocity = np.cos(panels[:, 5] - alpha) + tang_matrix @ gamma
    
    return velocity


def solve_pressure_coefficient(velocity):
    pressure_coef = 1 - velocity ** 2
    
    return pressure_coef
    

    
def solve_panel_method(airfoil, alpha: int):

    alpha = 10 * np.pi / 180

    upper_points, lower_points, _ = airfoil.calculate(N=100)

    points = ([lower_points[-1]] + lower_points[-2::-1] + upper_points[1:])

    panels, control_points = create_panels(points)
    normal_matrix, tang_matrix = inf_coefficient(panels, control_points)

    gamma = solve_gamma(normal_matrix, panels, alpha)
    velocity = solve_velocity(tang_matrix, panels, alpha, gamma)
    Cp = solve_pressure_coefficient(velocity)

    return Cp