import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import colorsys
import math
import time

pygame.init()
display = (1920, 1080)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
gluPerspective(60, display[0] / display[1], 0.1, 1000)
glTranslatef(0, 0, -140)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

N = 16000
t = np.linspace(0, 120 * np.pi, N)

observer_theta = 0.0
observer_phi = 0.0
observer_bias = 0.0

phase = 0.0
speed = 0.008

points = []

def field(phi, time_shift):
    return (
        np.sin(2.0 * phi + time_shift)
        + np.cos(3.1 * phi - time_shift * 0.7)
        + np.sin(0.9 * phi + np.cos(time_shift))
    )

def decode():
    points.clear()
    global phase
    phase += speed

    psi = field(t + observer_theta, phase)
    chi = field(t + observer_phi, -phase * 0.6)

    for i in range(N):
        r = 30 + 14 * psi[i]
        x = r * math.cos(t[i] + observer_theta + observer_bias)
        y = r * math.sin(t[i] + observer_phi)
        z = chi[i] * 50
        points.append((x, y, z, i / N))

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_POINTS)
    for x, y, z, h in points:
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        glColor4f(r, g, b, 0.85)
        glVertex3f(x, y, z)
    glEnd()
    pygame.display.flip()

clock = pygame.time.Clock()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            quit()
        if event.type == MOUSEMOTION:
            mx, my = event.rel
            observer_theta += mx * 0.0015
            observer_phi += my * 0.0015
            observer_bias += mx * 0.0003

    decode()
    draw()
    clock.tick(60)
