#! /usr/bin/python3

import sys
import random
import math

#route class
class map:
    #kind of confusing:
    #order is initialized to 0, 1, 2 ...
    #points uses that initialization to tie the point (0 or 1 or 2...) to its
    #ordered pair ({(0, [1,4]), (1, [4,3])}, etc)
    #then how calc_length works is it goes thru order, from last-first to (last-1)-last
    #and does pythagorean thereom
    #then the sum of that loop is self.length
    #so you can change around order and then call calc_length(self)
    #to update self.length
    def __init__(self, name, xpoints, ypoints):
        self.name = name
        self.order = [k for k in range(len(xpoints))] #the initial order is just [1, 2, 3...]
        self.points = {} #a dictionary
        for k in self.order:
            self.points[k] = [xpoints[k], ypoints[k]] #a dictionary of ordered pairs
    #call this after you initialize map object!
    def calc_length(self):
        length = 0
        i = -1
        while i < (len(self.order) - 1):
            current = self.order[i]
            next = self.order[i+1]
            deltax = self.points[current][0] - self.points[next][0]
            deltay = self.points[current][1] - self.points[next][1]
            before_root = deltax * deltax + deltay * deltay
            length += pow(before_root, .5)
            i+=1
        self.length = length

def fill_in(input, name):
    f = open(input, "r")
    lines = f.readlines()
    index = ""
    try:
        index = 0
        while name not in lines[index]:
            index+=1
        #print("index: %d"%index)
    except:
        print("%s not found in input file"%name)
        return -1

    xpoints = lines[index+1].strip()
    xpoints = xpoints.split(',')
    xpoints = [int(k) for k in xpoints]
    #print("for name: %s, xpoints:"%name)
    #print(xpoints)

    ypoints = lines[index+2].strip()
    ypoints = ypoints.split(',')
    ypoints = [int(k) for k in ypoints]
    #print("ypoints:")
    #print(ypoints)

    initial = map(name, xpoints, ypoints)
    initial.calc_length() #initialize length variable
    #returning a map object
    f.close()
    return initial

#simulate annealing
'''
we have a dummy map object that has order that's just one swap diff from initial
ofc do dummy.calc_length() to get the length
then compare the length of dummy and length of initial to see if
initial should assume that order. How do you decide that and not take forever?:

so we have a loop, index i = 100 and decreases by 1 each time
i is the 'heat'
for each time of the loop, we will make dummy have an order that is just
initial's order but with one set of points swapped
difference = dummy.length - initial.length
if difference < 0, make initial assume dummy's order
else, if difference/i < 1 (so, dummy is less than i units longer than initial)
then swap anyways (this is so we don't get stuck in local extrema)
the point is as the heat decreases, there will be less random swapping
w/ the intention of focusing in on one extrema

'''
def best_route(initial):
    len_order = len(initial.order)
    #create xpoints and ypoints from initial, b/c they're stored in a dict
    xpoints = []
    ypoints = []
    for k in range(len_order):
        xpoints.append(initial.points[k][0]) #x
        ypoints.append(initial.points[k][1]) #y
    dummy = map("dummy", xpoints, ypoints)
    dummy.calc_length()
    #test that dummy is a copy of our point:
    '''
    print("looking at %s"%dummy.name)
    for k in dummy.order:
        print("point %d:"%k)
        print(dummy.points[k])
    print("initial length: %f"%dummy.length)
    '''
    #know that dummy's order is set to 0, 1, 2 like initial's

    #now go into the loop that will allow for swaps
    i = 10000
    while i > 1:
        #choose 2 random positions in order to swap
        a = random.randrange(1, len_order) #a and b should never be 0
        b = random.randrange(1, len_order)
        #oh also you shouldn't move the 0th point
        if a==b and a != 1:
            a-=1 #cuz you can do negative indexing but no index>len
        elif a==b:
            a+=1 #to avoid getting a = 0 ever
        #print("i: %d, a: %d, b: %d"%(i, a, b))

        #make dummy's order
        temp_order = swap(initial.order[:], a, b)
        dummy.order = temp_order #not sure if all this copying is necessary

        #calculate the length of this new route
        dummy.calc_length()

        #now make the comparison to see if initial should assume that order
        difference = dummy.length - initial.length
        if difference < 0: #or difference/i < 1:
            #aka, dummy is less than i units longer than initial or dummy is shorter
            initial.order = dummy.order[:] #make it a copy so it doesn't switch each time!
            initial.calc_length() #remember to update the length!

        #else, don't change initial
        i-=.2
    return 0

def swap(order, a, b):
    temp = order[a]
    order[a] = order[b]
    order[b] = temp
    return order

def fill_out(output, mapObj):
    f = open(output, 'a')
    f.write('\n')
    f.write(mapObj.name)
    f.write('\n')
    order_string = [str(k) for k in mapObj.order]
    order_string = ','.join(order_string)
    f.write(order_string)
    f.write('\n')
    f.close()
    return 0

#command line variabels: this.py points.csv StudentPaths.csv name_route
def main(argv=None):
    #
    if not argv:
        argv = sys.argv
    input = argv[1]
    output = argv[2]
    name = argv[3]
    # create map object w/ data from input & name
    initial = fill_in(input, name)
    #testing -- printint out info of map
    if initial == -1:
        print("fill_in failed")
    '''else:
        print("testing:")
        print("looking at %s"%initial.name)
        for k in initial.order:
            print("point %d:"%k)
            print(initial.points[k])
        print("initial length: %f"%initial.length)
    '''
    # do solving
    best_route(initial) #returns initial with updated order
    print("finished best route, final length: %f"%initial.length)
    # write out results (from route)
    fill_out(output, initial)
    return 0

main()
