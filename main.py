#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import sudoku
# TODO: License


def routine():
    """
    Draws GUI application with Tkinter, starts new game
    """
    my_sudoku = []  # sudoku grid used for current game
    solution = []

    # default constraints
    field_width = 5
    field_height = 2
    field_font = ("default", 30)
    bg_color = "white"

    def game():
        """
        Draws grid for one specific game.
        :return: None
        """
        nonlocal my_sudoku
        active_field = None  # cell selected by click

        elements = [[] for i in range(9)]  # Cells of the grid

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
            :param event: key press event, that occured.
            :return: None
            """
            if active_field:
                if event.keysym == "BackSpace":
                    elements[active_field["row"]][active_field["column"]].config(text="")
                    solution[active_field["row"]][active_field["column"]] = 0
                elif event.char in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    elements[active_field["row"]][active_field["column"]].config(text=event.char)
                    solution[active_field["row"]][active_field["column"]] = int(event.char)

        window.bind("<Key>", change_number)

        args = {"width": field_width, "bg": bg_color, "font": field_font,
                "height": field_height}  # basic arguments for cell's Label
        # Generate grid GUI with sudoku
        for i, row in enumerate(my_sudoku):
            for j, column in enumerate(row):
                frm = tk.Frame(  # Every cell should have a border
                    highlightbackground="black",
                    highlightthickness=1,
                    master=grid_frm,
                    height=field_height,
                    width=field_width
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
                # Display cells in strict grid.
                frm.grid(row=i, column=j, pady=(padding_top, 0), padx=(padding_left, 0))
                el.pack()

        grid_frm.pack()
        tk.mainloop()

    window = tk.Tk()
    window.title("Sudoku")
    frm_control_btns = tk.Frame(  # Upper row of buttons to control the game
        bg=bg_color
    )
    # Slider to set difficulty in percentage of masked cells. Default is 50, maximum is 90.
    scale_dif = tk.Scale(master=frm_control_btns, from_=1, to=9, orient=tk.HORIZONTAL)
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

    # frame containing the game grid
    grid_frm = tk.Frame(bg=bg_color)

    # start a new game and initialize grid on startup
    new_game()


if __name__ == "__main__":
    routine()
