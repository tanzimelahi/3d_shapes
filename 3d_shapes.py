import math
from subprocess import Popen, PIPE
from os import remove

#constants
XRES = 500
YRES = 500
MAX_COLOR = 255
RED = 0
GREEN = 1
BLUE = 2

DEFAULT_COLOR = [0, 0, 0]

def new_screen( width = XRES, height = YRES ):
    screen = []
    for y in range( height ):
        row = []
        screen.append( row )
        for x in range( width ):
            screen[y].append( DEFAULT_COLOR[:] )
    return screen

def plot( screen,x,y,color ):
    newy = YRES - 1 - y
    if ( x < XRES and newy < YRES ):
        screen[int(newy)][int(x)] = color[:]

def clear_screen( screen ):
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            screen[y][x] = DEFAULT_COLOR[:]

def save_ppm( screen, fname ):
    f = open( fname, 'wb' )
    ppm = 'P6\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    f.write(ppm.encode())
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            f.write( bytes(pixel) )
    f.close()

def save_ppm_ascii( screen, fname ):
    f = open( fname, 'w' )
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range( len(screen) ):
        row = ''
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            row+= str( pixel[ RED ] ) + ' '
            row+= str( pixel[ GREEN ] ) + ' '
            row+= str( pixel[ BLUE ] ) + ' '
        ppm+= row + '\n'
    f.write( ppm )
    f.close()

def save_extension( screen, fname ):
    ppm_name = fname[:fname.find('.')] + '.ppm'
    save_ppm_ascii( screen, ppm_name )
    p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

def display( screen ):
    ppm_name = 'pic.ppm'
    save_ppm_ascii( screen, ppm_name )
    p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

#commands from here:
#for the first two octants, the x0 must be smaller than x1
def firstoct(screen,x0,y0,x1,y1,color):#oct 1 and 5
    x=x0
    y=y0
    A=y1-y0
    B=-(x1-x0)
    d=2*A+B
    while x<x1:
        plot(screen,x,y,color)
        if d>=0:
            y+=1
            d=d+2*B
        x=x+1
        d=d+2*A
    plot(screen,x1,y1,color)
def secondoct(screen,x0,y0,x1,y1,color):#oct 2 and 6
    x=x0
    y=y0
    A=y1-y0
    B=-(x1-x0)
    d=A+2*B
    while y<y1:
        plot(screen,x,y,color)
        if d<=0:
            d=d+2*A
            x+=1
        y=y+1
        d=d+2*B
    plot(screen,x1,y1,color)
def thirdoct(screen,x0,y0,x1,y1,color):#oct 3 and 7 remember the x0 and x1 hierarchy is reversed for this one
    x=x0
    y=y0
    A=y1-y0
    B=-(x1-x0)
    d=A+2*B
    while y<y1:
        plot(screen,x,y,color)
        if d>=0:
            x=x-1
            d=d-2*A
        y=y+1
        d=d+2*B
    plot(screen,x1,y1,color)
def fourthoct(screen,x0,y0,x1,y1,color): #oct 4 and 8
    x=x0
    y=y0
    A=y1-y0
    B=-(x1-x0)
    d=A+2*B
    while x<x1:
        plot(screen,x,y,color)
        if d<=0:
            y=y-1
            d=d-2*B
        x=x+1
        d=d+2*A
    plot(screen,x1,y1,color)
def oneSlopePos(screen,x0,y0,x1,y1,color):
    x=x0
    y=y0
    while x<=x1:
        plot(screen,x,y,color)
        x+=1
        y+=1

def oneSlopeNeg(screen,x0,y0,x1,y1,color):
    x=x0
    y=y0
    while x<=x1:
        plot(screen,x,y,color)
        x+=1
        y-=1
def zeroSlope(screen,x0,y0,x1,y1,color):
    x=x0
    y=y0
    while(x<=x1):
        plot(screen,x,y,color)
        x+=1
def undefinedSlope(screen,x0,y0,x1,y1,color):
    x=x0
    y=y0
    while y<=y1:
        plot(screen,x,y,color)
        y+=1

def drawline(screen,x0,y0,x1,y1,color):# whenever possible x0 must be greater than x1(left to right orientation)
    if(x0>x1):
        store=x0
        x0=x1
        x1=store
        storage=y0
        y0=y1
        y1=storage
    if(x0==x1):
        if(y1<y0):
            store=y0
            y0=y1
            y1=store
        undefinedSlope(screen,x0,y0,x1,y1,color)
    elif(y0==y1):
        zeroSlope(screen,x0,y0,x1,y1,color)
    elif abs(x1-x0)>=abs(y1-y0):
        if y1>y0:
            firstoct(screen,x0,y0,x1,y1,color)
        else:
            fourthoct(screen,x0,y0,x1,y1,color)
    else:
        if y1>y0:
            secondoct(screen,x0,y0,x1,y1,color)
        else:
            thirdoct(screen,x1,y1,x0,y0,color)



