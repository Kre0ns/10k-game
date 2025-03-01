import customtkinter
import functions
from player import Player
import logging


def main():

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - line: %(lineno)d - %(message)s",
        filename="game_log.log",
        filemode="w",
    )


class Game(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.withdraw()
        pregame = Pregame(self)

        # Initialize game state
        self.current_player = 0
        self.turn_points = 0
        self.player_list = []
        self.unlocked_dice = []
        self.current_rolls = []
        self.rolls_to_score = []
        self.game_started = False
        self.final_round = False

        # Configure main window
        self.title("Game")
        self.geometry("640x400")
        self.resizable(False, False)

        # Configure columns and rows
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Store references to dynamic elements
        self.dice_list = []
        self.checkbox_list = []
        self.player_frame_list = []

        # Initialize game board
        self._create_game_board()

    # creates the UI elements
    def _create_game_board(self):
        # Create frames
        self._create_dice_frame()
        self._create_checkbox_frame()
        self._create_player_frame()
        self._create_control_buttons()

    # creates the dice frame and fills it
    def _create_dice_frame(self):
        self.dice_frame = customtkinter.CTkFrame(self)
        self.dice_frame.grid_columnconfigure(0, weight=1)
        self.dice_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.dice_frame.grid_propagate(False)
        self.dice_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        # Create dice labels
        for i in range(6):
            dice = customtkinter.CTkLabel(self.dice_frame, text="0", font=("Arial", 25))
            dice.roll = 0
            dice.grid(row=i, column=0)
            self.dice_list.append(dice)

    # creates the checkbox frame and fills it
    def _create_checkbox_frame(self):
        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.grid_columnconfigure(0, weight=1)
        self.checkbox_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.checkbox_frame.grid_propagate(False)
        self.checkbox_frame.grid(column=1, row=0, padx=(0, 10), pady=10, sticky="nsew")

        # Create checkboxes
        for i in range(6):
            checkbox = customtkinter.CTkCheckBox(self.checkbox_frame, text=None)
            checkbox.grid(row=i, column=0)
            self.checkbox_list.append(checkbox)

    # creates the player frame
    def _create_player_frame(self):
        self.player_holder_frame = customtkinter.CTkFrame(self)
        self.player_holder_frame.grid_columnconfigure(0, weight=1)
        self.player_holder_frame.grid_propagate(False)
        self.player_holder_frame.grid(
            column=2, row=0, padx=(0, 10), pady=10, sticky="nsew"
        )

    # creates the control buttons
    def _create_control_buttons(self):
        # Roll button
        self.roll_button = customtkinter.CTkButton(
            self, text="Roll The dice!", command=self.roll_dice
        )
        self.roll_button.grid(
            column=0,
            row=1,
            columnspan=2,
            rowspan=2,
            padx=10,
            pady=(0, 10),
            sticky="nsew",
        )

    # adds a player
    def add_player(self, player):
        player_name = player.name

        # Create player frame
        player_frame = customtkinter.CTkFrame(self.player_holder_frame)
        player_frame.grid_columnconfigure((0, 1), weight=1)
        player_frame.grid_rowconfigure(0, weight=1)
        player_frame.grid(column=0, padx=10, pady=(10, 0), sticky="ew")

        # Player name label
        player_label = customtkinter.CTkLabel(player_frame, text=player_name)
        player_label.grid(column=0, row=0)

        # Points label
        points_label = customtkinter.CTkLabel(player_frame, text=player.points)
        player_frame.points_label = points_label
        points_label.grid(column=1, row=0)

        self.player_frame_list.append(player_frame)

        logging.debug("Adding player...")

    # resets checkboxes
    def reset_checkboxes(self):
        for i, checkbox in enumerate(self.checkbox_list):
            checkbox.configure(state="normal")
            checkbox.deselect()

        logging.debug("Reseting checkboxes...")

    # deletes a player
    def delete_player(self, frame):
        self.player_frame_list.remove(frame)
        frame.destroy()

        logging.debug("Deleting player...")

    # updates the unlocked dice based on the checkboxes
    def update_unlocked(self):
        self.unlocked_dice = []
        self.rolls_to_score = []

        for i, checkbox in enumerate(self.checkbox_list):
            if checkbox.cget("state") == "normal" and checkbox.get() == 0:
                self.unlocked_dice.append(self.dice_list[i])

            elif checkbox.cget("state") == "normal" and checkbox.get() == 1:
                checkbox.configure(state="disabled")
                self.rolls_to_score.append(self.dice_list[i].roll)

        logging.debug("Updating dice...")

    # rolls the dice and sets the dice labels
    def roll_dice(self):
        self.update_unlocked()
        self.calc_turn_points()

        self.current_rolls = functions.dice_rolls(len(self.unlocked_dice))

        for i, dice in enumerate(self.unlocked_dice):
            dice.roll = self.current_rolls[i]
            dice.configure(text=dice.roll)

        logging.debug("Rolling dice...")

    # resets the game state
    def reset_game(self):
        self.current_player = 0
        self.unlocked_dice = []
        self.turn_points = 0
        self.game_started = False
        self.final_round = False

        logging.debug("Reseting game...")

    # WIP game loop
    def game_loop(self):
        # To be implemented
        pass

    # starts the game loop if there is more than one player
    def start_game(self, player_list):
        self.deiconify()

        self.player_list = player_list

        for player in player_list:
            self.add_player(player)

        logging.debug("Starting game...")

    # ends turn adds points to player and moves the turn to the next player
    def end_turn(self):
        self.player_list[self.current_player].add_points(self.turn_points)
        self.current_player = (self.current_player + 1) % len(self.player_list)

        logging.debug("Ending turn...")

    # starts new turn and reset the turn points and selcted dice
    def start_turn(self):
        self.turn_points = 0
        self.unlocked_dice = []

        logging.debug("Starting turn...")

    # update the player point labels
    def update_points(self):
        for i, player in enumerate(self.player_list):
            self.player_frame_list[i].points_label.configure(text=player.points)

    # calculates of selcted dice
    def calc_turn_points(self):
        points = functions.points_calc(self.rolls_to_score)

        if points == 0:
            self.end_turn()
        else:
            self.turn_points += points

        logging.debug("calculating points...")


class Pregame(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.player_list = []
        self.starting_game = False

        self.title("Pregame")
        self.geometry("220x400")
        self.resizable(False, False)

        # Configure columns and rows
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self._create_interface()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _create_interface(self):
        self.player_holder_frame = customtkinter.CTkFrame(self)
        self.player_holder_frame.grid_columnconfigure(0, weight=1)
        self.player_holder_frame.grid_propagate(False)
        self.player_holder_frame.grid(
            column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

        self.name_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter Player name"
        )
        self.name_entry.grid(
            column=0, row=1, columnspan=2, padx=10, pady=(0, 10), sticky="nsew"
        )

        self.add_player_button = customtkinter.CTkButton(
            self, text="Add player", command=self.add_player
        )
        self.add_player_button.grid(
            column=0, row=2, padx=10, pady=(0, 10), sticky="nsew"
        )

        self.start_game_button = customtkinter.CTkButton(
            self,
            text="Start game",
            command=self.start_game,
            fg_color="red",
            hover_color="#0a5c0d",
            text_color_disabled="#DCE4EE",
            state="disabled",
        )
        self.start_game_button.grid(
            column=1, row=2, padx=(0, 10), pady=(0, 10), sticky="nsew"
        )

    def add_player(self):
        player_name = self.name_entry.get().strip()

        if player_name and len(self.player_list) < 6:
            self.name_entry.delete(0, customtkinter.END)

            new_player = Player(player_name)
            self.player_list.append(new_player)

            # Create player frame
            player_frame = customtkinter.CTkFrame(self.player_holder_frame)
            player_frame.grid_columnconfigure(0, weight=1)
            player_frame.grid_columnconfigure(1, weight=0)
            player_frame.grid_rowconfigure(0, weight=1)
            player_frame.grid(column=0, padx=10, pady=(10, 0), sticky="ew")

            # Player name label
            player_label = customtkinter.CTkLabel(player_frame, text=player_name)
            player_label.grid(column=0, row=0)

            # Delete button
            delete_button = customtkinter.CTkButton(
                player_frame,
                width=10,
                text="X",
                command=lambda f=player_frame, p=new_player: self.delete_player(f, p),
            )
            delete_button.grid(column=1, row=0, sticky="e")

            self.can_start()

    def can_start(self):
        if len(self.player_list) >= 2:
            self.start_game_button.configure(fg_color="green", state="normal")
        else:
            self.start_game_button.configure(fg_color="red", state="disabled")

    def start_game(self):
        self.starting_game = True
        self.master.start_game(self.player_list)
        self.destroy()

    def delete_player(self, frame, player):
        self.player_list.remove(player)
        frame.destroy()

        self.can_start()

    def on_close(self):
        if not self.starting_game:
            self.master.destroy()


if __name__ == "__main__":
    main()

    app = Game()
    app.mainloop()
