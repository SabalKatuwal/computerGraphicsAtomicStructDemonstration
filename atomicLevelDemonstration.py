import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

#Red = Proton +
#Green = Electron -
#blue = Neutron

def initialize(width, height):
    # Initialize pygame and set the display mode
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    # Set the viewport and perspective projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, width / height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)  # Enable depth buffering

def drawSolidSphere(radius, slices, stacks, ambient_color, diffuse_color, specular_color, shininess):
    # Enable lighting and set material properties
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_color)
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess)

    # Draw a solid sphere using triangle strips
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + (i - 1) / stacks)
        z0 = math.sin(lat0)
        zr0 = math.cos(lat0)

        lat1 = math.pi * (-0.5 + i / stacks)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)

        glBegin(GL_TRIANGLE_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * (j - 1) / slices
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(radius * x * zr0, radius * y * zr0, radius * z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(radius * x * zr1, radius * y * zr1, radius * z1)

        glEnd()

    # Disable lighting
    glDisable(GL_LIGHT0)
    glDisable(GL_LIGHTING)

#draw the entire scene
def drawScene(proton_radius, proton_slices, proton_stacks,
              neutron_radius, neutron_slices, neutron_stacks,
              electron_radius, electron_slices, electron_stacks,
              electron_distance, electron_speed,
              rotation_x, rotation_y):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(0, 0, -15, 0, 0, 0, 0, 1, 0)

    # Apply rotation to the entire scene
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    # Draw Proton(red sphere)
    proton_position = [
        (0.5, 0, 0),  # Right
        (-0.5, 0, 0),  # Left
    ]
    for position in proton_position:
        glPushMatrix()
        glTranslatef(*position)
        drawSolidSphere(proton_radius, proton_slices, proton_stacks, [0.2, 0.0, 0.0, 1.0], [0.8, 0.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0], 32.0)
        glPopMatrix()

    # Draw Neutron (blue sphere)
    neutron_position = [
        (0, 0.5, 0),  
        (0, -0.5, 0) 
    ]
    for position in neutron_position:
        glPushMatrix()
        glTranslatef(*position)
        drawSolidSphere(neutron_radius, neutron_slices, neutron_stacks, [0.0, 0.0, 0.2, 1.0], [0.0, 0.0, 0.8, 1.0], [1.0, 1.0, 1.0, 1.0], 32.0)
        glPopMatrix()

    # First white orbit
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glBegin(GL_LINE_LOOP)
    for angle in range(361):
        angle_rad = math.radians(angle)
        path_x = electron_distance * math.cos(angle_rad)
        path_y = electron_distance * math.sin(angle_rad)
        path_z = 0.0
        glVertex3f(path_x, path_y, path_z)
    glEnd()
    glPopMatrix()

    # Second white orbit
    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glBegin(GL_LINE_LOOP)
    for angle in range(361):
        angle_rad = math.radians(angle)
        path_x = electron_distance * math.cos(angle_rad)
        path_y = 0.0
        path_z = electron_distance * math.sin(angle_rad)
        glVertex3f(path_x, path_y, path_z)
    glEnd()
    glPopMatrix()

    # First Electron
    electron1_angle = pygame.time.get_ticks() / 1000.0 * electron_speed
    electron1_x = electron_distance * math.cos(electron1_angle)
    electron1_y = electron_distance * math.sin(electron1_angle)
    electron1_z = 0.0

    glPushMatrix()
    glTranslatef(electron1_x, electron1_y, electron1_z)
    drawSolidSphere(electron_radius, electron_slices, electron_stacks, [0.0, 0.2, 0.0, 1.0], [0.0, 0.8, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0], 32.0)
    glPopMatrix()

    # Second Electron
    electron2_angle = pygame.time.get_ticks() / 1000.0 * (electron_speed+0.67)
    electron2_x = electron_distance * math.cos(electron2_angle)
    electron2_y = 0.0
    electron2_z = electron_distance * math.sin(electron2_angle)

    glPushMatrix()
    glTranslatef(electron2_x, electron2_y, electron2_z)
    drawSolidSphere(electron_radius, electron_slices, electron_stacks, [0.0, 0.2, 0.0, 1.0], [0.0, 0.8, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0], 32.0)
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)


'''
Main function to run overall program:
The main function sets up the initial settings, creates the particles, and enters an infinite loop where the scene is continuously updated and rendered. 
The rotation of the particles and the camera position can be controlled by modifying the variables `rotation_x` and `rotation_y`.
'''
def main():
    width = 800
    height = 600

    initialize(width, height)

    proton_radius = 0.5
    proton_slices = 50
    proton_stacks = 50

    neutron_radius = 0.5
    neutron_slices = 30
    neutron_stacks = 30

    electron_radius = 0.3
    electron_slices = 20
    electron_stacks = 20
    electron_distance = 3.0
    electron_speed = 4.0

    rotation_x = 0
    rotation_y = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        rotation_x += 1
        rotation_y += 1

        drawScene(proton_radius, proton_slices, proton_stacks,
                  neutron_radius, neutron_slices, neutron_stacks,
                  electron_radius, electron_slices, electron_stacks,
                  electron_distance, electron_speed,
                  rotation_x, rotation_y)

        clock.tick(60)

if __name__ == "__main__":
    main()
