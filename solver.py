#This is a project made in my AI course, so thats why there are some comments regarding that

#Project 2: Sudoku Solver
#CISC 481: AI
#Miles Phillips, due on 4/19/22, with 3 day grace period (4/22)

#First things first, let us declare what a CSP object is, and the types of things that come along with
#it (ie functions, vars, etc, similar to nodes from the last project)
class CSP():
    import math #used for the fethcing of rows/columns
    #The three components of any CSP are the set of variables, the domains, and the constraints
    def __init__(self, puzzle, constraints): 
        self.puzzle = puzzle #The current state of the puzzle we are attempting to solve, these are the variables we are working with
        self.constraints = constraints #Give the constraints for this given CSP
        self.varsList = self.getVars()
        self.domains =  self.getDomains(self.varsList)#The default domain of every empty space will be the size of one side of the square
        self.arcs = self.getArcs()
    #Let us have a function to generate a mapping for all of the variables in puzzle
    def getVars(self):
        i = 0
        varList = []
        for x in self.puzzle: #Iterate thru the rows
            j = 0
            for y in self.puzzle[i]: #Iterate thru cols
                var = (10 * (i + 1)) + (j + 1) #This will act as a numbering system, with the first digit repping row, second reepping col
                varList.append(var)
                j = j + 1 #Increment col count
            i = i + 1 #Increment row count
        return varList #List of integers to identify each cell in the sudoku
    #Generates/gets all the domains for each space on the board
    def getDomains(self, vars):
        domains = [] #A list of domains, with two elements, a variable indicator and a list repping the domain
        for x in vars:
            currDomain = []
            row = self.math.floor(x / 10) #Tens place
            col = x % 10 #Ones place
            #Subtract one from each to get the appropriate array index (we start at 0)
            row = row - 1
            col = col - 1
            #If there is a value already in this space, the domain should be a singular number
            if(self.puzzle[row][col] != None):
                currDomain = [self.puzzle[row][col]]
            else:
                for i in range(1, len(self.puzzle) + 1): #Generate a list of numbers from 1 to the length of the puzzle
                    currDomain.append(i)
            domains.append([x, currDomain]) #Append to the list of domains the info needed
        return domains
    #Returns the domain list based on the cell number you give it (11, 12, etc... 99)
    def domain(self, cell):
        #Parse thru the domains we just genned
        dom = []
        for x in self.domains:
            if cell == x[0]:
                dom = x[1]
        return dom
    #Change the domain based on the cell 
    def alterDomain(self, cell, val):
        #Parse thru the domains
        for x in self.domains:
            if cell == x[0]:
                x[1].remove(val) #Remove once we get to the cell we wanted to edit
    #Give a domain to a specific list
    def setDomain(self, cell, val):
        #Parse thru the domains
        for x in self.domains:
            if cell == x[0]:
                x[1] = val #Set the domain to the passed val
    #Let us generate some arcs (edges) for each variable, based on the constraints file given and generated
    def getArcs(self):
        arcs = set() #Set of tuple keys defined within the constraints
        for con in self.constraints:
            arcs.add(con)
            inverse = con[::-1] #Inverse the tuple key
            arcs.add(inverse)
        return arcs
    #Get all of the neighbors (based on the constraints) of a given cell
    def neighbors(self, cell, removal):
        currNeighbors = []
        cellString = 'C' + str(cell) #Convert cell # to a string used in the data structure
        #Grab each tuple identifier for the constraints
        for con in self.constraints:
            #Check for constraints involving this cell
            if (con[0] == cellString):
                #convert last two digits to an int
                currStr = con[1][1::] 
                currVar = int(currStr)
                #Check if this is the one we are removing from the neighbors
                if(removal != currVar):
                    currNeighbors.append(currVar) #Add this neighbor to the arcs
            if (con[1] == cellString):
                #convert last two digits to an int
                currStr = con[0][1::]
                currVar = int(currStr)
                #Check if this is the one we are removing from the neighbors
                if(removal != currVar): 
                    currNeighbors.append(currVar) #Add this neighbor to the arcs
        return currNeighbors
    #Check the constraint given two spaces, a val for the first, and a domain for the second
    #Return a boolean, true if no constraint can be sated
    def checkConstraint(self, spacei, spacej, val, d):
        notPossible = True
        iString = 'C' + str(spacei) #Convert cell # to a string used in the data structure
        jString = 'C' + str(spacej) #Convert cell # to a string used in the data structure
        #If no value of y in domain of xj sates the constraints between two vars
        for con in self.constraints:
            #Check for a constraint on (spacei, spacej)
            if(con == (iString, jString)):
                currCon = self.constraints[con]
                #Now check the domains against the constraint
                for x in d:
                    for c in currCon:
                        if([val, x] == c):
                            notPossible = False
            #Check for a constraint on (spacej, spacei)
            if(con == (jString, iString)):
                currCon = self.constraints[con]
                #Now check the domains against the constraint
                for x in d:
                    for c in currCon:
                        if([x, val] == c):
                            notPossible = False
        return notPossible #Returns true if no solutions can be found between these two

        


