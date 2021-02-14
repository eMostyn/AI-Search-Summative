############
############ ALTHOUGH I GIVE YOU THE 'BARE BONES' OF THIS PROGRAM WITH THE NAME
############ 'skeleton.py', YOU CAN RENAME IT TO ANYTHING YOU LIKE. HOWEVER, FOR
############ THE PURPOSES OF THE EXPLANATION IN THESE COMMENTS, I ASSUME THAT
############ THIS PROGRAM IS STILL CALLED 'skeleton.py'.
############
############ IF YOU WISH TO IMPORT STANDARD MODULES, YOU CAN ADD THEM AFTER THOSE BELOW.
############ NOTE THAT YOU ARE NOT ALLOWED TO IMPORT ANY NON-STANDARD MODULES!
############

import os
import sys
import time
import random
import copy
############
############ NOW PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

def read_file_into_string(input_file, ord_range):
    the_file = open(input_file, 'r') 
    current_char = the_file.read(1) 
    file_string = ""
    length = len(ord_range)
    while current_char != "":
        i = 0
        while i < length:
            if ord(current_char) >= ord_range[i][0] and ord(current_char) <= ord_range[i][1]:
                file_string = file_string + current_char
                i = length
            else:
                i = i + 1
        current_char = the_file.read(1)
    the_file.close()
    return file_string

def remove_all_spaces(the_string):
    length = len(the_string)
    new_string = ""
    for i in range(length):
        if the_string[i] != " ":
            new_string = new_string + the_string[i]
    return new_string

def integerize(the_string):
    length = len(the_string)
    stripped_string = "0"
    for i in range(0, length):
        if ord(the_string[i]) >= 48 and ord(the_string[i]) <= 57:
            stripped_string = stripped_string + the_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def convert_to_list_of_int(the_string):
    list_of_integers = []
    location = 0
    finished = False
    while finished == False:
        found_comma = the_string.find(',', location)
        if found_comma == -1:
            finished = True
        else:
            list_of_integers.append(integerize(the_string[location:found_comma]))
            location = found_comma + 1
            if the_string[location:location + 5] == "NOTE=":
                finished = True
    return list_of_integers

def build_distance_matrix(num_cities, distances, city_format):
    dist_matrix = []
    i = 0
    if city_format == "full":
        for j in range(num_cities):
            row = []
            for k in range(0, num_cities):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    elif city_format == "upper_tri":
        for j in range(0, num_cities):
            row = []
            for k in range(j):
                row.append(0)
            for k in range(num_cities - j):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    else:
        for j in range(0, num_cities):
            row = []
            for k in range(j + 1):
                row.append(0)
            for k in range(0, num_cities - (j + 1)):
                row.append(distances[i])
                i = i + 1
            dist_matrix.append(row)
    if city_format == "upper_tri" or city_format == "strict_upper_tri":
        for i in range(0, num_cities):
            for j in range(0, num_cities):
                if i > j:
                    dist_matrix[i][j] = dist_matrix[j][i]
    return dist_matrix

def read_in_algorithm_codes_and_tariffs(alg_codes_file):
    flag = "good"
    code_dictionary = {}   
    tariff_dictionary = {}  
    if not os.path.exists(alg_codes_file):
        flag = "not_exist"  
        return code_dictionary, tariff_dictionary, flag
    ord_range = [[32, 126]]
    file_string = read_file_into_string(alg_codes_file, ord_range)  
    location = 0
    EOF = False
    list_of_items = []  
    while EOF == False: 
        found_comma = file_string.find(",", location)
        if found_comma == -1:
            EOF = True
            sandwich = file_string[location:]
        else:
            sandwich = file_string[location:found_comma]
            location = found_comma + 1
        list_of_items.append(sandwich)
    third_length = int(len(list_of_items)/3)
    for i in range(third_length):
        code_dictionary[list_of_items[3 * i]] = list_of_items[3 * i + 1]
        tariff_dictionary[list_of_items[3 * i]] = int(list_of_items[3 * i + 2])
    return code_dictionary, tariff_dictionary, flag

