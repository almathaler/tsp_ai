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
gonna change this, here are the hyperparameters given in
this demo (https://www.geeksforgeeks.org/simulated-annealing/):
*Initial and final temperature

*Temperature at which iteration terminates

*Decrease in temperature

*Number of iterations of annealing before decreasing temperature

also, I think I should change how it decides if to switch.
ofc I should keep the if difference < 0.
But I shouldn't use the difference/i < 1 because it's not 'normalized' (yea idk what that means)
I think the issue is that I'm confining the program to jumps around the graph that have little y variation
too quickly. The whole point is that there should be a few random jumps so the
algo can leave it's local maxima.

i think I should instead just say, if difference is positive, choose a random number between 0 and 1
if that number is less than 1-1/t, then make the change anyways. this will cause a lot
of random moves at first but hopefully this is a better approach.

Also I guess I should have more iters per certain temp
'''
#I think this should be done 3 times or so to get best route
def best_route(initial):
    len_order = len(initial.order)
    #create xpoints and ypoints from initial, b/c they're stored in a dict
    xpoints = []
    ypoints = []
    for k in range(len_order):
        xpoints.append(initial.points[k][0]) #x
        ypoints.append(initial.points[k][1]) #y
    #create dummy
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
    temp = 100
    i = 4950 #when i is a multiple of 10, decrease temp.
    cool = .2 #when i%10 == 0, temp-=cool. Can cool 495 times (temp>=1)
    while temp >= 1:
        #choose 2 random positions in order to swap
        a = random.randrange(1, len_order) #a and b should never be 0
        b = random.randrange(1, len_order)
        #oh also you shouldn't move the 0th point
        if a==b and a != 1:
            a-=1
        elif a==b:
            a+=1 #to avoid getting a = 0 ever
        #print("i: %d, a: %d, b: %d"%(i, a, b))

        #make dummy's order
        temp_order = swap(initial.order[:], a, b)
        dummy.order = temp_order #not sure if all this copying is necessary

        #calculate the length of this new route
        dummy.calc_length()

        #set up your chance for annealing
        chance_anneal = 1 - (1/temp)
        #now make the comparison to see if initial should assume that order
        difference = dummy.length - initial.length
        if difference < 0 or (difference*chance_anneal) < 1: #or difference/i < 1:
            #aka, dummy is less than i units longer than initial or dummy is shorter
            initial.order = dummy.order[:] #make it a copy so it doesn't switch each time!
            initial.calc_length() #remember to update the length!
        #now change our variables
        if i%10 == 0:
            temp -= cool
        i-=1

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
