# Web VPython 3.2
# Double pendulum

# The analysis is in terms of Lagrangian mechanics.
# The Lagrangian variables are angle of upper bar, angle of lower bar,
# measured from the vertical.

# Bruce Sherwood

'''




thetadot1 = (6/(L1**2))*(2*p1 - 3*(L1/L2)*cos(theta1-theta2)*p2)/(4*(M1+3*M2) - 9*M2*(cos(theta1-theta2))**2)
thetadot2 = (6/(M2*L2**2))*(2*p2*(M1+3*M2) - 3*M2*(L2/L1)*cos(theta1-theta2)*p1)/(4*(M1+3*M2) - 9*M2*(cos(theta1-theta2)**2))


'''
from vpython import box, text, vector, color, rate
from vpython import *
import numpy as np
import random
import sys

scene.width = 640
scene.height = 600
scene.range = 1.5
scene.title = """Apilamiento de Cajas con un Brazo
Robótico de Dos Articulaciones
"""


d = 0.05  # thickness of each bar
gap = 2*d  # distance between two parts of upper, U-shaped assembly
L1 = 1  # physical length of upper assembly; distance between axles

L1display = L1+d  # show upper assembly a bit longer than physical, to overlap axle
L2 = 0.5  # physical length of lower bar

L2display = L2+d/2  # show lower bar a bit longer than physical, to overlap axle

# hpedestal = 1.1*(L1+L2)  # height of pedestal
hpedestal = 1  # height of pedestal
wpedestal = 0.1  # width of pedestal
tbase = 0.05  # thickness of base
wbase = 8*gap  # width of base
offset = 2*gap  # from center of pedestal to center of U-shaped upper assembly
# top of inner bar of U-shaped upper assembly
pedestal_top = vec(0, hpedestal/2, 0)
pedestal_top = vec(0, 0, 0)

# theta1 = 1.3*pi/2  # initial upper angle (from vertical)
theta1 = 0  # initial upper angle (from vertical)
theta2 = theta1  # initial lower angle (from vertical)


axle1 = cylinder(pos=pedestal_top-vec(0, 0, gap/2-d/4), axis=vec(0, 0, -1),
                 size=vec(offset, d/4, d/4), color=color.yellow)

bar1 = box(pos=pedestal_top+vec(L1display/2-d/2, 0, -(gap+d)/2),
           size=vec(L1display, d, d), color=color.red)

bar1.rotate(angle=theta1, axis=vec(0, 0, 1), origin=vec(
    axle1.pos.x, axle1.pos.y, bar1.pos.z))

bar1b = box(pos=pedestal_top+vec(L1display/2-d/2, 0, (gap+d)/2),
            size=vec(L1display, d, d), color=bar1.color)

bar1b.rotate(angle=theta1, axis=vec(0, 0, 1), origin=vec(
    axle1.pos.x, axle1.pos.y, bar1b.pos.z))

pivot1 = vec(axle1.pos.x, axle1.pos.y, 0)

axle2 = cylinder(pos=pedestal_top+vec(L1, 0, -(gap+d)/2), axis=vec(0, 0, 1),
                 size=vec(gap+d, axle1.size.y/2, axle1.size.y/2), color=axle1.color)

axle2.rotate(angle=theta1, axis=vec(0, 0, 1), origin=vec(
    axle1.pos.x, axle1.pos.y, axle2.pos.z))


bar2 = box(pos=axle2.pos+vec(L2/2, 0, (gap+d)/2),
           size=vec(L2display, d, d), color=color.green)

bar2.rotate(angle=theta2,  axis=vec(0, 0, 1),
            origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))

axle3 = cylinder(pos=pedestal_top+vec(L2+L1, 0, -(gap+d)/2), axis=vec(0, 0, 1),
                 size=vec(gap+d, axle2.size.y, axle2.size.y), color=axle1.color)