#We will represent the puzzles as lists of lists (essentially a 2-D array with None values possible)
#They are represented like that in LISP, so let us represent them as so in python

#This may be bad style, but declaring a variable x to represent "None" in the 2d list allows me
#to visualize the board easier, as everything is lined up vertically this way. This will help in
#ensuring that we get the right answers from our algorithms
x = None

#Base Puzzles to be solved
puzzle1 = [
[7, x, x, 4, x, x, x, 8, 6],
[x, 5, 1, x, 8, x, 4, x, x],
[x, 4, x, 3, x, 7, x, 9, x],
[3, x, 9, x, x, 6, 1, x, x],
[x, x, x, x, 2, x, x, x, x],
[x, x, 4, 9, x, x, 7, x, 8],
[x, 8, x, 1, x, 2, x, 6, x],
[x, x, 6, x, 5, x, 9, 1, x],
[2, 1, x, x, x, 3, x, x, 5]
]

puzzle2 = [
[1, x, x, 2, x, 3, 8, x, x],
[x, 8, 2, x, 6, x, 1, x, x],
[7, x, x, x, x, 1, 6, 4, x],
[3, x, x, x, 9, 5, x, 2, x],
[x, 7, x, x, x, x, x, 1, x],
[x, 9, x, 3, 1, x, x, x, 6],
[x, 5, 3, 6, x, x, x, x, 1],
[x, x, 7, x, 2, x, 3, 9, x],
[x, x, 4, 1, x, 9, x, x, 5]
]

puzzle3 = [
[1, x, x, 8, 4, x, x, 5, x],
[5, x, x, 9, x, x, 8, x, 3],
[7, x, x, x, 6, x, 1, x, x],
[x, 1, x, 5, x, 2, x, 3, x],
[x, 7, 5, x, x, x, 2, 6, x],
[x, 3, x, 6, x, 9, x, 4, x],
[x, x, 7, x, 5, x, x, x, 6],
[4, x, 1, x, x, 6, x, x, 7],
[x, 6, x, x, 9, 4, x, x, 2]
]

#Tougher Puzzles
puzzle4 = [
[x, x, x, x, 9, x, x, 7, 5],
[x, x, 1, 2, x, x, x, x, x],
[x, 7, x, x, x, x, 1, 8, x],
[3, x, x, 6, x, x, 9, x, x],
[1, x, x, x, 5, x, x, x, 4],
[x, x, 6, x, x, 2, x, x, 3],
[x, 3, 2, x, x, x, x, 4, x],
[x, x, x, x, x, 6, 5, x, x],
[7, 9, x, x, 1, x, x, x, x]
]

puzzle5 = [
[x, x, x, x, x, 6, x, 8, x],
[3, x, x, x, x, 2, 7, x, x],
[7, x, 5, 1, x, x, 6, x, x],
[x, x, 9, 4, x, x, x, x, x],
[x, 8, x, x, 9, x, x, 2, x],
[x, x, x, x, x, 8, 3, x, x],
[x, x, 4, x, x, 7, 8, x, 5],
[x, x, 2, 8, x, x, x, x, 6],
[x, 5, x, 9, x, x, x, x, x]
]

#Now we will move onto the actual work of the assignment, as we have the puzzles translated now

#Part 1
#The constraints for part 1 will be included seperately, as with other constraint definitions (like the one the prof gave us)
#See the file sudoku4x4_constraints.py for the constraints. It was largely based upon the constraints file that was given

#Let us declare the minpuzzle given in the writeup
minipuzzle = [
[1, x, x, x],
[x, 2, x, x],
[x, x, 3, x],
[x, x, x, 4]
]

#Now onto fetching the constraints from the file we generated and the one given by the prof
import ast
from lib2to3.pytree import convert #Import for literal_eval

#Fetch the constraints we generated
constraints4x4 = None
with open("sudoku4x4_constraints.py") as constraints_file:
    constraints4x4 = ast.literal_eval(constraints_file.read())

#Fetch the constraints given
constraints9x9 = None
with open("sudoku_constraints.py") as constraints_file:
    constraints9x9 = ast.literal_eval(constraints_file.read())

#Now let's setup the CSP for the 4x4 puzzle that was given
csp4x4 = CSP(minipuzzle, constraints4x4)


