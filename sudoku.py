import tkinter as tk 
from tkinter import messagebox, filedialog 
import time
import random 
import copy
import pickle

class SudokuGenerator: 
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
                
        return True
    
    def solve(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board [row][col] = 0
                    return False
        return True
    
    def generate_full_solution(self):
        self.solve(self.board)
        return self.board
    
    def make_puzzle(self, difficulty='easy'):
        self.generate_full_solution()
        puzzle = copy.deepcopy(self.board)
        removals = {'easy': 30, 'medium': 40, 'hard': 50}
        cells_to_remove = removals.get(difficulty, 30)

        while cells_to_remove > 0:
            row, col = random.randint(0,8), random.randint(0,8)
            if puzzle[row][col] !=0:
                puzzle[row][col] = 0
                cells_to_remove -= 1
        return puzzle
    
class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku!!")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.original = [[0 for _ in range(9)] for _ in range(9)]
        self.generator = SudokuGenerator()
        self.solution = None
        self.start_time = time.time()
        self.timer_lable = tk.Label(self.root, text="Time: 0s", font=("Arial", 12))
        self.timer_lable.grid(row=10, column=0, columnspan=9)

        self.create_menu()
        self.create_grid()
        self.generate_new_puzzle('easy')

    def create_grid(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width= 3, font=('Arial', 18), justify='center')
                entry.grid(row= i, column=j, padx=1, pady=1)
                self.entries[i][j] = entry 

    def fill_grid(self, puzzle):
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(state='normal')
                entry.delete(0, tk.END)
                if puzzle[i][j] != 0:
                    entry.insert(0, str(puzzle[i][j]))
                    entry.config(state= 'disabled', disabledforeground= 'black')
                self.original[i][j] = puzzle[i][j]

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Game", menu= game_menu)
        game_menu.add_command(label="New Easy", command=lambda: self.generate_new_puzzle('easy'))
        game_menu.add_command(label="New Medium", command=lambda: self.generate_new_puzzle('medium'))
        game_menu.add_command(label="New Hard" , command=lambda: self.generate_new_puzzle('hard'))
        game_menu.add_separator()
        game_menu.add_command(label="Save Game", command= self.save_game)
        game_menu.add_command(label="Load Game", command= self.load_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command= self.root.quit)

        tools_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Tools", menu= tools_menu)
        tools_menu.add_command(label="Check Solution", command=self.check_solution)
        tools_menu.add_command(label="Auto-Solve", command=self.auto_solve)

    def generate_new_puzzle(self, difficulty):
        self.start_time= time.time()
        puzzle = self.generator.make_puzzle(difficulty)
        self.solution = copy.deepcopy(self.generator.board)
        self.fill_grid(puzzle)

    def get_current_grid(self):
        grid= []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                row.append(int(val) if val.isdigit() else 0)
            grid.append(row)
        return grid
    
    def check_solution(self):
        current = self.get_current_grid()
        if current == self.solution:
            elapsed = int(time.time() - self.start_time)
            messagebox.showinfo("Success",f"You solved it in {elapsed}!")
        else:
            messagebox.showerror("Incorrect", "That is not the correct solution.")

    def auto_solve(self):
        self.fill_grid(self.solution)

    def save_game(self):
        data = {
            'entries': self.get_current_grid(),
            'original': self.original,
            'solution': self.solution,
            'start_time': self.start_time
        }
        file_path = filedialog.asksaveasfilename(defaultextension= ".sudoku", filetypes=[("Sudoku Files", "*.sudoku")] )
        if file_path:
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            messagebox.showinfo("Saved", "Game saved successfully.")

    def load_game(self):
        file_path= filedialog.askopenfilename(filetypes=[("Sudoku Files", "*.sudoku")])
        if file_path:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)

            self.solution = data['solution']
            self.original = data['original']
            self.start_time = data['start_time']

            for i in range(9):
                for j in range(9):
                    entry = self.entries[i][j]
                    entry.config(state= 'normal')
                    entry.delete(0,tk.END)
                    value = data['entries'][i][j]
                    if self.original[i][j] != 0:
                        entry.insert(0, str(self.original[i][j]))
                        entry.config(state='disabled', disabledforeground= 'black')
                    elif value != 0:
                        entry.insert(0,str(value))

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_lable.config(text=f"Time: {elapsed}")
        self.root.after(1000, self.update_timer)

# Run the app
root = tk.Tk()
app = SudokuGUI(root)
root.mainloop()


            
                

                
