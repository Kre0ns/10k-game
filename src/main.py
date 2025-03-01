from CTkMessagebox import CTkMessagebox
import customtkinter
import functions
import logging
from player import Player


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
        sidekick = Sidekick(self)

        # Initialize game state
        self.current_player = 0
        self.final_player = 0
        self.turn_points = 0
        self.player_list = []
        self.unlocked_dice = []
        self.current_rolls = []
        self.rolls_to_score = []
        self.final_round = False
        self.did_lock_dice = True
        self.winner_found = False
        self.preturn = True

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
            dice = customtkinter.CTkLabel(self.dice_frame, text="-", font=("Arial", 25))
            dice.roll = 0
            dice.grid(row=i, column=0)
            self.dice_list.append(dice)

        self.unlocked_dice = self.dice_list

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
            self, text="Roll dice", command=self.roll_dice
        )

        self.end_turn_button = customtkinter.CTkButton(
            self, text="End turn", command=self.end_turn
        )

        self.lock_dice_button = customtkinter.CTkButton(
            self, text="Lock dice", command=self.lock_dice
        )

        self.turn_points_label = customtkinter.CTkLabel(self, text="Turn points: 0")

        self.roll_button.grid(
            column=0,
            row=1,
            rowspan=2,
            padx=10,
            pady=(0, 10),
            sticky="nsew",
        )
        self.end_turn_button.grid(
            column=2,
            row=1,
            rowspan=2,
            padx=(0, 10),
            pady=(0, 10),
            sticky="nsew",
        )
        self.lock_dice_button.grid(
            column=1,
            row=1,
            padx=(0, 10),
            pady=(0, 10),
            sticky="nsew",
        )
        self.turn_points_label.grid(
            column=1,
            row=2,
            padx=(0, 10),
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
        for checkbox in self.checkbox_list:
            checkbox.configure(state="normal")
            checkbox.deselect()

        logging.debug("Reseting checkboxes...")

    def reset_dice(self):
        for dice in self.dice_list:
            dice.configure(text="-")

    # rolls the dice and sets the dice labels
    def roll_dice(self):
        if self.did_lock_dice:
            self.preturn = False
            self.current_rolls = functions.dice_rolls(len(self.unlocked_dice))

            for i, dice in enumerate(self.unlocked_dice):
                dice.roll = self.current_rolls[i]
                dice.configure(text=dice.roll)

            if functions.points_calc(self.current_rolls) == 0:
                self.turn_points = 0
                self.end_turn()
            else:
                self.did_lock_dice = False

        else:
            CTkMessagebox(
                self,
                title="Error",
                message="Please lock at least one die!",
                icon="warning",
            )

        logging.debug("Rolling dice...")

    # resets the game state
    def reset_board(self):
        self.reset_checkboxes()
        self.reset_dice()
        self.lock_dice()
        self.turn_points_label.configure(text="Turn points: 0")

        logging.debug("Reseting board..")

    # starts the game loop if there is more than one player
    def start_game(self, player_list):
        self.deiconify()

        self.player_list = player_list

        for player in player_list:
            self.add_player(player)

        self.highlight_current_player()

        logging.debug("Starting game...")

    # ends turn adds points to player and moves the turn to the next player
    def end_turn(self):
        if not self.preturn:
            if self.did_lock_dice:

                self.player_list[self.current_player].add_points(self.turn_points)
                self.update_points()

                self.is_winner()

                self.current_player = (self.current_player + 1) % len(self.player_list)
                self.highlight_current_player()

                self.turn_points = 0

                self.reset_board()

                self.preturn = True

                logging.debug("Ending turn...")

                if self.winner_found:
                    self.destroy()

            else:
                CTkMessagebox(
                    self,
                    title="Error",
                    message="Please lock at least one die!",
                    icon="warning",
                )

        else:
            CTkMessagebox(
                self,
                title="Error",
                message="Can't end turn with unrolled dice!",
                icon="warning",
            )

    # update the player point labels
    def update_points(self):
        for i, player in enumerate(self.player_list):
            self.player_frame_list[i].points_label.configure(text=player.points)

    # calculates of selcted dice
    def calc_turn_points(self):
        points = functions.points_calc(self.rolls_to_score)

        self.turn_points += points
        self.turn_points_label.configure(text=f"Turn points: {self.turn_points}")

        logging.debug("calculating points...")

    def lock_dice(self):
        if not self.preturn:
            self.unlocked_dice = []
            self.rolls_to_score = []

            locked_die = False

            for i, checkbox in enumerate(self.checkbox_list):
                if checkbox.cget("state") == "normal" and checkbox.get() == 0:
                    self.unlocked_dice.append(self.dice_list[i])

                elif checkbox.cget("state") == "normal" and checkbox.get() == 1:
                    locked_die = True
                    checkbox.configure(state="disabled")
                    self.rolls_to_score.append(self.dice_list[i].roll)

            if locked_die:
                self.calc_turn_points()

                self.did_lock_dice = True
        else:
            CTkMessagebox(
                self,
                title="Error",
                message="Can't lock unrolled dice!",
                icon="warning",
            )

    def is_winner(self):
        if self.final_round:
            if (self.current_player + 1) % len(self.player_list) == self.final_player:
                winner = functions.find_winner(self.player_list)
                winner_message = CTkMessagebox(
                    self,
                    title="Winner",
                    message=f"The winner is: {winner.name} with {winner.points} points!",
                    icon="check",
                )
                winner_message.get()
                self.winner_found = True

        elif self.player_list[self.current_player].points >= 10000:
            print("final round")
            self.final_round = True
            self.final_player = self.current_player

    def highlight_current_player(self):
        self.player_frame_list[
            (self.current_player - 1) % len(self.player_list)
        ].configure(fg_color=["gray81", "gray20"])
        self.player_frame_list[self.current_player].configure(fg_color="green")


class Sidekick(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.player_list = []
        self.starting_game = False

        self.title("Sidekick")
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