def new_matrix(rows = 4, cols = 4):
    m = []
    for c in range( cols ):
        m.append( [] )
        for r in range( rows ):
            m[c].append( 0 )
    return m
def update_matrix(row,column,matrix,value):
    matrix[column][row]=value
def up(matrix,row,column,value):
    matrix[column][row]=value
def print_matrix(matrix):
    result=""
    row=len(matrix[0])
    col=len(matrix)
    for x in range(row):
        for y in range(col):
            add=str(matrix[y][x])
            if len(add)==1:
                result+=add+"   "
            elif len(add)==2:
                result+=add+"  "
            else:
                result+=add+" "
        result+="\n"
    print(result)
        


def ident(matrix):
    row=len(matrix[0])
    col=row
    for x in range(row):
        for y in range(col):
            if(x==y):
                matrix[y][x]=1
            else:
                matrix[y][x]=0
def matrix_multiplication(m1,m2): #this func works fine
    result=new_matrix(len(m1[0]),len(m2))
    for secondCol in range(len(m2)):
        for y in range(len(m1[0])):
            add=0
            for x in range(len(m1)):
                add+=(m1[x][y]*m2[secondCol][x])
            result[secondCol][y]=add
    for x in range(len(m2)):
        m2[x]=result[x]
def empty_matrix():
    m = []
    m.append( [] )
    return m
#test cases


#that ends here
def add_point(matrix,x,y,z=0):
    if len(matrix[0])==0:
        matrix[0].append(x)
        matrix[0].append(y)
        matrix[0].append(z)
        matrix[0].append(1)
    else:
        matrix.append([])
        matrix[len(matrix)-1].append(x)
        matrix[len(matrix)-1].append(y)
        matrix[len(matrix)-1].append(z)
        matrix[len(matrix)-1].append(1)
        
def update_point(matrix,x,y,z,unit=1):  #same as add_point but can modify the '1's used as helper func for rotation
    if len(matrix[0])==0:
        matrix[0].append(x)
        matrix[0].append(y)
        matrix[0].append(z)
        matrix[0].append(unit)
    else:
        matrix.append([])
        matrix[len(matrix)-1].append(x)
        matrix[len(matrix)-1].append(y)
        matrix[len(matrix)-1].append(z)
        matrix[len(matrix)-1].append(unit)
    
def add_edge(matrix,x0,y0,z0,x1,y1,z1):
    add_point(matrix,x0,y0,z0)
    add_point(matrix,x1,y1,z1)
def add_lines(screen,matrix,color):
    step=0
    while(step<len(matrix)):
        #print("x0:"+str(matrix[step][0])+"  "+"y0:"+str(matrix[step][1])+"  "+"x1:"+str(matrix[step+1][0])+"  "+"y1:"+str(matrix[step+1][1]))
        drawline(screen,matrix[step][0],matrix[step][1],matrix[step+1][0],matrix[step+1][1],color)
        step+=2
def scale(sx,sy,sz):
    info=[sx,sy,sz]
    matrix=new_matrix(4,4)
    ident(matrix)
    for col in range(len(matrix)-1):
        for row in range(len(matrix[0])-1):
            if row==col:
                matrix[col][row]=info[col]

    return matrix
def move(a,b,c):
    info=[a,b,c]
    matrix=new_matrix(4,4)
    ident(matrix)
    for row in range(len(matrix)-1):
        matrix[3][row]=info[row]
    return matrix



def x_rotation(angle):
    angle=math.radians(angle)
    matrix=empty_matrix()
    update_point(matrix,1,0,0,0)
    update_point(matrix,0,math.cos(angle),1*math.sin(angle),0)
    update_point(matrix,0,-1*math.sin(angle),math.cos(angle),0)
    update_point(matrix,0,0,0,1)
    return matrix
     
    

def y_rotation(angle):
    angle=math.radians(angle)
    matrix=empty_matrix()
    update_point(matrix,math.cos(angle),0,-1*math.sin(angle),0)
    update_point(matrix,0,1,0,0)
    update_point(matrix,1*math.sin(angle),0,math.cos(angle),0)
    update_point(matrix,0,0,0,1)
    return matrix



def z_rotation(angle):
    angle=math.radians(angle)
    matrix=empty_matrix()
    update_point(matrix,math.cos(angle),1*math.sin(angle),0,0)
    update_point(matrix,-1*math.sin(angle),math.cos(angle),0,0)
    update_point(matrix,0,0,1,0)
    update_point(matrix,0,0,0,1)
    return matrix
   

    