#Part 2
#Let use write the revise function, which takes in three inputs: the CSP, and two variables
def revise(csp, xi, xj):
    #Declare a boolean var revised
    revised = False
    #Iterate over each possible value in the domain (starts at a 1-9 range for normal sudoku problems)
    for val in csp.domain(xi):
        #If no value of y in domain of xj sates the constraints between two vars
        #Will be using a helper function inside of csp to determine this conditional
        #as it may be a tad tricky/ugly to do in line here
        if csp.checkConstraint(xi, xj, val, csp.domain(xj)):
            csp.alterDomain(xi, val)
            revised = True
    return revised

#Part 3
#Let us now write the AC-3 function, which takes in one variable: a CSP
def ac3(csp):
    arcQueue = csp.arcs #The initial arcs found within the CSP, defined by the constraints
    while (len(arcQueue) != 0):
        #Fetch the first arc
        arc = arcQueue.pop()
        #Assign spaces, 2 digit numbers to identify them
        spacei = arc[0]
        spacej = arc[1]
        #Convert from strings to ints
        spaceiInt = int(spacei[1::])
        spacejInt = int(spacej[1::])
        #Use our revise function to check if we have revised the domain of xi
        if (revise(csp, spaceiInt, spacejInt)):
            #Fetch the domain for the first space
            domaini = csp.domain(spaceiInt)
            #Check if there are no solutions possible
            if (len(domaini) == 0):
                return False
            #Append new arcs, removinkg spacej from the neighbors
            for spacek in csp.neighbors(spaceiInt, spacejInt):
                spacek = 'C' + str(spacek)
                arcQueue.add((spacek, spacei))
    #if we make it thru the entirety of the arcQueue without failure
    return True

#Part 4
#Let us write minimum remaining values, which takes in 2 variables: a CSP and a set of variable assignments
#Returns the variable with the lowest number of items in the domain
def minRemainingVals(csp, varSet):
    minVar = None
    minDLen = 9999
    #Go thru each variable in the list, checking if it has been assigned already
    assignedList = []
    for tup in varSet:
        var = tup[0] #Fetch the variable ID we are looking at
        assignedList.append(var)
    for var in csp.varsList:
        if(var not in assignedList):
            if(len(csp.domain(var)) < minDLen):
                minVar = var
                minDLen = len(csp.domain(var))
    return minVar

#Part 5
#Let us define some helper functions for the backtrack function

#First lets define something to check for consistency
def isConsistent(csp, variable, val, set):
    consistent = True
    for assign in set: #Go thru each variable assignment in the set
        if val == assign[1] and variable in csp.neighbors(assign[0], None): #Check if theres any conflicts here
            consistent = False
    return consistent


#Let us define the helper function backtrack() for the backtrace search
def backtrack(csp, assignSet):
    #Check if our assignment set is complete (aka same length as the amount of spaces in the puzzle)
    if(len(assignSet) == len(csp.varsList)):
        return assignSet
    #Grab a unassigned variable
    unassignedVar = minRemainingVals(csp, assignSet)
    #The order shouldn't really matter for a sudoku problem
    for value in csp.domain(unassignedVar):
        if isConsistent(csp, unassignedVar, value, assignSet): #use our helper function defined above to help w this
            assignSet.add((unassignedVar, value))
            oldDomain = csp.domain(unassignedVar)
            inferences = ac3(csp) #Use our AC3 function as a inference function
            if (inferences): #If we are maintaining arc consistency with the modifications made
                csp.setDomain(unassignedVar, [value]) #Update the domain of the unassigned var
                result = backtrack(csp, assignSet)
                if (result != "Failure"): #We have found a solution
                    return result
                csp.setDomain(unassignedVar, oldDomain)#Remove the inferences from the CSP by setting the domain to what it once was
            assignSet.remove((unassignedVar, value))
    return "Failure"

#Now let us define the backtracing search, fairly simple
def backtraceSearch(csp):
    assignments = set() #Declare an empty set
    return backtrack(csp, assignments)

#Part 7: Web representation of the assignments we make on each puzzle

#This generates a HTML file with all of the steps included, using the helper function gentable
#takes in the csp, the genned assignment list, and a puzzle name (for naming the HTML file)
def genSteps(csp, assignList, puzName):
    #Generate our table of values that was given initially
    tables = "<h1>" + puzName +" puzzle in HTML</h1> "
    puzzleCopy = csp.puzzle
    step = 0
    tables += genTable(puzzleCopy, step) #Gen the initial table
    #Go thru each assign and gen a table for it
    for assignment in assignList:
        space = assignment[0]
        #Get the placement in the 2D array, as we have before
        import math
        row = math.floor(space / 10) #Tens place
        col = space % 10 #Ones place
        #Subtract one from each to get the appropriate array index (we start at 0)
        row = row - 1
        col = col - 1
        if(puzzleCopy[row][col] == None): #If we are looking at an unassigned cell
            step = step + 1
            puzzleCopy[row][col] = assignment[1]
            tables += genTable(puzzleCopy, step) #Gen the modified table
    
    #Using the html given by the prof, declare our head/style, broken up into multiple lines for readability
    head = '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<title>Some Sudoku Puzzles</title>\n'
    head = head + '<style>\n'
    head = head + 'table {border: 3px solid black;border-collapse: collapse;}\ntr {padding: 0;}\n'
    head = head + 'td {width: 64px;height: 64px;padding: 0;border: 1px solid gray;text-align: center;vertical-align: center;font-size: 1.5em;}'
    head = head + 'tr.box-bottom td {border-bottom: 3px solid black;}'
    head = head + 'td.box-side {border-right: 3px solid black;}'
    head = head + '</style></head>'

    #Put all of our stuff together
    resultingHTML = head + tables
    #Write to a file, returning the filename
    filename = "sudoku" + puzName + ".html" #Generating a filename for this HTML
    htmlFile = open(filename, "w")
    htmlFile.write(resultingHTML)
    return filename    


