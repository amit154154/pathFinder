import kivy
from kivy.app import App
from kivy.graphics import Line, InstructionGroup,Color
from kivy.uix.widget import Widget
kivy.require('1.11.1')
from kivy.config import Config
from kivy.uix.button import Button


cols = []
rows = 10
columns = 10
col_size = 15
Start_cell = False
End_cell = False
width = rows*col_size
height = columns*col_size
widget = None
Config.set('graphics', 'width', str(width + 150))
Config.set('graphics', 'height', str(height))
touch_mode = 0

#Reast Board look
def ResetBoard():
    global cols,End_cell,Start_cell,touch_mode
    for row in range(rows):
        for col in range(columns):
            draw_x((row,col), (0,0,0,1))
    print_cols()
    cols = []
    init_cols()
    End_cell = False
    Start_cell = False
    touch_mode = 0

#Sort Maze for algoritam
def Sort_Maze(maze):
    sorted_maze =  maze
    for row in range(rows):
        for coloum in range(columns):
            if(maze[row][coloum] == 3 or maze[row][coloum] == 2):
                sorted_maze[row][coloum] = 0
    return sorted_maze

#draw grid
def draw_grid():
    for i in range(rows+1):
        for j in range(columns+1):
            draw_line(((i*col_size,height),(i*col_size,0)),(1,1,1,1))
            draw_line(((0,j*col_size),(width,j*col_size)),(1,1,1,1))

#print cols in table formant
def print_cols():
    print(cols[0])
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
          for row in cols]))

#init cols, reset all
def init_cols():
    for i in range(rows):
        cols.append([])
        for j in range(columns):
            cols[i].append(0)

#draw line from two points
def draw_line(pos,color):
    with widget.canvas:
        Color(color[0],color[1],color[2],color[3])
    widget.ig = InstructionGroup()
    widget.line = Line(points=[pos[0][0], pos[0][1],pos[1][0],pos[1][1]])
    widget.ig.add(widget.line)
    widget.canvas.add(widget.ig)

#drew x in specific index
def draw_x(pos,color):
    draw_line(((pos[0]*col_size,pos[1]*col_size),((pos[0]+1)*col_size,(pos[1]+1)*col_size)),color)
    draw_line(((pos[0]*col_size,(pos[1]+1)*col_size),((pos[0]+1)*col_size,pos[1]*col_size)),color)

#select index by pos in pixels
def pixels_to_indexs(pos):
    return (int(pos[0]/col_size), int(pos[1]/col_size))



