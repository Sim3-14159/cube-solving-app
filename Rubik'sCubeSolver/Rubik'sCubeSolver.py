#! /usr/bin/env python
import tkinter as tk
from tkinter import messagebox as msgBx
import kociemba
import time
import sys
import os
from PIL import Image, ImageTk


# constant positions in the cube:
ULB = (0, 36, 47)
URB = (2, 11, 45)
ULF = (6, 18, 38)
URF = (8, 20, 9)
DLF = (24, 27, 44)
DRF = (26, 29, 15)
DLB = (30, 33, 42)
DRB = (32, 35, 17)

CORNERS = (ULB, URB, ULF, URF, DLF, DRF, DLB, DRB)


UL = (3, 37)
UF = (7, 19)
UR = (5, 10)
UB = (1, 46)
FL = (23, 39)
FR = (21, 12)
BL = (50, 41)
BR = (48, 14)
DL = (27, 43)
DF = (31, 25)
DR = (29, 16)
DB = (33, 52)

EDGES = (UL, UF, UR, UB, FL, FR, BL, BR, DL, DF, DR, DB)

storage_file = "Rubik'sCubeSolverMode.txt"
if not os.getcwd().endswith("Rubik'sCubeSolver"):
    os.chdir(os.path.expanduser('~'))
    os.chdir("Rubik'sCubeSolver")
    

class CubeSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3x3 Solver")
        self.canvas = tk.Canvas(root, bg="#dddddd")
        self.canvas.pack(fill='both', expand=True)

        self.base_width = 800
        self.base_height = 600
        self.scaling_factor = 1.0

        self.cube_buttons = []
        self.selected_color = None
        self.widgets = []
        self.canvas_windows = {}
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'white']
        with open(storage_file) as f:
            self.mode = f.read().strip()
        
        self.color_box = tk.Label(self.canvas, background='darkgrey', height=20,
                                  relief='groove', border=3)
        self.widgets.append((self.color_box, 40, 30, 80, 260))

        self.build_ui()
        self.redraw_ui()
        
        # resizing with window
        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<Control-q>", exit)
        
        # keyboard shortcuts
        getbig = lambda e: self.root.geometry(
            f"{int(self.root.winfo_width()*1.1)}x{int(self.root.winfo_height()*1.1)}")
        getsmall = lambda e: self.root.geometry(
            f"{int(self.root.winfo_width()*0.9)}x{int(self.root.winfo_height()*0.9)}")
        movexback = lambda e: self.root.geometry(
            f"{int(self.root.winfo_width()*0.9)}x{self.root.winfo_height()}")
        movexforward = lambda e: self.root.geometry(
            f"{int(self.root.winfo_width()*1.1)}x{self.root.winfo_height()}")
        moveydown = lambda e: self.root.geometry(
            f"{self.root.winfo_width()}x{int(self.root.winfo_height()*1.1)}")
        moveyup = lambda e: self.root.geometry(
            f"{self.root.winfo_width()}x{int(self.root.winfo_height()*0.9)}")
        
        # control-plus may be control-equal on some systems
        self.root.bind("<Control-equal>", getbig) 
        self.root.bind("<Control-plus>", getbig)
        self.root.bind("<Control-minus>", getsmall)
        self.root.bind("<Control-Right>", movexforward)
        self.root.bind("<Control-Left>", movexback)
        self.root.bind("<Control-Up>", moveyup)
        self.root.bind("<Control-Down>", moveydown)
        
        menugetbig = lambda: self.root.geometry(
            f"{int(self.root.winfo_width()*1.1)}x{int(self.root.winfo_height()*1.1)}")
        menugetsmall = lambda: self.root.geometry(
            f"{int(self.root.winfo_width()*0.9)}x{int(self.root.winfo_height()*0.9)}")
        
        showaboutinfo = lambda: msgBx.showinfo('About', '3x3 Solver is an app developed '
'by Simyon Hein.\n\nWhat makes this app different than other similar programs is it\'s '
'ability to be easily changed and run on any device with Python installed.')
        
        showhelpinfo = lambda: msgBx.showinfo('Help', 'Click on a colored rectangle on the'
' left side of the screen to select a color, then click on an uncolored '
'square on the 2D Rubik\'s Cube in correspondence with the stickers on your cube. '
'\n\nThe front side is in the middle of the cube.')
        
        self.menubar = tk.Menu(root, activebackground='grey')
        
        self.filemenu = tk.Menu(self.menubar, tearoff=0, activebackground='grey')
        self.filemenu.add_command(label='Quit         (Ctrl+q)', command=exit)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        
        self.viewmenu = tk.Menu(self.menubar, tearoff=0, activebackground='grey')
        self.viewmenu.add_command(label='Increase Size        (Ctrl++)', command=menugetbig)
        self.viewmenu.add_command(label='Decrease Size        (Ctrl+-)', command=menugetsmall)
        self.menubar.add_cascade(label='View', menu=self.viewmenu)
        
        self.prefmenu = tk.Menu(self.menubar, tearoff=0, activebackground='grey')
        self.modemenu = tk.Menu(self.prefmenu, tearoff=0, activebackground='grey')
        self.modemenu.add_command(label='Dark Mode', command=self.darkmode)
        self.modemenu.add_command(label='Light Mode', command=self.lightmode)
        self.modemenu.add_command(label='Auto', command=self.setautomode)
        self.prefmenu.add_cascade(label='Mode', menu=self.modemenu)
        self.menubar.add_cascade(label='Prefrences', menu=self.prefmenu)
        
        self.helpmenu = tk.Menu(self.menubar, tearoff=0, activebackground='grey')
        self.helpmenu.add_command(label='About', command=showaboutinfo)
        self.helpmenu.add_command(label='How to Use', command=showhelpinfo)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)
        
        self.root.config(menu=self.menubar)

        self.mode_is_auto = False
        self.auto_mode()  # Start the loop
        
        if self.mode == 'light':
            self.lightmode()
        elif self.mode == 'dark':
            self.darkmode()
        else:
            self.mode_is_auto = True
        
    def darkmode(self):
        self.canvas.config(bg='#444444')
        self.status_label.config(bg='#222222', fg='white')
        dark = '#666666'
        self.menubar.config(bg=dark)
        self.prefmenu.config(bg=dark)
        self.filemenu.config(bg=dark)
        self.viewmenu.config(bg=dark)
        self.modemenu.config(bg=dark)
        self.helpmenu.config(bg=dark)
        self.mode_is_auto = False
        with open(storage_file, 'w') as f:
            f.write('dark')
        
    def lightmode(self):
        self.canvas.config(bg='#dddddd')
        self.status_label.config(bg='darkgrey', fg='black')
        light = '#aaaaaa'
        self.menubar.config(bg=light)
        self.prefmenu.config(bg=light)
        self.filemenu.config(bg=light)
        self.viewmenu.config(bg=light)
        self.modemenu.config(bg=light)
        self.helpmenu.config(bg=light)
        self.mode_is_auto = False
        with open(storage_file, 'w') as f:
            f.write('light')
    
    def auto_mode(self):
        if self.mode_is_auto:
            the_time = time.localtime().tm_hour
            
            if 6 < the_time < 20:
                self.lightmode()
            else:
                self.darkmode()
            
            with open(storage_file, 'w') as f:
                f.write('auto')
            
        self.root.after(100, self.auto_mode) # checks times a second for night mode
        
            
    def setautomode(self):
        self.mode_is_auto = True
        
    
    def build_ui(self):
        for i, color in enumerate(self.colors):
            btn  = tk.Button(self.root, bg=color, width=2, border=3, relief='groove',
                             command=lambda c=color: self.set_color(c))
            
            if color == 'red': btn.config(activebackground='#cc0000')
            elif color == 'orange': btn.config(activebackground='#aa7700')
            elif color == 'yellow': btn.config(activebackground='#bbbb00')
            elif color == 'green': btn.config(activebackground='#006600')
            elif color == 'blue': btn.config(activebackground='#000099')
            elif color == 'white': btn.config(activebackground='#bbbbbb')
                    
            self.widgets.append((btn, 50, 50 + 40 * i, 60, 30))

        self.solve_button = tk.Button(self.root, text="Solve", bg='green', border=5,
                                      command=self.solve_cube, activebackground='darkgreen'
                                      )#activeforeground='lightgreen')
        self.widgets.append((self.solve_button, 50, 500, 100, 50))

        self.status_label = tk.Label(self.root, text="Fill in the cube colors", bg='darkgrey')
        self.widgets.append((self.status_label, 200, 30, 400, 30))

        self.create_cube_faces()


    def create_cube_faces(self):
        face_order = ['U', 'R', 'F', 'D', 'L', 'B']
        face_positions = {
            'U': (3, 0),
            'L': (2, 1),
            'F': (3, 1),
            'R': (4, 1),
            'B': (5, 1),
            'D': (3, 2),
        }

        for face in face_order:
            col, row = face_positions[face]
            for i in range(3):
                for j in range(3):
                    btn = tk.Button(self.root, bg='black', relief='raised', border=3,
                                    command=lambda b=len(self.cube_buttons): self.set_cube_color(b),
                                    activebackground='#444444')
                    x = 10 + (col * 3 + j) * 42
                    y = 110 + (row * 3 + i) * 42
                    self.cube_buttons.append([btn, None])
                    self.widgets.append((btn, x, y, 40, 40))

    def set_color(self, color):
        self.selected_color = color

    def set_cube_color(self, idx):
        if self.selected_color:
            btn, _ = self.cube_buttons[idx]
            btn.config(bg=self.selected_color)
            self.cube_buttons[idx][1] = self.selected_color
    
    def solve_cube(self):
        colors = [color[1] for color in self.cube_buttons]
        if None in colors:
            self.status_label.config(text="Missing colors!")
            msgBx.showwarning("Uncolored stickers", 'Please fill each sticker with a color')
            return
        cube_string = ''.join(c[0].upper() for c in colors)
        facelets = self.color_to_cubestring(cube_string)
        try:
            solution = kociemba.solve(facelets)
            self.status_label.config(text=f"Solution: {solution}")
        except ValueError:
            
            self.status_label.config(text="Invalid scramble!")
            msgBx.showwarning('Invalid Scramble!', 'The scramble you entered is not solvable.')
            '''
            if self._edge_flipped(facelets):
                msgBx.showwarning('Invalid Scramble!', 'It looks like an edge is flipped.')
            elif self._corner_twisted(facelets):
                msgBx.showwarning('Invalid Scramble!', 'It looks like a corner is twisted.')
            else:
                msgBx.showwarning("Invalid Scramble!", 'The scramble you entered is not solvable.')
            '''
            
    def _corner_twisted(self, cubestring):
        total_twist_direction = 0
        twist_values = (0, 1, -1)
        for corner in CORNERS:
            for i in range(3):
                # if the cornner is good (facing up or down)
                if cubestring[corner[i]] == 'U' or cubestring[corner[i]] == 'D':
                    total_twist_direction += twist_values[i]
        
        return total_twist_direction
    
    def _edge_flipped(self, cubestring):
        total_flipped = False
        for edge in EDGES:
            # if the edge is good (facing up, down, left, or right)
            x = cubestring[edge[0]]
            if x == 'U' or x == 'D' or x == 'F' or x == 'B':
                continue
            else:
                total_flipped = not total_flipped
                continue
                    
        return total_flipped
                

    def color_to_cubestring(self, cube_colors):
        topColor = cube_colors[4]
        rightColor = cube_colors[13]
        frontColor = cube_colors[22]
        bottomColor = cube_colors[31]
        leftColor = cube_colors[40]
        backColor = cube_colors[49]

        cubeString = (cube_colors.replace(topColor, 'U')
                      .replace(leftColor, 'L')
                      .replace(frontColor, 'F')
                      .replace(bottomColor, 'D')
                      .replace(rightColor, 'R')
                      .replace(backColor, 'B'))
        return cubeString

    def on_resize(self, event):
        if hasattr(self, "_resize_after_id"):
            self.root.after_cancel(self._resize_after_id)
        self._resize_after_id = self.root.after(100, self.handle_resize)

    def handle_resize(self):
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        width_ratio = width / self.base_width
        height_ratio = height / self.base_height
        new_scale = min(width_ratio, height_ratio)

        if abs(new_scale - self.scaling_factor) > 0.01:
            self.scaling_factor = new_scale
            self.redraw_ui()

    def redraw_ui(self):
        # Create or move canvas windows
        
        for widget, x, y, w, h in self.widgets:
            if not widget.winfo_exists():
                continue
            try:
                font_size = max(9, int(10 * self.scaling_factor))
                
                if widget is self.solve_button:
                    widget.config(font=("Bold", int(font_size*1.5)))
                else:
                    widget.config(font=("Arial", font_size))
                    
            except tk.TclError:
                continue
            sx = x * self.scaling_factor
            sy = y * self.scaling_factor
            sw = w * self.scaling_factor
            sh = h * self.scaling_factor

            if widget not in self.canvas_windows:
                window_id = self.canvas.create_window(sx, sy, width=sw, height=sh, window=widget, anchor='nw')
                self.canvas_windows[widget] = window_id
            else:
                self.canvas.coords(self.canvas_windows[widget], sx, sy)
                self.canvas.itemconfig(self.canvas_windows[widget], width=sw, height=sh)



def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.minsize(600, 400)
    
    path = os.path.dirname(os.path.abspath(__file__))
    icon = Image.open(path + "/RubiksCube.jpg")
    icon = ImageTk.PhotoImage(icon)
    root.iconphoto(True, icon)

    app = CubeSolverApp(root)

    root.mainloop()

main()

