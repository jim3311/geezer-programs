"""  poly_from_triangle        August - Nov 2024   JR

  Calculate and plot a closed irregular polygon from input list of side lengths.
    First find the largest area triangle formed by splitting the input list
    of segments into 3 pieces. Then puff out the sides of the triangle
    to make the area larger.  Finally, remove dents in the polygon. """

import sys
import math
import numpy as np
import matplotlib.pyplot as plt


def divide_list(L):
    """Copilot:  Given a list L of numbers write a python script that divides the
       the list into three parts, keeping the original order such that the sum
       of numbers in each part is approximately the same.  (needed JR fix) """

    total_sum = sum(L)
    target_sum = total_sum / 3

    list1, list2, list3 = [], [], []
    current_sum1, current_sum2, current_sum3 = 0, 0, 0
    onedone = twodone = 0  # JR addition

    for num in L:
        if ((current_sum1 + num <= total_sum/2) and (onedone == 0)):
            list1.append(num)
            current_sum1 += num
        elif ((current_sum2 + num <= target_sum) and (twodone == 0)):
            onedone = 1
            list2.append(num)
            current_sum2 += num
        else:
            twodone = 1
            list3.append(num)
            current_sum3 += num

    return list1, list2, list3


def divide_into_three_parts(L):
    """ Used Divide_list to divide list into three parts.
    Iterate to return max area triangle"""

    L = L[::-1]
    total_sum = sum(L)
    rotate_step = 0
    tempL = L
    tarea = bigtarea = 0

    while rotate_step <= len(L):
        rotate_step = rotate_step + 1
        # Initialize the three lists and their sums
        list1, list2, list3 = [], [], []
        list1, list2, list3 = divide_list(L)

        # print("Divide into 3 parts--  Sides ", list1, list2, list3)
        tarea = 0
        if ((sum(list1) < total_sum/2) and (sum(list2) < total_sum/2)
                and (sum(list3) < total_sum/2)):
            tarea = calculate_triangle(sum(list1), sum(list2), sum(list3))
        #    a1,a2,a3 = triangle_angles(sum(list1), sum(list2), sum(list3))
        #  print("Divide into 3 parts--  triangle angles = ", a1,a2,a3)
        #  if(min(a1,a2,a3) > 0.0):       # a valid triangle

        # print("Divide into 3 parts--  tarea = ",tarea)
        if tarea >= bigtarea:
            tempL = [list1, list2, list3]
            bigtarea = tarea
        L.append(L.pop(0))     # rotate first segment to end
        # print(L)
    return tempL


def calculate_angle(a, b, c):
    """ Function to calculate angle using law of cosines """
    if 2*max([a, b, c]) > sum([a, b, c]):
        print("Can't calculate angle for  ", a, b, c)
    angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c))
    return angle


def normalize(vector):
    """  make size of vector = 1 """
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
    if magnitude != 0:
        return (vector[0] / magnitude, vector[1] / magnitude)
    return (0, 0)


def cross_product(A, B, C):
    """"Function to calculate the cross product of normalized vectors AB and AC"""

    AB = (B[0] - A[0], B[1] - A[1])
    AC = (C[0] - A[0], C[1] - A[1])

    # Normalize the vectors AB and AC
    AB_normalized = normalize(AB)
    AC_normalized = normalize(AC)

    cross_prod = AB_normalized[0] * AC_normalized[1] - \
        AB_normalized[1] * AC_normalized[0]
    return cross_prod


def int_angs(vertices, sides):
    """  Function to calculate the internal angles of the polygon"""

    angs = [0.0 for element in sides]
    n = len(sides)
#    print("int_angs vertices and sides   ",n,vertices[n-1],sides[n-1],sides[0])
    angs[0] = math.degrees(calculate_angle(calculate_distance(
        vertices[n-1], vertices[1]), sides[n-1], sides[0]))
    for i in range(1, n):
        angs[i] = math.degrees(calculate_angle(calculate_distance(
            vertices[i-1], vertices[i+1]), sides[i-1], sides[i]))
    return angs


def calculate_triangle(a, b, c):
    """ Function to calculate triangle area using Heron's formulia"""

    # calculate the semi-perimeter
    s = (a + b + c) / 2
    # calculate the area
    tarea = math.sqrt(s*(s-a)*(s-b)*(s-c))
    return tarea


def triangle_angles(a, b, c):
    """" Calculate the interior angles in radians using the Law of Cosines"""

    angle_A = math.acos(min(1, (b**2 + c**2 - a**2) / (2 * b * c)))
    angle_B = math.acos(min(1, (a**2 + c**2 - b**2) / (2 * a * c)))
    angle_C = math.acos(max(-1, (a**2 + b**2 - c**2) / (2 * a * b)))
    return angle_A, angle_B, angle_C


