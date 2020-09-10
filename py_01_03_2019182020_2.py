import turtle
a=0
b=0
turtle.speed(0)
def move(x1,y1,x2,y2):
    turtle.penup()
    turtle.goto(x1,y1)
    turtle.pendown()
    turtle.goto(x2,y2)

while (a<=5):
    move((a*100)-300,200,(a*100)-300,-300)
    a=a+1

while (b<=5):
    move(-300,(b*100)-300,200,(b*100)-300)
    b=b+1

turtle.exitonclick()
