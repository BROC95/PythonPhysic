#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 22:16:30 2020

@author: breyneroc
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 21:25:09 2020

@author: breyneroc
"""

# OJO DE BREYNER
import turtle
#import Tkinter
from random import randint

def color_random():
    """Generates an R,G,B values randomly in range
    0 to 255 """
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return r, g,b

global num
num=4
MAX_DEPTH = 4
# 6 ojo

# Con num 4  da 90

# 90 Crea la ilusion de un ojo
def angulo(n):
    div=(n-2)*180
    theta=div/n
    return theta
def poli(theta,profundidad=0):
    if profundidad > MAX_DEPTH:
        #print(profundidad)
        
        return
    # Tamaño
    longitud = 50 * (2/3)**profundidad
    turtle.speed(10)
    # Cubo de 8 lados  se toman 4 con espacio
    for i in range(num*2):
        turtle.color(color_random())
        turtle.forward(longitud)
        turtle.right(theta)
        turtle.penup()
        turtle.forward(longitud)
        turtle.pendown()
        
        
    # Corre hacia arriba
    turtle.forward(longitud)
    turtle.right(theta*2)
    # Primera llamada recursiva, 
    
    poli(theta,profundidad+1)

    # se deja en la esquina sup derecha
    # 
    turtle.right(theta*2)

    # ¡Dos llamadas recursivas en la mimsa función! 
    poli(theta,profundidad+1)

    turtle.right(theta*2) # se invierte
    turtle.forward(longitud) # queda en el segmento interno
    turtle.left(180) # damos media vuelta


#turtle.home()
turtle.title("Fractal color")
turtle.setup(500,500)

turtle.bgcolor('black') # Set the background colour of thescreen
turtle.colormode(255) # Indicates RGB numbers will be in therange 0 to 255

turtle.hideturtle()


theta=angulo(num)
print(theta)
print(num)
turtle.setposition(0,0)
poli(theta) # Hay que llamar a nuestra función, si no no pasa nada
turtle.penup()
# posicionno giro y completo el ojo
turtle.setposition(0,0)
turtle.right(180)
poli(theta)


#ts=turtle.getsscreen()
#ts.getcanvas().postcript(file="OJOfractal.eps")
print('Done')
turtle.done()
#turtle.exitonclick()