############
############ THE RESERVED VARIABLE 'input_file' IS THE CITY FILE UNDER CONSIDERATION.
############
############ IT CAN BE SUPPLIED BY SETTING THE VARIABLE BELOW OR VIA A COMMAND-LINE
############ EXECUTION OF THE FORM 'python skeleton.py city_file.txt'. WHEN SUPPLYING
############ THE CITY FILE VIA A COMMAND-LINE EXECUTION, ANY ASSIGNMENT OF THE VARIABLE
############ 'input_file' IN THE LINE BELOW iS SUPPRESSED.
############
############ IT IS ASSUMED THAT THIS PROGRAM 'skeleton.py' SITS IN A FOLDER THE NAME OF
############ WHICH IS YOUR USER-NAME, E.G., 'abcd12', WHICH IN TURN SITS IN ANOTHER
############ FOLDER. IN THIS OTHER FOLDER IS THE FOLDER 'city-files' AND NO MATTER HOW
############ THE NAME OF THE CITY FILE IS SUPPLIED TO THIS PROGRAM, IT IS ASSUMED THAT 
############ THE CITY FILE IS IN THE FOLDER 'city-files'.
############

input_file = "AISearchfile012.txt"

############
############ PLEASE SCROLL DOWN UNTIL THE NEXT BLOCK OF CAPITALIZED COMMENTS.
############
############ DO NOT TOUCH OR ALTER THE CODE IN BETWEEN! YOU HAVE BEEN WARNED!
############

if len(sys.argv) > 1:
    input_file = sys.argv[1]

the_particular_city_file_folder = "city-files"
    
if os.path.isfile("../" + the_particular_city_file_folder + "/" + input_file):
    ord_range = [[32, 126]]
    file_string = read_file_into_string("../" + the_particular_city_file_folder + "/" + input_file, ord_range)
    file_string = remove_all_spaces(file_string)
    print("I have found and read the input file " + input_file + ":")
else:
    print("*** error: The city file " + input_file + " does not exist in the folder '" + the_particular_city_file_folder + "'.")
    sys.exit()

location = file_string.find("SIZE=")
if location == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
comma = file_string.find(",", location)
if comma == -1:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()
    
num_cities_as_string = file_string[location + 5:comma]
num_cities = integerize(num_cities_as_string)
print("   the number of cities is stored in 'num_cities' and is " + str(num_cities))

comma = comma + 1
stripped_file_string = file_string[comma:]
distances = convert_to_list_of_int(stripped_file_string)

counted_distances = len(distances)
if counted_distances == num_cities * num_cities:
    city_format = "full"
elif counted_distances == (num_cities * (num_cities + 1))/2:
    city_format = "upper_tri"
elif counted_distances == (num_cities * (num_cities - 1))/2:
    city_format = "strict_upper_tri"
else:
    print("*** error: The city file " + input_file + " is incorrectly formatted.")
    sys.exit()

dist_matrix = build_distance_matrix(num_cities, distances, city_format)
print("   the distance matrix 'dist_matrix' has been built.")

############
############ YOU NOW HAVE THE NUMBER OF CITIES STORED IN THE INTEGER VARIABLE 'num_cities'
############ AND THE TWO_DIMENSIONAL MATRIX 'dist_matrix' HOLDS THE INTEGER CITY-TO-CITY 
############ DISTANCES SO THAT 'dist_matrix[i][j]' IS THE DISTANCE FROM CITY 'i' TO CITY 'j'.
############ BOTH 'num_cities' AND 'dist_matrix' ARE RESERVED VARIABLES AND SHOULD FEED
############ INTO YOUR IMPLEMENTATIONS.
############

############
############ THERE NOW FOLLOWS CODE THAT READS THE ALGORITHM CODES AND TARIFFS FROM
############ THE TEXT-FILE 'alg_codes_and_tariffs.txt' INTO THE RESERVED DICTIONARIES
############ 'code_dictionary' AND 'tariff_dictionary'. DO NOT AMEND THIS CODE!
############ THE TEXT FILE 'alg_codes_and_tariffs.txt' SHOULD BE IN THE SAME FOLDER AS
############ THE FOLDER 'city-files' AND THE FOLDER WHOSE NAME IS YOUR USER-NAME, E.G., 'abcd12'.
############

code_dictionary, tariff_dictionary, flag = read_in_algorithm_codes_and_tariffs("../alg_codes_and_tariffs.txt")

