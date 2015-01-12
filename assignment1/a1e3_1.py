import turtle
import random
import copy

window = turtle.Screen()
window.screensize(2000, 1500)

turtle.left(90)
def tree(distance, steps):
	if steps > 0:
		turtle.forward(distance)
		left_branch_angle = random.randint(-10, 10) + 35
		turtle.left(left_branch_angle)
		tree(distance * 0.75, steps - 1)
		right_branch_angle = left_branch_angle + random.randint(-10, 10) + 35
		turtle.right(right_branch_angle)
		tree(distance * 0.75, steps - 1)
		turtle.left(right_branch_angle - left_branch_angle)
		turtle.backward(distance)

turtle.speed(0)
tree(100, 10)
window.exitonclick()
