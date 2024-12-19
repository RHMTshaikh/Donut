import math
import os
import time
import sys

# Screen dimensions
screen_width, screen_height = os.get_terminal_size()

side = 33
side_length_x = side
side_length_y = side*2
side_length_z = side

half_side_length = [side_length_x//2, side_length_y//2, side_length_z//2]

object_distance = 80
screen_distance = 40

# light source
[lx, ly, lz] = [0.0, 1.0, -1.0]
magnitude = math.sqrt(sum(component ** 2 for component in [lx, ly, lz]))

# Avoid division by zero
if magnitude == 0:
    raise ValueError("Cannot normalize a zero vector")

# Normalize the vector
[lx, ly, lz] = [component / magnitude for component in [lx, ly, lz]]
print(lx, ly, lz)

def render_frame(A, B):
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)
    
    # Initialize output and zbuffer
    output = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]
    
    point = [0.0,0.0,0.0] # x, y, z
    
    for axis_num in range(3):
        fix = half_side_length[axis_num]
        dim_1 = half_side_length[(axis_num+1)%3]
        dim_2 = half_side_length[(axis_num+2)%3]
        
        for face in [1,-1]:
            # Calculate luminance
            normal = [0.0,0.0,0.0]
            normal[axis_num] = face
            [nx, ny, nz] = normal
            [nx, ny, nz] = [nx, ny*cosA - nz*sinA, ny*sinA + nz*cosA]
            [nx, ny, nz] = [nx*cosB - ny*sinB, nx*sinB + ny*cosB, nz]
            
            for i in range(-dim_1, dim_1):
                for j in range(-dim_2, dim_2):
                    
                    point[axis_num] = face*fix
                    point[(axis_num+1)%3] = i
                    point[(axis_num+2)%3] = j
                    
                    [x, y, z] = point
                    [x, y, z] = [x, y*cosA - z*sinA, y*sinA + z*cosA]
                    [x, y, z] = [x*cosB - y*sinB, x*sinB + y*cosB, z]
                    
                    z += object_distance
                    
                    ooz = 1 / z if z != 0 else sys.maxsize
                    
                    # 2D projection
                    xp = int(screen_width / 2 + screen_distance * x / z)
                    yp = int(screen_height / 2 - (screen_distance * y / z)//2) # Because each character has twice the height compared to with
                    
                    # Check if the surface is visible
                    if 0 <= xp < screen_width and 0 <= yp < screen_height and ooz > zbuffer[yp][xp]:
                        zbuffer[yp][xp] = ooz                        
                        L = lx*nx + ly*ny + lz*nz
                        luminance_index = int(L * 11)
                        luminance_index = max(0, min(11, luminance_index))  # Clamp to range 0-11
                        chars = ".,-~:;=!*#$@"
                        output[yp][xp] = chars[luminance_index]
        

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    for row in output:
        print(''.join(row))

def spinning_donut():
    A = 0 # Rotation around the x-axis
    B = 0 # Rotation around the z-axis
    while True:
        render_frame(A, B)
        A += 0.04
        B += 0.02
        time.sleep(0.03)  # Adjust speed

spinning_donut()
        