def rotation (angle,axis_of_rotation):
    if(axis_of_rotation=="x"):
        return x_rotation(angle)
    elif axis_of_rotation=="y":
        return y_rotation(angle)
    else:
        return z_rotation(angle)

def bezier(matrix,x0,y0,x1,y1,x2,y2,x3,y3):
    ax=-x0+3*x1-3*x2+x3
    bx=3*x0-6*x1+3*x2
    cx=-3*x0+3*x1
    dx=x0
    ay=-y0+3*y1-3*y2+y3
    by=3*y0-6*y1+3*y2
    cy=-3*y0+3*y1
    dy=y0
    t=0
    input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
    input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
    t+=0.0001
    new_input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
    new_input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
    add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
    input_x=new_input_x
    input_y=new_input_y
    t+=0.0001
    while(t<=1):
        new_input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
        new_input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
        add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
        input_x=new_input_x
        input_y=new_input_y
        t+=0.0001
    
def hermite(matrix,x0,y0,x1,y1,rx0,ry0,rx1,ry1):
    my_matrix=empty_matrix()
    m2x=empty_matrix()
    add_point(m2x,x0,x1,rx0)
    update_matrix(3,0,m2x,rx1)
    add_point(my_matrix,2,-3,0)
    add_point(my_matrix,-2,3,0)
    add_point(my_matrix,1,-2,1)
    add_point(my_matrix,1,-1,0)
    info=[1,0,0,0]
    for x in range(4):
        update_matrix(3,x,my_matrix,info[x])
    matrix_multiplication(my_matrix,m2x)
    ax=m2x[0][0]
    bx=m2x[0][1]
    cx=m2x[0][2]
    dx=m2x[0][3]
    m2y=empty_matrix()
    add_point(m2y,y0,y1,ry0)
    update_matrix(3,0,m2y,ry1)
    matrix_multiplication(my_matrix,m2y)
    ay=m2y[0][0]
    by=m2y[0][1]
    cy=m2y[0][2]
    dy=m2y[0][3]
    t=0
    input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
    input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
    t+=0.0001
    new_input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
    new_input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
    add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
    input_x=new_input_x
    input_y=new_input_y
    t+=0.0001
    while(t<=1):
        new_input_x=int(ax*math.pow(t,3)+bx*math.pow(t,2)+cx*t+dx)
        new_input_y=int(ay*math.pow(t,3)+by*math.pow(t,2)+cy*t+dy)
        add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
        input_x=new_input_x
        input_y=new_input_y
        t+=0.0001
def circle(matrix,cx,cy,cz,r):
    t=0
    input_x=int(math.cos(math.pi*2*t)*r+cx)
    input_y=int(math.sin(math.pi*2*t)*r+cy)
    t+=0.0001
    new_input_x=int(math.cos(math.pi*2*t)*r+cx)
    new_input_y=int(math.sin(math.pi*2*t)*r+cy)
    add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
    input_x=new_input_x
    input_y=new_input_y
    t+=0.01
    while(t<=1):
        new_input_x=int(math.cos(math.pi*2*t)*r+cx)
        new_input_y=int(math.sin(math.pi*2*t)*r+cy)
        add_edge(matrix,input_x,input_y,0,new_input_x,new_input_y,0)
        input_x=new_input_x
        input_y=new_input_y
        t+=0.01
     
def apply(transform,edge):
    matrix_multiplication(transform,edge)


def parser(fl_name,screen,color,edge,transform):
    fl=open(fl_name,"r")
    data=fl.readlines()
    i=0
    while(i<len(data)):
        #print(data[i].strip())
        if data[i].strip()=="line":
            coords=data[i+1].split()
            x0=int(coords[0])
            y0=int(coords[1])
            z0=int(coords[2])
            x1=int(coords[3])
            y1=int(coords[4])
            z1=int(coords[5])
            add_edge(edge,x0,y0,z0,x1,y1,z1)
        elif data[i].strip()=="ident":
            ident(transform)
        elif data[i].strip()=="scale":
            coords=data[i+1].split()
            sx=int(coords[0])
            sy=int(coords[1])
            sz=int(coords[2])
            apply(scale(sx,sy,sz),transform)
        elif data[i].strip()=="apply":
            apply(transform,edge)
        elif data[i].strip()=="move":
            coords=data[i+1].split()
            a=int(coords[0])
            b=int(coords[1])
            c=int(coords[2])
            apply(move(a,b,c),transform)
        elif data[i].strip()=="rotate":
            coords=data[i+1].split()
            angle=int(coords[0])
            axis=coords[1]
            apply(rotation(angle,axis),transform)
        elif data[i].strip()=="save":
            clear_screen(screen)#new update
            coords=data[i+1].split()
            add_lines(screen,edge,color)
            save_ppm(screen,coords[0])
        elif data[i].strip()=="display":
            clear_screen(screen)
            add_lines(screen,edge,color)
            display(screen)
        elif data[i].strip()=="clear":
            edge=empty_matrix()
        elif data[i].strip()=="sphere":
            coords=data[i+1].split()
            x=int(coords[0])
            y=int(coords[1])
            z=int(coords[2])
            r=int(coords[3])
            sphere(edge,x,y,z,r)
        elif data[i].strip()=="box":
             coords=data[i+1].split()
             x=int(coords[0])
             y=int(coords[1])
             z=int(coords[2])
             x_width=int(coords[3])
             y_width=int(coords[4])
             z_width=int(coords[5])
             box(edge,x,y,z,x_width,y_width,z_width)
        elif data[i].strip()=="torus":
            coords=data[i+1].split()
            x=int(coords[0])
            y=int(coords[1])
            z=int(coords[2])
            r=int(coords[3])
            R=int(coords[4])
            torus(edge,x,y,z,r,R)
        i+=1
   
        
        
