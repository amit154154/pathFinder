#take an image and creat new image with solved maze
from PIL import Image
import glob
import os
import numpy as np
import tqdm


maze_name = 'maze3.png'
dir_mazes = '/Users/amit/Documents/python/pathFinder/mazes/'
dir_solve_mazes = '/Users/amit/Documents/python/pathFinder/solves_mazes/'
start_color = (211, 47, 47, 255) #rgb start pixel color
end_color = (255, 235, 59, 255) #rgb end pixel color
wall_color = (121, 85, 72, 255)#rgb wall pixel color
solve_color = (30,255,255,255)#rgb solve way pixel color

def Creat_Maze(maze_image):
    maze = []
    width, height = maze_image.size
    pixels = maze_image.load()
    for i in range(width):
        maze.append([])
        for j in range(height):
            if pixels[i,j] == start_color:
                start_pixel = (i,j)
            elif pixels[i,j] == end_color:
                end_pixel = (i,j)
            if pixels[i,j] == wall_color:
                maze[i].append(1)
            else:
                maze[i].append(0)
    return maze,start_pixel,end_pixel

def get_mazeJPG(maze_name):
        return Image.open(dir_mazes + maze_name)

#Node Class For each pixel
class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

def Creat_Solve(maze,start,end,solve,imageName):
    for pos in solve:
        maze[pos[0]][pos[1]] = 4
    maze[start[0]][start[1]] = 2
    maze[end[0]][end[1]] = 3

    for row in range(len(maze)):
        for pos in range(len(maze[0])):
            if maze[row][pos] == 2:
                maze[row][pos] = start_color
            elif maze[row][pos] == 3:
                maze[row][pos] = end_color
            elif maze[row][pos] == 4:
                maze[row][pos] = solve_color
            elif maze[row][pos] == 1:
                maze[row][pos] = wall_color
            else:
                maze[row][pos] = (255,255,255,255)

    array = np.array(maze, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save(dir_solve_mazes + imageName)

def Solves_All():
   mazes_path = glob.glob(dir_mazes + '*.png')
   for maze_path in tqdm.tqdm(mazes_path):
       solve_name = maze_path.split('/')[-1].split('.')[0] + '_solve.png'
       maze_image = Image.open(mazes_path)
       maze, start_pixel, end_pixel = Creat_Maze(maze_image)
       Creat_Solve(maze, start_pixel, end_pixel, astar(maze, start_pixel, end_pixel), solve_name)


maze_image = get_mazeJPG(maze_name)
maze , start_pixel, end_pixel = Creat_Maze(maze_image)
Creat_Solve(maze , start_pixel, end_pixel,astar(maze , start_pixel, end_pixel),'solve3.png')
Solves_All()