#take an image and creat new image with solved maze
from PIL import Image
import glob
import os

maze_name = 'maze2.png'
dir_mazes = '/Users/amit/Documents/python/pathFinder/mazes/'
start_color = (205, 220, 57, 255) #rgb start pixel color
end_color = (229, 57, 53, 255) #rgb end pixel color
wall_color = (121, 85, 72, 255)#rgb wall pixel color

def Creat_Maze(maze_image):
    maze = []
    width, height = maze_image.size
    pixels = maze_image.load()
    for i in range(width):
        maze.append([])
        for j in range(height):
            print(pixels[i,j])
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

maze_image = get_mazeJPG(maze_name)
maze , start_pixel, end_pixel = Creat_Maze(maze_image)
print(astar(maze,start_pixel,end_pixel))