def box(matrix,x,y,z,x_width,y_width,z_width):
    add_edge(matrix,x,y,z,x+x_width,y,z)#1 and 3
    add_edge(matrix,x,y,z,x,y+y_width,z)#1 and 2
    add_edge(matrix,x,y+y_width,z,x+x_width,y+y_width,z)# 2 and 4
    add_edge(matrix,x+x_width,y,z,x+x_width,y+y_width,z)#3 and 4
    add_edge(matrix,x,y,z,x,y,z+z_width)#1 and 6
    add_edge(matrix,x,y+y_width,z,x,y+y_width,z+z_width)#2 and 5
    add_edge(matrix,x,y+y_width,z+z_width,x,y,z+z_width)#5 and 6
    add_edge(matrix,x,y,z+z_width,x+x_width,y,z+z_width)#6 and 7
    add_edge(matrix,x,y+y_width,z+z_width,x+x_width,y+y_width,z+z_width)#5 and 8
    add_edge(matrix,x+x_width,y+y_width,z+z_width,x+x_width,y,z+z_width)#8 and 7
    add_edge(matrix,x+x_width,y,z,x+x_width,y,z+z_width)#3 and 7
    add_edge(matrix,x+x_width,y+y_width,z,x+x_width,y+y_width,z+z_width)#4 and 8


def sphere(matrix,cx,cy,cz,radius):
    rot=0
    t=0
    x0=radius*math.cos(2*math.pi*0)+cx
    y0=radius*math.sin(2*math.pi*0)*math.cos(math.pi*0)+cy
    z0=radius*math.sin(2*math.pi*0)*math.sin(math.pi*0)+cz
    while rot<=1:
        while t<=1:
            x=radius*math.cos(2*math.pi*t)+cx
            y=radius*math.sin(2*math.pi*t)*math.cos(2*math.pi*rot)+cy
            z=radius*math.sin(2*math.pi*t)*math.sin(2*math.pi*rot)+cz
            t+=0.0001
            add_edge(matrix,x0,y0,z0,x,y,z)
            x0=x
            y0=y
            z0=z
            t+=0.01
        t=0
        rot+=0.01
     


def torus(matrix,cx,cy,cz,r,R):
    rot=0
    t=0
    x0=math.cos(rot)*(r*math.cos(t)+R)+cx
    y0=math.sin(t)*r+cy
    z0=-1*math.sin(rot)*(r*math.cos(t)+cx+R)+cz
    while rot<=1:
        while t<=1:
            x=math.cos(2*math.pi*rot)*(r*math.cos(2*math.pi*t)+R)+cx
            y=r*math.sin(2*math.pi*t)+cy
            z=-1*math.sin(2*math.pi*rot)*(r*math.cos(2*math.pi*t)+R)+cz
            t+=0.01
            add_edge(matrix,x0,y0,z0,x,y,z)
            x0=x
            y0=y
            z0=z
            
        t=0
        rot+=0.01
        

screen=new_screen(600,600)
edge=empty_matrix()
transform=new_matrix(4,4)
ident(transform)
parser("script.txt",screen,[0,0,255],edge,transform)
print("box test pic: box.ppm")
print("first sphere test: first_sphere.ppm")
print("second sphere test: second_sphere.ppm")
print("third sphere test: third_sphere.ppm")
print("fourth sphere test: fourth_sphere.ppm")
print("first torus test: first_torus.ppm")
print("second torus test: second_torus.ppm")
print("third torus test: third_torus.ppm")
print("fourth torus test: fourth_torus.ppm")
#box(edge,0,0,0,200,100,400)
#add_lines(screen,edge,[0,0,255])
#save_ppm(screen,"munnas.ppm")


