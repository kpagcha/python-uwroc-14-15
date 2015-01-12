import turtle

def arbol(tam, prof):
	if prof > 0:
		turtle.forward(tam)
		turtle.left(45)
		arbol(tam*2/3, prof-1)
		turtle.right(90)
		arbol(tam*2/3, prof-1)
		turtle.left(45)
		turtle.back(tam)

turtle.Screen().screensize(2000, 2000)
turtle.speed(0)
turtle.left(90)
arbol(120, 10)
turtle.done()