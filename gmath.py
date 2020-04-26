import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)
    iambient = calculate_ambient(ambient, areflect)
    idiffuse = calculate_diffuse(light, dreflect, normal)
    ispecular = calculate_specular(light, sreflect, view, normal)
    # print("A: " + str(iambient))
    # print("D: " + str(idiffuse))
    # print("S: " + str(ispecular))
    return limit_color([int(iambient[0] + idiffuse[0] + ispecular[0]),
                        int(iambient[1] + idiffuse[1] + ispecular[1]),
                        int(iambient[2] + idiffuse[2] + ispecular[2])])

def calculate_ambient(alight, areflect):
    return [alight[0] * areflect[0], alight[1] * areflect[1], alight[2] * areflect[2]]

def calculate_diffuse(light, dreflect, normal):
    d = dot_product(normal, light[0])
    if d < 0: d = 0
    return [light[1][0] * dreflect[0] * d,
            light[1][1] * dreflect[1] * d,
            light[1][2] * dreflect[2] * d]

def calculate_specular(light, sreflect, view, normal):
    temp = dot_product([(2 * normal[0] * dot_product(normal, light[0])) - light[0][0],
                        (2 * normal[1] * dot_product(normal, light[0])) - light[0][1],
                        (2 * normal[2] * dot_product(normal, light[0])) - light[0][2]], view)
    if temp < 0: temp = 0
    return [light[1][0] * sreflect[0] * math.pow(temp, SPECULAR_EXP),
            light[1][1] * sreflect[1] * math.pow(temp, SPECULAR_EXP),
            light[1][2] * sreflect[2] * math.pow(temp, SPECULAR_EXP)]


def limit_color(color):
    if color[RED] > 255:
        color[RED] = 255
    elif color[RED] < 0:
        color[RED] = 0
    if color[GREEN] > 255:
        color[GREEN] = 255
    elif color[GREEN] < 0:
        color[GREEN] = 0
    if color[BLUE] > 255:
        color[BLUE] = 255
    elif color[BLUE] < 0:
        color[BLUE] = 0
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