if flag != "good":
    print("*** error: The text file 'alg_codes_and_tariffs.txt' does not exist.")
    sys.exit()

print("The codes and tariffs have been read from 'alg_codes_and_tariffs.txt':")

############
############ YOU NOW NEED TO SUPPLY SOME PARAMETERS.
############
############ THE RESERVED STRING VARIABLE 'my_user_name' SHOULD BE SET AT YOUR USER-NAME, E.G., "abcd12"
############

my_user_name = "skbh77"

############
############ YOU CAN SUPPLY, IF YOU WANT, YOUR FULL NAME. THIS IS NOT USED AT ALL BUT SERVES AS
############ AN EXTRA CHECK THAT THIS FILE BELONGS TO YOU. IF YOU DO NOT WANT TO SUPPLY YOUR
############ NAME THEN EITHER SET THE STRING VARIABLES 'my_first_name' AND 'my_last_name' AT 
############ SOMETHING LIKE "Mickey" AND "Mouse" OR AS THE EMPTY STRING (AS THEY ARE NOW;
############ BUT PLEASE ENSURE THAT THE RESERVED VARIABLES 'my_first_name' AND 'my_last_name'
############ ARE SET AT SOMETHING).
############

my_first_name = "Elis"
my_last_name = "Mostyn"

############
############ YOU NEED TO SUPPLY THE ALGORITHM CODE IN THE RESERVED STRING VARIABLE 'algorithm_code'
############ FOR THE ALGORITHM YOU ARE IMPLEMENTING. IT NEEDS TO BE A LEGAL CODE FROM THE TEXT-FILE
############ 'alg_codes_and_tariffs.txt' (READ THIS FILE TO SEE THE CODES).
############

algorithm_code = "AC"

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW! YOU HAVE BEEN WARNED!
############

if not algorithm_code in code_dictionary:
    print("*** error: the agorithm code " + algorithm_code + " is illegal")
    sys.exit()
print("   your algorithm code is legal and is " + algorithm_code + " -" + code_dictionary[algorithm_code] + ".")

############
############ YOU CAN ADD A NOTE THAT WILL BE ADDED AT THE END OF THE RESULTING TOUR FILE IF YOU LIKE,
############ E.G., "in my basic greedy search, I broke ties by always visiting the first 
############ city found" BY USING THE RESERVED STRING VARIABLE 'added_note' OR LEAVE IT EMPTY
############ IF YOU WISH. THIS HAS NO EFFECT ON MARKS BUT HELPS YOU TO REMEMBER THINGS ABOUT
############ YOUR TOUR THAT YOU MIGHT BE INTERESTED IN LATER.
############

added_note = ""

############
############ NOW YOUR CODE SHOULD BEGIN.
############



#Nearest neighbour search
def nearestNeighbour(num_cities,dist_matrix):
    #The current tour, starting at city 0 
    currTour = [0]
    #Holds weights 
    weight = []
    #While the tour isnt the same length as amount of cities
    while len(currTour) != num_cities:
        #Get the weights to all other citys
        weights = dist_matrix[currTour[-1]]
        smallest = [99999999999,0]
        #For each edge 
        for i in range(0,len(weights)):
            #If not currently visited
            if i not in currTour:
                #If the dist = 0 then its the same city so ignore it
                if weights[i] != 0 and weights[i] < smallest[0]:
                    smallest = weights[i],i
        #Append the city and weight to the appropriate places
        currTour.append(smallest[1])
        weight.append(smallest[0])
    #Return the tour and the distance, including last to first city 
    return(currTour,sum(weight)+dist_matrix[currTour[-1]][currTour[0]])

#Places ants on vertices at start of search
def antsOnVerts(N,num_cities):
    antPos = []
    #For each ant randomly assign it a city
    for i in range(0,N):
        antPos.append(random.randint(0,num_cities-1))
    return antPos

#Function to calculate next edge
def calculateEdge(vCitys,currentVert,hDes,Probs):
    total = 0
    #Holds probabilites
    Ps = {}
    #For each city in valid citys
    for i in vCitys:
        #Calculate its attractiveness from the probabiliy matrix
        attractiveness = float(Probs[currentVert][i])
        #Add that to the total
        total += attractiveness
        #Add it to the probabilities
        Ps[i] = attractiveness
    r = random.random()
    cumm = 0.0
    #Pick a city using its probabilities
    for p in Ps.keys():
        weight = Ps[p] / total
        if r <= weight + cumm:
            return p
        cumm += weight

