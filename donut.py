import math
import os
import time
import sys

# Screen dimensions
screen_width, screen_height = os.get_terminal_size()

# Torus parameters
theta_spacing = 0.07
phi_spacing = 0.02
R1 = 10
R2 = 30
object_distance = 50
screen_distance = 30

def render_frame(A, B):
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)
    
    # Initialize output and zbuffer
    output = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer = [[0 for _ in range(screen_width)] for _ in range(screen_height)]

    # Loop over theta and phi
    theta = 0
    while theta <= 2 * math.pi:
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        phi = 0
        while phi <= 2 * math.pi:
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            # Calculate the x, y coordinates of the circle before rotation
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D transformations
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = object_distance + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z if z != 0 else sys.maxsize  # Avoid division by zero

            # 2D projection
            xp = int(screen_width / 2 + screen_distance * x / z)
            yp = int(screen_height / 2 - (screen_distance * y / z)//2) # Because each character has twice the height compared to with

            # Calculate luminance
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            
            # Check if the surface is visible
            if 0 <= xp < screen_width and 0 <= yp < screen_height:
                if ooz > zbuffer[yp][xp]:
                    zbuffer[yp][xp] = ooz
                    luminance_index = int(L * 8)
                    luminance_index = max(0, min(11, luminance_index))  # Clamp to range 0-11
                    chars = ".,-~:;=!*#$@"
                    output[yp][xp] = chars[luminance_index]

            phi += phi_spacing
        theta += theta_spacing

    # Print output to the screen
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    for row in output:
        print(''.join(row))

def spinning_donut():
    A = 0
    B = 0
    while True:
        render_frame(A, B)
        A += 0.04
        B += 0.02
        time.sleep(0.03)  # Adjust speed

spinning_donut()