class TouchInput(Widget):
    def __init__(self, **kwargs):
        super(TouchInput, self).__init__(**kwargs)

    def on_touch_down(self,touch):
        global touch_mode, Start_cell,End_cell,cols
        indexs = pixels_to_indexs(touch.pos)
        try:
            col = cols[indexs[0]][indexs[1]]
            if (col == 0) and touch_mode!=2 and touch_mode != 3:
                touch_mode = 0
                cols[indexs[0]][indexs[1]] = 1
                draw_x(indexs, (1, 1, 1, 1))
            elif (col == 1):
                touch_mode = 1
                cols[indexs[0]][indexs[1]] = 0
                draw_x(indexs, (0, 0, 0, 1))
            elif(touch_mode == 2):
                if Start_cell==False:
                    cols[indexs[0]][indexs[1]] = 2
                    Start_cell = True
                    draw_x(indexs,[0,1,0,1])
                    find_start(cols)
                elif Start_cell and cols[indexs[0]][indexs[1]] == 2:
                    touch_mode = 0
                    cols[indexs[0]][indexs[1]] = 0
                    Start_cell = False
                    draw_x(indexs, [0, 0, 0, 1])
            elif (col == 1):
                touch_mode = 1
                cols[indexs[0]][indexs[1]] = 0
                draw_x(indexs, (0, 0, 0, 1))

            elif(touch_mode == 2):
                if Start_cell==False:
                    cols[indexs[0]][indexs[1]] = 2
                    Start_cell = True
                    draw_x(indexs,[0,1,0,1])
                elif Start_cell and cols[indexs[0]][indexs[1]] == 2:
                    touch_mode = 1
                    cols[indexs[0]][indexs[1]] = 0
                    Start_cell = False
                    draw_x(indexs, [0, 0, 0, 1])

            elif(touch_mode == 3):
                if End_cell==False:
                    cols[indexs[0]][indexs[1]] = 3
                    End_cell = True
                    draw_x(indexs,[1,0,0,1])
                    touch_mode = 0
                elif End_cell and cols[indexs[0]][indexs[1]] == 3:
                    touch_mode = 3
                    cols[indexs[0]][indexs[1]] = 0
                    End_cell = False
                    draw_x(indexs, [0, 0, 0, 1])
        except:
            if  width<touch.pos[0] and touch.pos[0]<width+150 and touch.pos[1]> height-height/4 and touch.pos[1]<height:
                touch_mode = 2

            if  width<touch.pos[0] and touch.pos[0]<width+150 and touch.pos[1]> height-height/2 and touch.pos[1]<height-height/4:
                touch_mode = 3

            if  width<touch.pos[0] and touch.pos[0]<width+150 and touch.pos[1]> height-height/4 * 3 and touch.pos[1]<height-height/2:
                ResetBoard()

            if  width<touch.pos[0] and touch.pos[0]<width+150 and touch.pos[1]> 0 and touch.pos[1]<height-height/4 * 3:
                copy = cols.copy()
                start = find_start(copy)
                end = find_end(copy)
                path = astar(Sort_Maze(copy),start,end)
                draw_Way(path,[0,1,0,1])



        return touch.pos

    def on_touch_move(self, touch):
        indexs = pixels_to_indexs(touch.pos)
        try:
            if touch_mode == 1 and cols[indexs[0]][indexs[1]] == 1:  # obstical
                cols[indexs[0]][indexs[1]] = 0
                draw_x(indexs, (0, 0, 0, 1))

                # draw_rectangle((3,3), (1, 0, 0, 1))
            elif touch_mode == 0 and cols[indexs[0]][indexs[1]] == 0:  # delete
                cols[indexs[0]][indexs[1]] = 1
                draw_x(indexs, (1, 1, 1, 1))
                # draw_rectangle(indexs, (1, 1, 1, 1))
        except:
            pass


class app(App):
    def build(self):
        global widget
        widget = TouchInput()
        init_cols()
        draw_grid()
        Color(1, 0, 0, 1)


        widget.add_widget(Button_Widget('StartTouch',(width,height - height/4),2))
        widget.add_widget(Button_Widget('EndTouch',(width,height - height/2),3))
        widget.add_widget(Button_Widget('Reset',(width,height - height/4 * 3),0))
        widget.add_widget(Button_Widget('Solve',(width,0),0))
        return widget

#Button Widghet
class Button_Widget(Widget):
    def __init__(self,text,position, touchmode ,**kwargs):
        super(Button_Widget, self).__init__(**kwargs)
        btn1 = Button(text=text, pos= position, size = (150,height/4))
        btn1.bind(on_press=self.callback)
        self.touch_mode = touchmode
        self.add_widget(btn1)

    def callback(self, instance):
        global touch_modebutt
        touch_mode = self.touch_mode

#Node Class For each Coloum
class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

#astar algoritam
def astar(maze, start, end):
    # Create start and end node
    print(maze)
    print(start)
    print(end)
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


#find the start pos in the maze
def find_start(maze):
    for i in range(rows):
        for j in range(columns):
            if(maze[i][j] == 2):
                return (i,j)

#find the end pos in the maze
def find_end(maze):
    for i in range(rows):
        for j in range(columns):
            if(maze[i][j] == 3):
                return (i,j)

#draw way by given the road
def draw_Way(moves,color):
    print(moves)
    for pos in moves:
        draw_x((pos[0],pos[1]), color)


if __name__ == '__main__':
  app().run()

