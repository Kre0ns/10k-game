import customtkinter
import functions


def main():
    def roll_dice():
        rolls = functions.dice_rolls(6)
        for index, dice in enumerate(dice_list):
            dice.configure(text=rolls[index])

    app = customtkinter.CTk()
    app.title("my app")
    app.geometry("640x764")
    app.resizable(False, False)
    app.grid_columnconfigure((1), weight=1)
    app.grid_columnconfigure((0), weight=2)
    app.grid_rowconfigure((0, 1), weight=1)

    dice_frame = customtkinter.CTkFrame(app)
    dice_frame.grid_columnconfigure((0), weight=1)
    dice_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    dice_list = []

    checkbox_frame = customtkinter.CTkFrame(app)
    checkbox_frame.grid_columnconfigure((0), weight=1)
    checkbox_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    checkbox_list = []

    for i in range(6):
        dice = customtkinter.CTkLabel(dice_frame, text=i, font=("Arial", 25))
        dice.grid(row=i, column=0)
        dice_list.append(dice)

        checkbox = customtkinter.CTkCheckBox(checkbox_frame, text=None)
        checkbox.grid(row=i, column=0, padx=(0, 50), sticky="e")
        checkbox_list.append(checkbox)

    dice_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ewsn")
    checkbox_frame.grid(column=1, row=0, padx=(0, 10), pady=10, sticky="ewsn")

    btn = customtkinter.CTkButton(app, text="Roll The dice!", command=roll_dice)
    btn.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="ewsn")

    app.mainloop()


if __name__ == "__main__":
    main()