def genTable(puzzle, step):
    if(step != 0): #For every step we are assigning
        gennedTable = "<h2>Step " + str(step) + "</h2>\n"
    else: #For the initial Step
        gennedTable = "<h2>Initial Puzzle</h2>\n"
    gennedTable += "<table>\n"
    #Determine which boxes need to have bottoms and which ones need to have sides
    puzSize = len(puzzle)
    import math
    boxSize = int(math.sqrt(puzSize)) #Calculate the size of every box
    #Iterate thru our puzzle to render it
    i = 0
    for x in puzzle:
        gennedTable += "\n"
        if ((i + 1) % boxSize) == 0: #if we are at a local that needs a 
            gennedTable += '<tr class="box-bottom">\n'
        else:
            gennedTable += '<tr>\n'
        j = 0
        for y in puzzle[i]:
            if ((j + 1) % boxSize) == 0:
                gennedTable+= '<td class="box-side">%s</td>' % cellString(y)
            else:
                gennedTable+= '<td>%s</td>' % cellString(y)
            j = j + 1
        gennedTable += '\n</tr>'
        i = i + 1
    gennedTable += "</table>"
    return gennedTable

#This helps in representing the 
def cellString(val):
    if val == None:
        return ""
    else:
        return str(val)
#Lets do some main function stuff
def main():
    print("I will only be showing a solution for our 4x4 CSP in the terminal, as the others get a bit long, as they have 81 variables")
    print("The first double digit number in the tuple is the coordinates (row, col), and the second digit is the value assigned there by algorithm")
    print("Solution for 4x4 CSP:")
    assignList4x4 = backtraceSearch(csp4x4)
    print(assignList4x4)
    csp9x9puz1 = CSP(puzzle1, constraints9x9)
    csp9x9puz2 = CSP(puzzle2, constraints9x9)
    csp9x9puz3 = CSP(puzzle3, constraints9x9)
    csp9x9puz4 = CSP(puzzle4, constraints9x9)
    csp9x9puz5 = CSP(puzzle5, constraints9x9)
    print("Genning Assign List for Puzzle 1...")
    assignList1 = backtraceSearch(csp9x9puz1)
    print("Genning Assign List for Puzzle 2...")
    assignList2 = backtraceSearch(csp9x9puz2)
    print("Genning Assign List for Puzzle 3...")
    assignList3 = backtraceSearch(csp9x9puz3)
    print("Genning Assign List for Puzzle 4...")
    assignList4 = backtraceSearch(csp9x9puz4)
    print("Genning Assign List for Puzzle 5...")
    assignList5 = backtraceSearch(csp9x9puz5)
    
    #Now lets move onto repping this in HTML, this will overwrite any old HTMOL files we were using in the past
    html4x4 = genSteps(csp4x4, assignList4x4, "4x4")
    html9x9puz1 = genSteps(csp9x9puz1, assignList1, "9x9Puzzle1")
    html9x9puz2 = genSteps(csp9x9puz2, assignList2, "9x9Puzzle2")
    html9x9puz3 = genSteps(csp9x9puz3, assignList3, "9x9Puzzle3")
    html9x9puz4 = genSteps(csp9x9puz4, assignList4, "9x9Puzzle4")
    html9x9puz5 = genSteps(csp9x9puz5, assignList5, "9x9Puzzle5")

    print("Opening web representations of each puzzle... You may be prompted to open the HTML files by your device...")
    print("Alternatively, you can change the URL to be the representation you wish to see (i.e. 'sudoku4x4.html, 'sudoku9x9Puzzle1.html', etc)'")
    import webbrowser
    webbrowser.open(html4x4)
    webbrowser.open(html9x9puz1)
    webbrowser.open(html9x9puz2)
    webbrowser.open(html9x9puz3)
    webbrowser.open(html9x9puz4)
    webbrowser.open(html9x9puz5)

#Call the main method
main()