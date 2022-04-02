#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import sudoku
# TODO: License


def routine():
    """
    Draws GUI application with Tkinter, starts new game
    """
    my_sudoku = []

    def game():
        """
        Draws grid for own specific game.
        :return: None
        """
        nonlocal my_sudoku
        active_field = None

        elements = [[] for i in range(9)]

        def change_active_field(field, r, c):
            nonlocal active_field
            if active_field:
                elements[active_field["row"]][active_field["column"]].config(bg="white")
            active_field = {"field": field, "row": r, "column": c}
            elements[r][c].config(bg="#E5E7E9")

        def change_number(event):
            if active_field:
                if event.keysym == "BackSpace":
                    elements[active_field["row"]][active_field["column"]].config(text="")
                    solution[active_field["row"]][active_field["column"]] = 0
                elif event.char in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    elements[active_field["row"]][active_field["column"]].config(text=event.char)
                    solution[active_field["row"]][active_field["column"]] = int(event.char)

        window.bind("<Key>", change_number)

        for i, row in enumerate(my_sudoku):
            for j, column in enumerate(row):
                frm = tk.Frame(
                    highlightbackground="black",
                    highlightthickness=1,
                    master=grid_frm,
                    height=field_height,
                    width=field_width
                )
                args = {"master": frm, "width": field_width, "background": "white", "font": field_font, "height": field_height}
                if column == 0:
                    el = tk.Label(
                        **args
                    )
                    el.bind("<Button-1>", lambda event, field=el, r=i, c=j: change_active_field(el, r, c))
                else:
                    el = tk.Label(
                        **args,
                        text=column
                    )
                elements[i].append(el)
                padding_top = 5 if i % 3 == 0 else 0
                padding_left = 5 if j % 3 == 0 else 0
                frm.grid(row=i, column=j, pady=(padding_top, 0), padx=(padding_left, 0))
                el.pack()

        grid_frm.pack()
        tk.mainloop()

    window = tk.Tk()
    frm_control_btns = tk.Frame(
        bg="white"
    )
    scale_dif = tk.Scale(master=frm_control_btns, from_=1, to=9, orient=tk.HORIZONTAL)
    scale_dif.set(5)

    def new_game():
        nonlocal my_sudoku
        nonlocal solution
        my_sudoku = sudoku.generate_sudoku(scale_dif.get()*10)
        solution = [row[:] for row in my_sudoku]
        game()

    btn_new_game = tk.Button(
        text="Neues Sudoku",
        background="white",
        master=frm_control_btns,
        command=new_game
    )

    def check():
        if sudoku.check(solution):
            messagebox.showinfo(title="Richtig!", message="Herzlichen Glückwunsch! \nDu hast das Sudoku richtig gelöst!")
        else:
            messagebox.showerror(title="Leider falsch", message="Leider noch nicht ganz richtig :(")

    btn_check = tk.Button(
        text="Überprüfen",
        background="white",
        master=frm_control_btns,
        command=check
    )

    def reset():
        nonlocal solution
        nonlocal my_sudoku
        solution = [row[:] for row in my_sudoku]
        game()

    btn_reset = tk.Button(
        text="Zurücksetzen",
        background="white",
        master=frm_control_btns,
        command=reset

    )

    scale_lbl = tk.Label(
        text="Schwierigkeit: ",
        background="white",
        master=frm_control_btns
    )
    scale_lbl.pack(side=tk.LEFT)
    scale_dif.pack(side=tk.LEFT)
    btn_new_game.pack(side=tk.LEFT)
    btn_reset.pack(side=tk.RIGHT)
    btn_check.pack(side=tk.RIGHT)

    frm_control_btns.pack(fill=tk.X)

    grid_frm = tk.Frame(bg="white")

    field_width = 5
    field_height = 2
    field_font = ("default", 30)

    solution = []
    new_game()


if __name__ == "__main__":
    routine()
