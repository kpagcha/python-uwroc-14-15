import turtle

window = turtle.Screen()
window.screensize(2000, 1500)

def squares(n, gap, step):
	if step > 0:
		for i in range(0, 4):
			turtle.left(90)
			turtle.forward(n)
		turtle.penup()
		turtle.forward(gap)
		turtle.right(90)
		turtle.forward(gap)
		turtle.left(90)
		turtle.pendown()
		squares(n+gap*2, gap*1.20, step-1)

turtle.speed(0)
squares(20, 5, 10)
window.exitonclick()