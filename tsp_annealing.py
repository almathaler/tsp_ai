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

def best_route(initial):
    #initial is a map object
    #does random switching w.r.t temperature
    #returns the object w/ best route it could find
    return 0
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
    else:
        print("testing:")
        print("looking at %s"%initial.name)
        for k in initial.order:
            print("point %d:"%k)
            print(initial.points[k])
        print("initial length: %f"%initial.length)
    # do solving
    best_route(initial) #should modify order of initial
    # write out results (from route)
    fill_out(output, initial)
    return 0

main()
