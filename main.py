#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, font
import sudoku


def routine():
    """
    Draws GUI application with Tkinter, starts new game
    """
    my_sudoku = []  # sudoku grid used for current game
    solution = []
    elements = []

    # default constraints
    bg_color = "white"

    def game():
        """
        Draws grid for one specific game.
        :return: None
        """
        nonlocal my_sudoku
        nonlocal elements
        active_field = None  # cell selected by click

        elements = [[] for i in range(9)]  # Clear cells of the grid

        def change_active_field(r, c):
            """
            Emulated Click handler. Selects cell the user clicks on by changing its color and making it the active field
            :param r: row of field clicked on
            :param c: column of the field
            :return: None
            """
            nonlocal active_field
            if active_field:  # reset color of last active field if one exists
                elements[active_field["row"]][active_field["column"]].config(bg=bg_color)
            active_field = {"row": r, "column": c}
            elements[r][c].config(bg="#E5E7E9")

        def change_number(event):
            """
            Key press handler. If a number is pressed and a cell is selected, the number is filled in to the cell.
            If backspace is pressed and a cell is selected, the cell's value is deleted.
            :param event: key press event, that occurred.
            :return: None
            """
            if active_field:
                if event.keysym == "BackSpace":
                    elements[active_field["row"]][active_field["column"]].config(text="")
                    solution[active_field["row"]][active_field["column"]] = 0
                elif event.char in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    elements[active_field["row"]][active_field["column"]].config(text=event.char, fg="black")
                    solution[active_field["row"]][active_field["column"]] = int(event.char)
                    # If the grid is entirely filled and no cell is still highlighted from last validation, valid the
                    # grid automatically.
                    # But actually fill the field before validating
                    window.update_idletasks()
                    if all(all(c != 0 for c in r) for r in solution) and \
                            all(all(element["fg"] != "red" for element in r) for r in elements):
                        check()

        window.bind("<Key>", change_number)

        args = {   # basic arguments for cell's Label
            "bg": bg_color
        }

        # Generate grid GUI with sudoku
        for i, row in enumerate(my_sudoku):
            for j, column in enumerate(row):
                frm = tk.Frame(  # Every cell should have a border
                    highlightbackground="black",
                    highlightthickness=1,
                    master=grid_frm
                )

                args["master"] = frm
                if column == 0:  # Labels of empty cells should not have any text and should be selected on click.
                    el = tk.Label(
                        **args
                    )
                    el.bind("<Button-1>", lambda event, r=i, c=j: change_active_field(r, c))
                else:  # Labels of cells filled by default should display the number
                    el = tk.Label(
                        **args,
                        text=column
                    )
                elements[i].append(el)
                # Make sudoku 3x3 squares visible by adding some space between them
                padding_top = 5 if i % 3 == 0 else 0
                padding_left = 5 if j % 3 == 0 else 0
                # Display cells in strict grid. Make the grid responsive to window size.
                el.pack(fill=tk.BOTH, expand=True)
                frm.grid(row=i, column=j, pady=(padding_top, 0), padx=(padding_left, 0), sticky="nsew")

        grid_frm.pack(fill=tk.BOTH, expand=True)  # Make grid responsive
        # Adjust font size after actual window size is known
        window.after(1, resize)
        tk.mainloop()

    window = tk.Tk()
    window.title("Sudoku")
    # Make window resize according to screen size, while big enough to display everything properly and as big as the
    # screen allows by default.
    window.aspect(32, 30, 32, 30)
    window.minsize(554, 519)
    window.geometry("1000x1000")
    frm_control_btns = tk.Frame(  # Upper row of buttons to control the game
        bg=bg_color
    )
    # Slider to set difficulty in percentage of masked cells. Default is 50, maximum is 90.
    scale_dif = tk.Scale(
        master=frm_control_btns,
        from_=1,
        to=9,
        orient=tk.HORIZONTAL
    )
    scale_dif.set(5)

    # Click listener and widget for New game button
    def new_game():
        """
        Generates a new sudoku and starts the game.
        :return: None
        """
        nonlocal my_sudoku
        nonlocal solution
        my_sudoku = sudoku.generate_sudoku(scale_dif.get()*10)
        solution = [row[:] for row in my_sudoku]
        game()

    btn_new_game = tk.Button(
        text="Neues Sudoku",
        bg=bg_color,
        master=frm_control_btns,
        command=new_game
    )

    # Click listener and widget for button to check if the solution is valid
    def check():
        """
        Checks solution from GUI and displays a success or error message.
        :return: None
        """
        if sudoku.check(solution):
            messagebox.showinfo(title="Richtig!", message="Herzlichen Glückwunsch! "
                                                          "\nDu hast das Sudoku richtig gelöst!")
        else:
            messagebox.showerror(title="Leider falsch", message="Leider noch nicht ganz richtig :(")
            # Find wrong fields (remember we made it very likely for the solution to be unique) and highlight them
            # by changing their text color to red.
            correct = sudoku.solve(my_sudoku)
            for i, row in enumerate(solution):
                for j, s in enumerate(row):
                    if not solution[i][j] == correct[i][j]:
                        elements[i][j].config(fg="red")

    btn_check = tk.Button(
        text="Überprüfen",
        bg=bg_color,
        master=frm_control_btns,
        command=check
    )

    # Click listener and widget for reset button
    def reset():
        """
        Resets the grid and the solution array to the originally created sudoku
        :return: None
        """
        nonlocal solution
        nonlocal my_sudoku
        solution = [row[:] for row in my_sudoku]
        game()

    btn_reset = tk.Button(
        text="Zurücksetzen",
        bg=bg_color,
        master=frm_control_btns,
        command=reset

    )

    # Label to indicate purpose of difficulty slider.
    scale_lbl = tk.Label(
        text="Schwierigkeit: ",
        bg=bg_color,
        master=frm_control_btns
    )

    # pack control elements
    scale_lbl.pack(side=tk.LEFT)
    scale_dif.pack(side=tk.LEFT)
    btn_new_game.pack(side=tk.LEFT)
    btn_reset.pack(side=tk.RIGHT)
    btn_check.pack(side=tk.RIGHT)

    frm_control_btns.pack(fill=tk.X)

    def resize(event=None):
        """
        Change the font size of the grid labels according to the cell size
        :param event: Config event, given by event handler
        :return: None
        """
        frame_height = elements[0][0].master.winfo_height()  # All cells are of equal size
        for row in elements:
            for element in row:
                element.config(font=("default", round(frame_height / 2.3)))

    # frame containing the game grid
    grid_frm = tk.Frame(bg=bg_color)
    # Make grid frame responsive
    for i in range(9):
        grid_frm.columnconfigure(i, weight=1, uniform="cell")
        grid_frm.rowconfigure(i, weight=1, uniform="cell")
    grid_frm.bind("<Configure>", resize)

    # start a new game and initialize grid on startup
    new_game()


if __name__ == "__main__":
    routine()
