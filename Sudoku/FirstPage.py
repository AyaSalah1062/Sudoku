import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
# from SudokuGenerator import SudokuGenerator
from CSPSolver import CSPSolver  # Import CSPSolver class 
from SolveUser import SolveUser
import random
from itertools import product
import time

class FirstPageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver - Mode Selection")
        self.root.geometry("700x600")
        self.bg_image = None  # Store the background image
        self.create_widgets()

    def create_widgets(self):
        try:
            image_path = "C:/Users/Dell/Desktop/gui2.jpeg"
            self.load_background_image(image_path)
        except Exception as e:
            print(f"Error loading background image: {e}")

        mode_frame = tk.Frame(self.root, padx=20, pady=20)
        mode_frame.place(relx=0.2, rely=0.5, anchor="center")

        mode_label = tk.Label(mode_frame, text="Select Mode:", font=("Arial", 18, "bold"))
        mode_label.pack(side="top", pady=10)

        self.mode_var = tk.StringVar(value="AI")
        ai_radio = tk.Radiobutton(mode_frame, text="AI", font=("Arial", 16), variable=self.mode_var, value="AI")
        ai_radio.pack(anchor="w", pady=5)

        user_radio = tk.Radiobutton(mode_frame, text="User", font=("Arial", 16), variable=self.mode_var, value="User")
        user_radio.pack(anchor="w", pady=5)

        level_frame = tk.Frame(self.root, padx=20, pady=20)
        level_frame.place(relx=0.8, rely=0.5, anchor="center")

        level_label = tk.Label(level_frame, text="Select Level:", font=("Arial", 18, "bold"))
        level_label.pack(side="top", pady=10)

        self.level_var = tk.StringVar(value="Easy")
        easy_check = tk.Checkbutton(level_frame, text="Easy", font=("Arial", 16), variable=self.level_var, onvalue="Easy", offvalue="")
        easy_check.pack(anchor="w", pady=5)

        intermediate_check = tk.Checkbutton(level_frame, text="Intermediate", font=("Arial", 16), variable=self.level_var, onvalue="Intermediate", offvalue="")
        intermediate_check.pack(anchor="w", pady=5)

        hard_check = tk.Checkbutton(level_frame, text="Hard", font=("Arial", 16), variable=self.level_var, onvalue="Hard", offvalue="")
        hard_check.pack(anchor="w", pady=5)

        if self.mode_var.get() == "User":
            start_button_text = "Start Game"
        else:
            start_button_text = "Solve with CSP"

        start_button = tk.Button(self.root, text=start_button_text, font=("Arial", 16, "bold"), bg="green", fg="white", command=self.start_game)
        start_button.place(relx=0.5, rely=0.8, anchor="center")

    def load_background_image(self, image_path):
        try:
            image = Image.open(image_path)
            image = image.resize((800, 600), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            bg_label = tk.Label(self.root, image=self.bg_image)
            bg_label.image = self.bg_image  # Keep a reference to the image
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

    def start_game(self):
        mode = self.mode_var.get()
        level = self.level_var.get()

        if not level:
            messagebox.showerror("Error", "Please select a difficulty level.")
            return

        self.open_sudoku_game(level, mode)

    def open_sudoku_game(self, level, mode):
        self.root.withdraw()  # Hide the mode selection window
        game_root = tk.Tk()
        game_root.title("Sudoku Game")
        sudoku_gui = SudokuGUI(game_root, level, mode, self.root)  # Pass the mode selection window as parent

class SudokuGUI:
    def __init__(self, master, level, mode, mode_root):
        self.master = master
        self.master.title("Sudoku Solver")
        self.mode_root = mode_root

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        self.board_size = min(screen_width, screen_height) * 0.65
        self.cell_size = self.board_size // 9

        self.level = level
        self.mode = mode
        self.board = [[0]*9 for _ in range(9)]
        self.selected_cell = None
        self.solution_board = None
        self.start_time = None
        # self.timer_running = False
        # self.timer_label = tk.Label(self.master, text="Timer: 00:00", font=("Arial", 14))
        # self.timer_label.pack(pady=10)
        self.constraints_label = tk.Label(self.master, text="Constraints: ", font=("Arial", 14))
        self.constraints_label.pack(pady=10)

        self.timer_label = tk.Label(self.master, text="Solver Time: ......", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.board_size, height=self.board_size, bg="white")
        self.canvas.pack(expand=True)
        self.canvas.focus_set() 

        button_frame = tk.Frame(self.master)
        button_frame.pack(pady=20)

        generate_manual_button = tk.Button(button_frame, text="Generate Manually", font=("Arial", 15),
                                           command=self.generate_manual_puzzle, bg="black", fg="white")
        generate_manual_button.pack(side="left", padx=10)

        generate_random_button = tk.Button(button_frame, text="Generate Randomly", font=("Arial", 15),
                                           command=self.generate_random_puzzle, bg="black", fg="white")
        generate_random_button.pack(side="left", padx=10)

        if self.mode == "User":
            start_button_text = "Start Game"
            start_button_command = self.start_user_game
        else:
            start_button_text = "Solve"
            start_button_command = self.solve_with_csp
        
        start_button = tk.Button(button_frame, text=start_button_text, font=("Arial", 16, "bold"), bg="green", fg="white", command=start_button_command)
        start_button.pack(side="left", padx=10)
        
        clear_button = tk.Button(button_frame, text="Clear", font=("Arial", 16),
                                 command=self.clear_puzzle, bg="black", fg="white")
        clear_button.pack(side="left", padx=10)

        exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 16),
                                command=self.master.destroy, bg="red", fg="white")
        exit_button.pack(side="left", padx=10)

        return_button = tk.Button(button_frame, text="Back", font=("Arial", 16),
                                  command=self.return_to_mode_selection, bg="orange", fg="white")
        return_button.pack(side="left", padx=10)
        
        self.canvas.bind("<Button-1>", self.validate_user_input)
        self.canvas.bind("<Key>", self.validate_user_input)

        self.draw_empty_grid()

    def return_to_mode_selection(self):
        self.master.destroy()
        self.mode_root.deiconify()

    def display_constraints(self, row, col):
        row = int(row)
        col = int(col)
        
        if self.board[row][col] == 0:
            valid_constraints = [num for num in range(1, 10) if self.is_valid_move(row, col, num)]
            if valid_constraints:
                valid_nums = ", ".join(map(str, valid_constraints))
                self.constraints_label.config(text=f"Valid numbers for cell ({row}, {col}): {valid_nums}")
            else:
                self.constraints_label.config(text=f"No valid numbers for cell ({row}, {col})")
        else:
            self.constraints_label.config(text="")

    def draw_empty_grid(self):
        self.canvas.delete("all")
        for i in range(9):
            for j in range(9):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                color = "white" if (i // 3 + j // 3) % 2 == 0 else "lightgray"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def generate_manual_puzzle(self):
        self.clear_puzzle()
        self.selected_cell = None
        self.draw_grid()

        # messagebox.showinfo("Manual Input", "Click on a cell to input a number.")
        self.canvas.bind("<Button-1>", self.on_manual_input)

    def on_manual_input(self, event):
        col, row = event.x // self.cell_size, event.y // self.cell_size
        # Ensure row and col are integers
        row = int(row)
        col = int(col)
        if 0 <= row < 9 and 0 <= col < 9:
            self.selected_cell = (row, col)
            self.display_constraints(row, col)
            self.draw_grid()  # Redraw to highlight the selected cell and display constraints
            self.master.bind("<Key>", self.input_number)


    def input_number(self, event):
        if event.char.isdigit() and self.selected_cell:
            num = int(event.char)
            row, col = self.selected_cell
            
            # Ensure row and col are integers
            row = int(row)
            col = int(col)
            
            if 1 <= num <= 9 and self.is_valid_move(row, col, num):
                self.board[row][col] = num
                self.draw_grid()  # Redraw grid after valid number input
            # else:
            #     messagebox.showerror("Invalid Number", "This number cannot be placed here. Please try again.")
        elif event.keysym == "BackSpace" and self.selected_cell:
            row, col = self.selected_cell
            # Ensure row and col are integers
            row = int(row)
            col = int(col)
            
            self.board[row][col] = 0
            self.draw_grid()  # Redraw grid after clearing the cell

    def generate_random_puzzle(self):
        self.clear_puzzle()
        num_random_cells = {"Easy": 41, "Intermediate": 51, "Hard": 61}[self.level]
        for _ in range(10):
            while True:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                num = random.randint(1, 9)
                if self.is_valid_move(row, col, num):
                    self.board[row][col] = num
                    break
        csp_solver = CSPSolver(self.board)
        solution = csp_solver.solve(0)
        if not solution:
            self.generate_random_puzzle()
            return
        random_cells = random.sample(list(product(range(9), range(9))), num_random_cells)
        for row, col in random_cells:
            solution[row][col] = 0
        self.board = solution
        self.draw_grid()

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            self.timer_label.config(text=f"Timer: {minutes:02d}:{seconds:02d}")
            self.master.after(1000, self.update_timer)

    def start_user_game(self):
        # Solve the puzzle without generating it on the board and save the solution
        self.solution_board = self.solve_user_with_csp()
        if self.solution_board:
            self.start_timer()  # Start the timer when the game starts
            self.selected_cell = None
            self.draw_grid()
            self.canvas.bind("<Button-1>", self.on_user_input)
        else:
            messagebox.showerror("Error", "Failed to generate a valid solution.")



    def on_user_input(self, event):
        col, row = event.x // self.cell_size, event.y // self.cell_size
        # Ensure row and col are integers
        row = int(row)
        col = int(col)
        if 0 <= row < 9 and 0 <= col < 9:
            self.selected_cell = (row, col)
            self.display_constraints(row, col)
            self.draw_grid()  # Redraw to highlight the selected cell and display constraints
            self.master.bind("<Key>", self.input_number2)

    def color_cell_green(self, row, col):
        x0, y0 = col * self.cell_size, row * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")
        num = self.board[row][col]
        if num != 0:
            self.canvas.create_text(x0 + self.cell_size / 2, y0 + self.cell_size / 2, text=str(num), font=("Arial", 16), fill="black")

    def color_cell_red(self, row, col):
        x0, y0 = col * self.cell_size, row * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="red")
        num = self.board[row][col]
        if num != 0:
            self.canvas.create_text(x0 + self.cell_size / 2, y0 + self.cell_size / 2, text=str(num), font=("Arial", 16), fill="black")
    
    def is_puzzle_solved(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False
        return True
    def input_number2(self, event):
        if self.selected_cell:
            row, col = self.selected_cell
            num = event.char
            if num.isdigit():
                num = int(num)
                if 1 <= num <= 9:
                    if self.board[row][col] == self.solution_board[row][col]:
                        self.color_cell_green(row, col)
                        if self.is_puzzle_solved():
                            self.stop_timer()  # Stop the timer when the puzzle is solved
                            messagebox.showinfo("Congratulations", "Puzzle is solved!")
                    else:
                        self.color_cell_red(row, col)

    def solve_user_with_csp(self):
        # Function to solve the puzzle without generating it on the board
        start_time = time.time()
        solver = SolveUser(self.board)  # Instantiate SolveUser properly
        solution = solver.solve(1)  # Call the solve method from the instantiated object
        end_time = time.time()  # Record the end time of the solver
        solver_time = end_time - start_time  # Calculate the solver time
        if solution:
            return solution
        else:
            messagebox.showinfo("No Solution", "No solution found for the Sudoku puzzle.")
            return None

    def validate_user_input(self, event):
        # Handles both mouse clicks and keyboard inputs for entering numbers
        if self.selected_cell:
            x = int(event.x)
            y = int(event.y)
            row, col = y // self.cell_size, x // self.cell_size
            row = int(row) # Ensure row is an integer
            col = int(col) # Ensure col is an integer
            num = int(event.char) if event.char.isdigit() else None

            if num and 1 <= num <= 9 and self.is_valid_move(row, col, num):
                self.board[row][col] = num
                self.draw_grid() # Redraw grid after valid number input
                self.check_correctness(row, col)
            elif event.keysym == "BackSpace":
                self.board[row][col] = 0
                self.draw_grid() # Redraw grid after clearing the cell
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid number (1-9) or use Backspace to clear.")

    def check_correctness(self, row, col):
        # Checks if the user's input matches the solution board
        if self.solution_board is None:
            print("Solution board not available.")
            return
        if self.board[row][col] == self.solution_board[row][col]:
            print("Correct")
        else:
            print("Incorrect")

    def clear_puzzle(self):
        self.board = [[0]*9 for _ in range(9)]
        self.draw_grid()
        self.timer_label.config(text=f"Solver Time:........")


    def draw_grid(self):
        self.draw_empty_grid()

        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                x, y = j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2

                # Highlight selected cell
                if self.selected_cell == (i, j):
                    self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                                 (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                                 outline="black", width=2)

                # Draw numbers with different colors based on validity
                if num != 0:
                    if self.is_valid_move(i, j, num):
                        text_color = "black"  # Valid number color
                    else:
                        text_color = "black"    # Invalid number color

                    # Draw number with shadow effect
                    self.canvas.create_text(x + 2, y + 2, text=str(num), font=("Arial", 16), fill="gray")
                    self.canvas.create_text(x, y, text=str(num), font=("Arial", 16), fill=text_color)

        if self.selected_cell:
            row, col = self.selected_cell
            x0, y0 = col * self.cell_size, row * self.cell_size
            x1, y1 = x0 + self.cell_size, y0 + self.cell_size
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="blue", width=2)

    def is_valid_move(self, row, col, num):
        row = int(row)
        col = int(col)
        # Check row
        if num in self.board[row]:
            return False

        # Check column
        if num in [self.board[i][col] for i in range(9)]:
            return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def solve_with_csp(self):
        start_time = time.time()
        csp_solver = CSPSolver(self.board)
        solution = csp_solver.solve(1)
        end_time = time.time()  # Record the end time of the solver
        solver_time = end_time - start_time  # Calculate the solver time
        if solution:
            self.board = solution
            self.draw_grid()
            self.timer_label.config(text=f"Solver Time: {solver_time:.4f}")
        else:
            messagebox.showinfo("No Solution", "No solution found for the Sudoku puzzle.")

def main():
    root = tk.Tk()
    app = FirstPageGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()