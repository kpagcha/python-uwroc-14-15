import turtle
import random

ANG = 20
RAND = 10
REL = 2/3
RANDT = 60
GROSORTRONCO = 2
TAMINIC = 150
TAMHOJA = 4
ANGHOJA = 180
PROF = 10

def hoja(t, a):
	turtle.begin_fill()
	turtle.right(a/2)
	turtle.circle(t, a)
	turtle.left(180-a)
	turtle.circle(t, a)
	turtle.left(180-a/2)
	turtle.end_fill()

def arbol(t, d):
	if d == 0:
		turtle.forward(t)
		hoja(TAMHOJA, ANGHOJA)
		turtle.penup()
		turtle.back(t)
		turtle.pendown()
		return
	else:
		angulo1 = ANG + random.randrange(-RAND, RAND+1)
		angulo2 = ANG + random.randrange(-RAND, RAND+1)
		tamano = t + t*random.randrange(-RANDT, RANDT+1)/100

		turtle.pensize(d+GROSORTRONCO)
		turtle.forward(tamano)
		turtle.left(angulo1)
		arbol(t*REL, d-1)
		turtle.right(angulo1 + angulo2)
		arbol(t*REL, d-1)
		turtle.left(angulo2)
		turtle.penup()
		turtle.back(tamano)
		turtle.pendown()

turtle.Screen().screensize(2000, 2000)
turtle.speed(0)
turtle.left(90)
arbol(120, 10)
turtle.done()