#Generates a hDesierability matrix
def hDes():
    #Initally 1, any not updated cities will stay one as it represents the desirability to go from 1 city to itself
    hDes = [[ 1 for a in range(num_cities) ] for b in range(num_cities)]
    #For each row & column
    for i in range(0,len(hDes)):
        for j in range(0,len(hDes[i])):
            #If not the same city 
            if dist_matrix[i][j] != 0:
                #Calculate hDesirability
                hDes[i][j] = (1/dist_matrix[i][j])
    return hDes

#Used to update the probabilities 
def updateProbs(pLevels,hDes):
    #Initally all probabilities are 0 
    Ps = [[ 0.0 for a in range(num_cities) ] for b in range(num_cities)]
    #For each positon in the matrix
    for i in range(0,len(Ps)):
        for j in range(0,len(Ps[i])):
            #Get the pheromones and hDes
            pheromone = float(pLevels[i][j])
            hDesirability = float(hDes[i][j])
            #Calculate P
            p =  float(pow(pheromone,a) * pow(hDesirability,b))
            #If too small can cause floating point error and go to 0 = errors with dividing, so set to small number
            if(p==0.0):
                p = 0.00000000000001
            #Set the probability at that position
            Ps[i][j] = float(p)
    return Ps

def ACO():
    #Set the number of ants
    N = num_cities
    #Get the nearestNeighbour tour and tour cost
    bTour,NN = nearestNeighbour(num_cities,dist_matrix)
    #Set ininital pheromone
    P0 = float(N/NN)
    #P Levels represents the pheromones on each edge
    pLevels = [[ P0 for _ in range(num_cities) ] for _ in range(num_cities)]
    #Get hDes matrix
    hDesirability = hDes()
    #Set best tour, which holds the actual tour as well as tour cost
    bestTour = [bTour,NN]
    #Starting position will be the inital positions of all ants
    startingPos= antsOnVerts(N,num_cities)
    #Number of max iterations, currently set to 0 so as to stop by time not by iterations
    t = 0
    max_it = 1000
    #Gets start time, useful for ensuring completion < 1 minute
    startTime = time.time();
    #Loop until we run out of time
    while t<max_it:
        #Update all probabilities
        probs = updateProbs(pLevels,hDesirability)
        #Create a new updated pheromones table, which will be the pheromones of t+1 iteration
        pUpdated = [[ (1-rho)*pLevels[x][y] for x in range(num_cities) ] for y in range(num_cities)]
        #Holds min tour for this iteration
        minTour = [bTour,NN]
        #For each ant
        for k in range(0,N):
            #Valid citys initially holds all cities
            validCitys = {i for i in range(num_cities) }
            #Check we havent gone over time
            if time.time() - startTime > 58:
                note = "Ants:"+str(N)+ " Iterations: : " +str(t) + " Alpha: "+str(a) + " Beta: "+ str(b) + " Rho: "+ str(rho)
                return bestTour[0],bestTour[1],note
            #Cost of the tour 
            cost = 0
            #The tour the ant takes
            antTour = [startingPos[k]]
            #Current position is last visited city
            currPos = antTour[-1]
            #Remove this city from the valid citys
            validCitys.remove(currPos)
            #While the we still have citys to visit
            while(len(validCitys) > 0):
                #If we only have 1 city remaining, visit it
                if len(validCitys) == 1:
                    newVert = validCitys.pop()
                else:
                    #Calculate the edge to travel on
                    newVert = calculateEdge(validCitys,currPos,hDesirability,probs)
                    #Remove this new city from the list of valid citys
                    validCitys.remove(newVert)
                #Add the cost
                cost += dist_matrix[currPos][newVert]
                #Add the city to the tour
                antTour.append(newVert)
                #Update the current positon of the ant
                currPos = newVert
            #Add the cost of the last in the tour to the first
            cost += dist_matrix[currPos][antTour[0]]
            #If the cost is smaller than the best of the iteration
            if cost < minTour[1]:
                minTour = antTour,cost
            #Between every 2 cities in the tour 
            for j in range(0,len(antTour)-1):
                #City num 1
                num1 = antTour[j]
                #City num 2 
                num2 = antTour[j+1]
                #Add the 1/cost to the edge in updated pheromones, adding to the both directions to keep symmetric
                pUpdated[num1][num2] += 1/cost
                pUpdated[num2][num1] += 1/cost
        #If the min tour of the iteration is lower than the best tour found so far
        if minTour[1] < bestTour[1]:
            bestTour[0],bestTour[1] = minTour[0],minTour[1]
        #The pheromone levels are now the updated ones
        pLevels = copy.copy(pUpdated)
        #Iterate the amount of iterations
        t += 1
    note = "Ants:"+str(N)+ " Iterations: : " +str(t) + " Alpha: " +  str(a) + " Beta: " +str(b) + " Rho: " +str(rho)
    return bestTour[0],bestTour[1],note
        
            