axle3.rotate(angle=theta2, axis=vec(0, 0, 1), origin=vec(
    axle2.pos.x, axle2.pos.y, axle3.pos.z))

graph(scroll=True, xmin=0, xmax=5)
energy = gcurve(color=color.black, label="E<sub>total</sub>", interval=1000)
ktrans = gcurve(color=color.red, label="K<sub>trans</sub>", interval=1000)
krot = gcurve(color=0.7*color.green, label="K<sub>rot</sub>", interval=1000)
PE = gcurve(color=color.blue, label="E<sub>potential</sub>", interval=1000)

y1 = bar1.pos.y
y2 = bar2.pos.y

run = False


def caja(x, y):
    s = 0.1
    return box(pos=pedestal_top+vec(x, y, 0),
               size=vec(s, s, s), color=color.cyan)


def objetivo(x, y):
    s = 0.3
    box(pos=pedestal_top+vec(x, y, 0),
        size=vec(s, 0.01, s), color=color.yellow)


def cinematica_inversa(x, y):
    argu = (x**2+y**2-L1**2-L2**2)/(2*L1*L2)
    thet2 = np.arccos(argu)
    argu2 = L2*np.sin(thet2)/(L1+L2*np.cos(thet2))
    thet1 = np.arctan(y/x)-np.arctan(argu2)

    # print(thet1,thet2)

    return thet1, thet2


x, y = 0.5, 1.2
xo, yo = 1, -1
S = L1+L2
cajas = []
coord = []
rand_init = random.SystemRandom()

def create_cajas(n):
    for i in range(n):
        x, y = rand_init.uniform(0.1, S), rand_init.uniform(0.1, S)
        if x > 0:
            # print("mag", np.linalg.norm(np.array([x, y])))
            norC = np.linalg.norm(np.array([x, y]))
            norO = np.linalg.norm(np.array([xo, yo]))
            if norC <= S:
                if norO <= S:
                    caj = caja(x, y)
                    objetivo(xo, yo)
                    cajas.append(caj)
                    coord.append((x, y))
                    

                else:
                    print("Error Obj debe ser Mag < ", L1+L2)
                    T = text(text=f"Error : magObj < {L1+L2}",
                            align='center', color=color.green)
                    # x, y = 0.1, -1
                    # caja(x, y)
                    i = 0
                    # sys.exit(0)
                    # scene.delete()
                    # create_cajas(n)
                    return False

            else:
                print("Error debe ser Mag < ", L1+L2)

                T = text(text=f"Error : mag < {L1+L2}",
                        align='center', color=color.green)
                # x, y = 0.1, 1
                # caja(x, y)
                i = 0
                # sys.exit(0)
                # scene.delete()
                # create_cajas(n)
                return False

        else:
            print("Error debe ser x > 0")
            T = text(text="Error : x > 0",
                    align='center', color=color.green)
            # x, y = 1, 1
            # caja(x, y)
            i = 0
            # sys.exit(0)
            # scene.delete()
            # create_cajas(n)
            return False
    else:
        return True

if create_cajas(3):
    print(True)
else:
    create_cajas(3)

def pause(b):
    global run
    run = not run
    if run:
        b.text = 'Objetivo'
    else:
        b.text = 'Caja'


button(text='Caja', bind=pause)

graphing = False
tstart = 0


def graphit(b):
    global graphing, tstart, instructions
    graphing = not graphing
    if graphing:
        create_cajas(4)
        
        b.text = 'Pause Graph'
        instructions = wtext(text=f"""{angles}""")
      
    else:
        b.text = 'Graph Energy'


def anglesT(angles):
    instructions = wtext(text=f"""{angles}""")

# button(text='Graph Energy', bind=graphit)