def area(vertices, sides):
    """ Function to calculate the area enclosed by the sides of a polygon """

    n = len(sides)
    acres = calculate_triangle(
        sides[0], sides[1], calculate_distance(vertices[0], vertices[2]))
    if n == 3:
        return acres
    acres = acres + calculate_triangle(calculate_distance(
        vertices[0], vertices[n-1]), sides[n-2], calculate_distance(vertices[0], vertices[n-2]))
    if n == 4:
        return acres
    for i in range(2, n-2):
        acres = acres + calculate_triangle(sides[i], calculate_distance(
            vertices[0], vertices[i]), calculate_distance(vertices[0], vertices[i+1]))
    return acres


def calculate_distance(vertex1, vertex2):
    """ Function to calculate the distance between two vertices"""

    # Unpack the coordinates
    x1, y1 = vertex1
    x2, y2 = vertex2
    # Calculate the distance
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance


def rotate_until_max_first(lst):
    """ Function to rotate list of sides until longest side is at start of list"""

    # Find the index of the maximum number in the list
    max_index = lst.index(max(lst))
    # Rotate the list until the maximum number is at the front
    for _ in range(max_index):
        lst.append(lst.pop(0))
    return lst


def rotate_vertex(vertex1, vertex2, alpha):
    """ Function to rotate vertex1 about vertex2 by angle alpha radians"""

    # Unpack the coordinates
    x1, y1 = vertex1
    x2, y2 = vertex2

    # To convert alpha to radians:  alpha = math.radians(alpha)

    # Calculate the coordinates of the new vertex
    x = x2 + math.cos(alpha) * (x1 - x2) - math.sin(alpha) * (y1 - y2)
    y = y2 + math.sin(alpha) * (x1 - x2) + math.cos(alpha) * (y1 - y2)
    return (x, y)


def translate(l_vert, vert0):
    """# Function to translate list of vertices l_vert so that first vertex
    is at vert0"""

    new_vert_list = []
    x0, y0 = vert0
    for vert in l_vert:
        x, y = vert
        x = x + x0
        y = y + y0
        vert = x, y
        new_vert_list.append(vert)
    return new_vert_list


def get_side_lengths_from_user():
    """ Ask the user to input a list of side lengths separated by commas """

    user_input = input(
        "Please enter a list of side lengths separated by commas or 'quit' to exit: ")
# Split the input string into a list
    sides = user_input.split(',')
    if len(sides) < 2:
        print("Exiting the program...")
        sys.exit()
    else:
        # Convert the list items to decimal numbers
        sides = [float(item) for item in sides]
        return sides


def plot_poly(tarea, sides, vertices):
    """ Draw the polygon in pyplot.  Calculates and shows distance between
        vertices.  Side drawn in red if calculated dist <> input side length."""

    # Unzip the coordinates
    x, y = zip(*vertices)
    distances = [0.0 for element in x]
    for i in range(len(x)-1):
        distances[i] = math.dist((x[i+1], y[i+1]), (x[i], y[i]))
#        print("Plot points and distances  ", i,x[i],y[i],"   ", distances[i])
    # Plot the polygon
    plt.figure()
    plt.plot(x, y,  'b-', marker='o')
    plt.fill(x, y, 'b', alpha=0.2)      # fill the polygon
    plt.gca().set_aspect('equal', adjustable='box')
    n = len(x) - 2
    for i in range(n+1):
        dist = distances[i]
     #   plt.text(x[i], y[i,], f'V{i+1}', fontsize=12, ha='right')
        if i < n:
            mid_x = (x[i] + x[i+1])/2
            mid_y = (y[i] + y[i+1])/2
        else:
            mid_x = (x[i] + x[0])/2
            mid_y = (y[i] + y[0])/2
        plt.text(mid_x, mid_y, f'{dist:.2f}', fontsize=12, ha='left')

    if abs(distances[n]-sides[n]) >= 0.01*sides[n]:
        plt.plot([x[n], x[n+1]], [y[n], y[n+1]], 'r-')
    acres = tarea
    if tarea == 0:           # calculate area if poly not a triangle
        acres = area(vertices, sides)
    plt.text(max(x)/5, (max(y)+min(y))/2,
             f'Area = {acres:.2f}', fontsize=16, ha='left')
    plt.show()
    return 0  # dist


def initialize_vertices(delta, tside):   # one side of triangle
    """ Calculate the coordinates of the vertices; delta = interior angle"""

    # print(tside, "  delta ",delta)
    vertices = [(0, 0), (tside[0], 0)]
    n = len(tside)
    angle = 0.0
    for i in range(2, n+1):
        angle = angle + delta
        # Calculate the coordinates of the current vertex
        x = vertices[i-1][0] + tside[i-1] * np.cos(angle)
        y = vertices[i-1][1] + tside[i-1] * np.sin(angle)
        vertices.append((x, y))
    # print("Unrotated vertices  ",vertices)
    # put vertices along x-axis
    x1, y1 = vertices[-1]
    dis = math.sqrt(x1*x1 + y1*y1)
    angle = -math.acos(x1/dis)
    for i in range(1, n+1):
        vertices[i] = rotate_vertex(vertices[i], vertices[0], angle)

    # print("Initialized vertices  ",vertices)
    return vertices