a = 1
b = 5
rho = 0.5
tour,tour_length,added_note = ACO()






############
############ YOUR CODE SHOULD NOW BE COMPLETE AND WHEN EXECUTION OF THIS PROGRAM 'skeleton.py'
############ REACHES THIS POINT, YOU SHOULD HAVE COMPUTED A TOUR IN THE RESERVED LIST VARIABLE 'tour', 
############ WHICH HOLDS A LIST OF THE INTEGERS FROM {0, 1, ..., 'num_cities' - 1}, AND YOU SHOULD ALSO
############ HOLD THE LENGTH OF THIS TOUR IN THE RESERVED INTEGER VARIABLE 'tour_length'.
############

############
############ YOUR TOUR WILL BE PACKAGED IN A TOUR FILE OF THE APPROPRIATE FORMAT AND THIS TOUR FILE,
############ WHOSE NAME WILL BE A MIX OF THE NAME OF THE CITY FILE, THE NAME OF THIS PROGRAM AND THE
############ CURRENT DATA AND TIME. SO, EVERY SUCCESSFUL EXECUTION GIVES A TOUR FILE WITH A UNIQUE
############ NAME AND YOU CAN RENAME THE ONES YOU WANT TO KEEP LATER.
############

############
############ DO NOT TOUCH OR ALTER THE CODE BELOW THIS POINT! YOU HAVE BEEN WARNED!
############

flag = "good"
length = len(tour)
for i in range(0, length):
    if isinstance(tour[i], int) == False:
        flag = "bad"
    else:
        tour[i] = int(tour[i])
if flag == "bad":
    print("*** error: Your tour contains non-integer values.")
    sys.exit()
if isinstance(tour_length, int) == False:
    print("*** error: The tour-length is a non-integer value.")
    sys.exit()
tour_length = int(tour_length)
if len(tour) != num_cities:
    print("*** error: The tour does not consist of " + str(num_cities) + " cities as there are, in fact, " + str(len(tour)) + ".")
    sys.exit()
flag = "good"
for i in range(0, num_cities):
    if not i in tour:
        flag = "bad"
if flag == "bad":
    print("*** error: Your tour has illegal or repeated city names.")
    sys.exit()
check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + dist_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + dist_matrix[tour[num_cities - 1]][tour[0]]
if tour_length != check_tour_length:
    flag = print("*** error: The length of your tour is not " + str(tour_length) + "; it is actually " + str(check_tour_length) + ".")
    sys.exit()
print("You, user " + my_user_name + ", have successfully built a tour of length " + str(tour_length) + "!")

local_time = time.asctime(time.localtime(time.time()))
output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
output_file_time = output_file_time.replace(" ", "0")
script_name = os.path.basename(sys.argv[0])
if len(sys.argv) > 2:
    output_file_time = sys.argv[2]
output_file_name = script_name[0:len(script_name) - 3] + "_" + input_file[0:len(input_file) - 4] + "_" + output_file_time + ".txt"

f = open(output_file_name,'w')
f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + "),\n")
f.write("ALGORITHM CODE = " + algorithm_code + ", NAME OF CITY-FILE = " + input_file + ",\n")
f.write("SIZE = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + ",\n")
f.write(str(tour[0]))
for i in range(1,num_cities):
    f.write("," + str(tour[i]))
f.write(",\nNOTE = " + added_note)
f.close()
print("I have successfully written your tour to the tour file:\n   " + output_file_name + ".")
    
    











    