instructions = wtext(text="""
Apilamiento de Cajas con un Brazo
Robótico de Dos Articulaciones
In Web VPython programs:
To rotate "camera", drag with right button or Ctrl-drag.
To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
  On a two-button mouse, middle is left + right.
To pan left/right and up/down, Shift-drag.
Touch screen: pinch/extend to zoom, swipe or two-finger rotate.
""")
#                      Intro
# Este proyecto se enfoca en programar un brazo rob´otico de dos articulaciones para recoger tres cajas
# desde ubicaciones dadas y apilarlas en una ubicaci´on objetivo, utilizando el concepto de cinem´atica
# inversa, resuelta mediante geometría.                    
                    #  """)

dt = 1
t = 0


def mov_bar1(theta1):
    bar1.rotate(angle=theta1, axis=vec(0, 0, 1),
                origin=vec(axle1.pos.x, axle1.pos.y, bar1.pos.z))
    bar1b.axis = bar1.axis
    bar1b.pos = bar1.pos+vec(0, 0, bar1b.pos.z-bar1.pos.z)
    axle2.pos = pivot1 - vec(0, 0, (gap+d)/2) + L1*hat(bar1.axis)
    pivot2 = vec(axle2.pos.x, axle2.pos.y, 0)
    bar2.pos = pivot2 + 0.5*L2*hat(bar2.axis)
    bar2.rotate(angle=theta1,  axis=vec(0, 0, 1),
                origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))
    axle3.pos = pivot2 - vec(0, 0, (gap+d)/2) + L2*hat(bar2.axis)
    if goal:
        pivot3 = vec(axle3.pos.x, axle3.pos.y, 0)
        caj.pos = pivot3


goal = False

angles = []
anglesO = []

# print(cajas)
i = 0
while True:
    # rate(1/dt)
    rate(1)

    if i == len(cajas):
        sleep(2)
        T = text(text="Terminado",
                 align='center', color=color.green)
        # scene.delete()
        instructions = wtext(text=[f"Elemento {x}\n" for x in angles])
    try:
        caj = cajas[i]
        x, y = coord[i]
    except:
        i = 0
    if not run:
        continue
    if not goal:
        theta1, theta2 = cinematica_inversa(x, y)
        angles.append((theta1, theta2))
    else:
        theta1, theta2 = cinematica_inversa(xo, yo)
        anglesO.append((theta1, theta2))

    pos1 = vec(bar1.pos)  # keep copies of where we were
    pos2 = vec(bar2.pos)
    mov_bar1(theta1=theta1)

    sleep(1)

    if True and goal == False:
        bar2.rotate(angle=theta2,  axis=vec(0, 0, 1),
                    origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))
        axle3.rotate(angle=theta2,  axis=vec(0, 0, 1),
                     origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))

        sleep(1)

        

        bar2.rotate(angle=-theta2, axis=vec(0, 0, 1),
                    origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))
        axle3.rotate(angle=-theta2,  axis=vec(0, 0, 1),
                     origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))
        pivot3 = vec(axle3.pos.x, axle3.pos.y, 0)
        caj.pos = pivot3

        sleep(1)
        mov_bar1(theta1=-theta1)
        caj.pos = vec(axle3.pos.x, axle3.pos.y, 0)

        sleep(1)
        goal = not goal

        run = not run

    else:

        bar2.rotate(angle=theta2,  axis=vec(0, 0, 1),
                    origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))

        axle3.rotate(angle=theta2,  axis=vec(0, 0, 1),
                     origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))
        caj.pos = vec(axle3.pos.x, axle3.pos.y, 0)

        sleep(1)
        caj.visible = False

        bar2.rotate(angle=-theta2, axis=vec(0, 0, 1),
                    origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))
        axle3.rotate(angle=-theta2,  axis=vec(0, 0, 1),
                     origin=vec(axle2.pos.x, axle2.pos.y, bar2.pos.z))
        sleep(1)
        mov_bar1(theta1=-theta1)
        goal = not goal
        i += 1
        run = not run
    
    # if graphing:
    #     print(anglesO)
    #     print(angles)


        
