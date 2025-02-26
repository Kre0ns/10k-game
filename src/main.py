import customtkinter
import functions
from player import Player


class TenThousandGame(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Initialize game state
        self.current_player = 0
        self.player_list = []
        self.selected_dice = []
        self.turn_points = 0
        self.game_started = False
        self.final_round = False

        # Configure main window
        self.title("10K")
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

    def _create_game_board(self):
        # Create frames
        self._create_dice_frame()
        self._create_checkbox_frame()
        self._create_player_frame()
        self._create_control_buttons()

    def _create_dice_frame(self):
        self.dice_frame = customtkinter.CTkFrame(self)
        self.dice_frame.grid_columnconfigure(0, weight=1)
        self.dice_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.dice_frame.grid_propagate(False)
        self.dice_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        # Create dice labels
        for i in range(6):
            dice = customtkinter.CTkLabel(self.dice_frame, text="-", font=("Arial", 25))
            dice.grid(row=i, column=0)
            self.dice_list.append(dice)

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

    def _create_player_frame(self):
        self.player_holder_frame = customtkinter.CTkFrame(self)
        self.player_holder_frame.grid_columnconfigure(0, weight=1)
        self.player_holder_frame.grid_propagate(False)
        self.player_holder_frame.grid(
            column=2, row=0, padx=(0, 10), pady=10, sticky="nsew"
        )

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

        # Player entry
        self.player_name_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter player name"
        )
        self.player_name_entry.grid(
            column=2, row=1, padx=(0, 10), pady=(0, 10), sticky="nsew"
        )

        # Add player button
        self.add_player_button = customtkinter.CTkButton(
            self, text="Add player", command=self.add_player
        )
        self.add_player_button.grid(
            column=2, row=2, padx=(0, 10), pady=(0, 10), sticky="nsew"
        )

    def reset_game(self):
        self.current_player = 0
        self.selected_dice = []
        self.turn_points = 0
        self.game_started = False
        self.final_round = False

    def delete_player(self, frame):
        self.player_frame_list.remove(frame)
        frame.destroy()

    def roll_dice(self):
        rolls = functions.dice_rolls(6)

        for index, dice in enumerate(self.dice_list):
            dice.configure(text=rolls[index])

    def add_player(self):
        player_name = self.player_name_entry.get()

        if player_name and len(self.player_frame_list) < 6:
            new_player = Player(player_name)
            self.player_list.append(new_player)

            # Create player frame
            player_frame = customtkinter.CTkFrame(self.player_holder_frame)
            player_frame.grid_columnconfigure((0, 1), weight=3)
            player_frame.grid_columnconfigure(2, weight=1)
            player_frame.grid_rowconfigure(0, weight=1)
            player_frame.grid(column=0, padx=10, pady=(10, 0), sticky="ew")

            # Player name label
            player_label = customtkinter.CTkLabel(player_frame, text=player_name)
            player_label.grid(column=0, row=0)

            # Points label
            points_label = customtkinter.CTkLabel(player_frame, text=new_player.points)
            points_label.grid(column=1, row=0)

            # Delete button
            delete_button = customtkinter.CTkButton(
                player_frame,
                width=10,
                text="X",
                command=lambda f=player_frame: self.delete_player(f),
            )
            delete_button.grid(column=2, row=0, sticky="e")

            self.player_frame_list.append(player_frame)

    def game_loop(self):
        # To be implemented
        pass

    # starts the game loop if there is more than one player
    def start_game(self):
        if len(self.player_frame_list) > 1:
            self.game_loop()

    # ends turn adds points to player and moves the turn to the next player
    def end_turn(self):
        self.player_list[self.current_player].add_points(self.turn_points)
        self.current_player = (self.current_player + 1) % len(self.player_list)

    # starts new turn and reset the turn points and selcted dice
    def start_turn(self):
        self.turn_points = 0
        self.selected_dice = []


if __name__ == "__main__":
    game = TenThousandGame()
    game.mainloop()
