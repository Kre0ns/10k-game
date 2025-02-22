import customtkinter
import functions


def main():
    # gets the dice rolls and displays them on screen
    def roll_dice():
        rolls = functions.dice_rolls(6)

        for index, dice in enumerate(dice_list):
            dice.configure(text=rolls[index])

    def add_player():
        pass

    # initializing app
    app = customtkinter.CTk()
    app.title("10K")
    app.geometry("640x400")
    app.resizable(False, False)

    # grid config
    app.grid_columnconfigure((0, 1, 2), weight=1)
    app.grid_rowconfigure((0, 1, 2), weight=1)

    # dice frame config
    dice_frame = customtkinter.CTkFrame(app)
    dice_frame.grid_columnconfigure((0), weight=1)
    dice_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    dice_frame.grid_propagate(False)
    dice_list = []  # stored the dice labels

    # checkbox frame config
    checkbox_frame = customtkinter.CTkFrame(app)
    checkbox_frame.grid_columnconfigure((0), weight=1)
    checkbox_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    checkbox_frame.grid_propagate(False)
    checkbox_list = []  # stores the checkboxes

    # player holder frame config (a frame for the player frames)
    player_holder_frame = customtkinter.CTkFrame(app)
    player_holder_frame.grid_columnconfigure((0), weight=4)
    player_holder_frame.grid_columnconfigure((1), weight=1)
    player_holder_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
    player_holder_frame.grid_propagate(False)
    player_frame_list = []  # stores the player frames

    # generating dice and checkboxes
    for i in range(6):
        # dice config
        dice = customtkinter.CTkLabel(dice_frame, text="-", font=("Arial", 25))
        dice.grid(row=i, column=0)
        dice_list.append(dice)

        # checkbox config
        checkbox = customtkinter.CTkCheckBox(checkbox_frame, text=None)
        checkbox.grid(row=i, column=0)
        checkbox_list.append(checkbox)

    # displaying the frames
    dice_frame.grid(column=0, row=0, padx=10, pady=10, sticky="ewsn")
    checkbox_frame.grid(column=1, row=0, padx=(0, 10), pady=10, sticky="ewsn")
    player_holder_frame.grid(column=2, row=0, padx=(0, 10), pady=10, sticky="ewsn")

    # roll button config
    roll_button = customtkinter.CTkButton(app, text="Roll The dice!", command=roll_dice)
    roll_button.grid(
        column=0, row=1, columnspan=2, rowspan=2, padx=10, pady=(0, 10), sticky="ewsn"
    )

    # player name entry config
    player_name_entry = customtkinter.CTkEntry(
        app, placeholder_text="Enter player name"
    )
    player_name_entry.grid(column=2, row=1, padx=(0, 10), pady=(0, 10), sticky="ewsn")

    # add player button config
    add_player_button = customtkinter.CTkButton(
        app, text="Add player", command=add_player
    )
    add_player_button.grid(column=2, row=2, padx=(0, 10), pady=(0, 10), sticky="ewsn")

    # starting the app loop
    app.mainloop()


if __name__ == "__main__":
    main()