def attach_next_side(vlist1, vlist2, angle):
    """ Attach vlist2 to last vertex in vlist1 """

    v0 = vlist1[-1]
    newlist = vlist1
    vlist2 = translate(vlist2, v0)
    newlist.pop()
    for v in vlist2:
        newlist.append(rotate_vertex(v, v0, angle))
    return newlist


def build_initial_triangle(tsides):
    """ Build triangle from list of vertices along each side"""

    a1, a2, a3 = triangle_angles(
        sum(tsides[0]), sum(tsides[1]), sum(tsides[2]))
    # print(tsides)
    # print("build_initial_triangle -- triangle angles = ", a1,a2,a3)
    tarea = calculate_triangle(sum(tsides[0]), sum(tsides[1]), sum(tsides[2]))
    # print("build_initial_triangle -- Triangle Area = ", tarea)
    delta = 0
    tvertices0 = initialize_vertices(delta, tsides[0])
    vertices = tvertices0

    tvertices1 = initialize_vertices(delta, tsides[1])
    vertices = attach_next_side(vertices, tvertices1, (math.pi - a3))
    tvertices2 = initialize_vertices(delta, tsides[2])
    vertices = attach_next_side(vertices, tvertices2, (-a3 - a1))

    # print("build_initial_triangle -- Initial Triangle Sides ",sides, "  Vertices  ",vertices)
    return (tarea, vertices)


def bend_triangle_sides(n, tsides, vertices):
    """ Bend triangle sides at interior vertices by angle for symetric polygon"""

    delta = math.pi - math.radians((n-2)*180/n)
    tvertices0 = initialize_vertices(delta, tsides[0])
    tvertices1 = initialize_vertices(delta, tsides[1])
    tvertices2 = initialize_vertices(delta, tsides[2])
    d0 = calculate_distance(tvertices0[0], tvertices0[-1])
    d1 = calculate_distance(tvertices1[0], tvertices1[-1])
    d2 = calculate_distance(tvertices2[0], tvertices2[-1])
    dists = [d0, d1, d2]
    if max(dists) > sum(dists)/2:
        print("Can't make a triangle with bent sides")
        return vertices

    # print("bend_triangle_sides -- d0,d1,d2  ", d0,d1,d2,
    # " arg  ", ((d0**2 + d1**2 - d2**2) / (2 * d0 * d1)))
    a1, a2, a3 = triangle_angles(d0, d1, d2)

    vertices = tvertices0
    vertices = attach_next_side(vertices, tvertices1, (math.pi - a3))
    vertices = attach_next_side(vertices, tvertices2, (-a3 - a1))

    # print("bend_triangle_sides -- Sides ",sides, "  Vertices  ",vertices)
    return vertices


def fix_dents(n, vertices):
    """ Eliminate interior angles > 180 from polygon"""

    vertices.extend(vertices[:2])    # add first 2 vertices to end
    dents = 0
    for i in range(0, n):
        A = vertices[i]
        B = vertices[i+1]
        C = vertices[i+2]

        if cross_product(A, B, C) < -1.0e-10:  # cross product negative for interior angle > 180
            angle = math.asin(cross_product(A, B, C))
            print("fix dents  Angle  ",angle)
            vertices[i+1] = rotate_vertex(B, A, 2*angle)
            dents = dents + 1

    vertices = vertices[:-2]  # Delete the two added vertices
    return dents, vertices


def main():
    """ Main Program for Calculating Irregular Polygon"""

    while True:
        sides = []   # Array of side lengths
    #    sides = [1,3,2,4,5,6,7]    [1,3,2,4,5,6,9,5,6] sample inputs
        sides = get_side_lengths_from_user()  # use this to ask the user for input
        if (max(sides) > sum(sides)/2) or (len(sides) < 3):
            sys.exit(
                "Execution ended because one side is too large to form a triangle")
     #   print(sides)
        n = len(sides)
        tsides = []
        tsides = divide_into_three_parts(sides)   # make 3 triangle sides
        sides = tsides[0] + tsides[1] + tsides[2]

        tarea, vertices = build_initial_triangle(
            tsides)  # triangle with straight sides
        dist = plot_poly(tarea, sides, vertices)

        vertices = bend_triangle_sides(
            n, tsides, vertices)  # triangle with bends added
        dist = plot_poly(0, sides, vertices)
        if dist != 0:
            print("Polygon failed to close after bending triangle. Gap = ", dist)

        # Now puff out -- eliminate interior angles > 180"
        dents = 1
        while dents > 0:
            dents, vertices = fix_dents(n, vertices)
            if dents > 0:
                dist = plot_poly(0, sides, vertices)
                if dist != 0:
                    print("Polygon failed to close after fixing dents. Gap = ", dist)


if __name__ == "__main__":
    main()
