# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: 

### Naked Twins
Naken Twins techniques states that, if in a unit(rows,colums, 3X3 square, 2 diagonals) two different boxes are occupied by a same number of length 2(for example 23), then the two values (2, 3) are blocked between these two boxes in the unit, which implies that no other boxes in the unit can hold the values or hold the possibility of having the values (2, 3) in them. 

For example if we have a unit(before naked twins) = [4, 6, 8, 2379, 379, 23, 1, 5, 23], here we can see that [23, 23] are naked twins, and according to the naked twin techniques, we know that now these two values (2, 3) are blocked between the boxes with index 5 and 8. So, we can safely remove values (2, 3) from all the other boxes as the naked twin technique states. So we will be left with the following unit

unit(after first iteration of naked twins) = [4, 6, 8, 79, 79, 23, 1, 5, 23]

We can see this generates another pair of naked twins in the unit [79, 79] but as no other boxes hold these values, so there will be no further change in this unit.

### Constraint propogation in naked twins

#### Constraint Propogation
To put it in a more subtle way, let's assume we have three linear equations in variables (x, y, z) say (e1, e2, e3), and if we have to find a value of (x, y, z) that satisfies all the three equations (e1, e2, e3), the solution that we will get will lie in a feasible region which satifies all the three equations (e1, e2, e3). This simply means that we are trying to satisfy a set of constrains which are imposed by the three equations on the three variables (x, y, z). So, this is what constraint satisfaction means. 

Now, I will take liberty in defining constraint propogation. Now suppose in Sudoku we have multiple units, which we work with, and every unit is exposed to the same set of constraints, for example every unit should contain the number 1 to 9, only once, and there are several other constraints which we can introduce like naked twins. So, when we want to propogate a set of constraints on several different units, untill all the units satisfy that constrain(in case of sudoku when the board stope observing any changes anymore), we call it constraint propogation.  

#### Constraint propogation in naked twins problem
In naked twin we know what constraint do we want to satify for every unit?, the constraint is if in a unit(rows,colums, 3X3 square, 2 diagonals) two different boxes are occupied by a same number of length 2(for example 23), then the two values (2, 3) are blocked between these two boxes in the unit, which implies that no other boxes in the unit can hold the values or hold the possibility of having the values (2, 3) in them. We have defined the constraint satisfaction problem of naked twins, now if we want to propogate this constraint through all the units of Sudoku, and make sure we resolve all the naked twins in the board till the board stops observing any changes anymore. This is how we will solve naked twins problem using constraint propagation, by propogating the constraint of naked twins to all the units of the board, till the board stops changing anymore.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A:

#### Constraint Propogation
To put it in a more subtle way, let's assume we have three linear equations in variables (x, y, z) say (e1, e2, e3), and if we have to find a value of (x, y, z) that satisfies all the three equations (e1, e2, e3), the solution that we will get will lie in a feasible region which satifies all the three equations (e1, e2, e3). This simply means that we are trying to satisfy a set of constrains which are imposed by the three equations on the three variables (x, y, z). So, this is what constraint satisfaction means. 

Now, I will take liberty in defining constraint propogation. Now suppose in Sudoku we have multiple units, which we work with, and every unit is exposed to the same set of constraints, for example every unit should contain the number 1 to 9, only once, and there are several other constraints which we can introduce like naked twins. So, when we want to propogate a set of constraints on several different units, untill all the units satisfy that constrain(in case of sudoku when the board stope observing any changes anymore), we call it constraint propogation.  

#### Diagonal Sudoku
The only significant difference Diagonal Sudoku has from normal Sudoku is the fact that it has two additional units(two diagonals) which need to satify the constraints too and besides that everything remains the same. 

#### Constrain Propagation in Diagonal Sudoku
Constraints on Diagonal Sudoku

Units = unit in normal Sudoku + two diagonal units

1) Every unit can only have values 1 to 9 once.
2) Eliminate(applied on peers)
3) Only Choice(applied on units)
4) Naked Twins(applied on units)

For applying constaint propagation in Diagonal Sudoku, we just need to apply these four constrains on all units and peers of diagonal sudoku, and keep iterating through it, till we have a solution to the problem. This is how constraint propagation is applied on diagonal sudoku. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.