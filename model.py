import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from scipy.signal import fftconvolve
import colorsys

N = 120
alpha = 0.04
beta = 0.02
gamma = 0.02
delta = 0.01
sigma = 6.0
omega = 0.2
eta = 1.5
hover_radius = 6.0

x = np.linspace(-1, 1, N)
y = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, y)

A = np.ones((N, N))
phi = np.random.uniform(0, 2 * np.pi, (N, N))
psi = A * np.exp(1j * phi)

R = np.sqrt(X**2 + Y**2)
kernel = np.exp(-(R**2)/(2*sigma**2)) * np.exp(1j * omega * R)

def laplacian(Z):
    return (
        np.roll(Z, 1, 0)
        + np.roll(Z, -1, 0)
        + np.roll(Z, 1, 1)
        + np.roll(Z, -1, 1)
        - 4 * Z
    )

pygame.init()
display = (1920, 1080)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
gluPerspective(45, display[0]/display[1], 0.1, 100.0)
glTranslatef(0, 0, -3)
glEnable(GL_DEPTH_TEST)
glPointSize(2)

mouse_x = None
mouse_y = None

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        if event.type == MOUSEMOTION:
            mx, my = event.pos
            mouse_x = int(mx / display[0] * N)
            mouse_y = int(my / display[1] * N)

    phi = phi + alpha * laplacian(phi) + beta * np.sin(phi)
    A = A + gamma * laplacian(A) - delta * (A - 1)

    if mouse_x is not None and mouse_y is not None:
        dx = np.arange(N)[:, None] - mouse_y
        dy = np.arange(N)[None, :] - mouse_x
        D = np.sqrt(dx*dx + dy*dy)
        phi += eta * np.exp(-(D**2)/(2*hover_radius**2))

    psi = A * np.exp(1j * phi)
    holo = fftconvolve(psi, kernel, mode="same")
    I = np.abs(holo)
    I /= I.max()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_POINTS)

    for i in range(N):
        for j in range(N):
            h = (phi[i, j] % (2*np.pi)) / (2*np.pi)
            r, g, b = colorsys.hsv_to_rgb(h, 1, I[i, j])
            glColor3f(r, g, b)
            glVertex3f(X[i, j], Y[i, j], I[i, j] * 0.8)

    glEnd()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
