from CTkMessagebox import CTkMessagebox
import customtkinter
import functions
import logging
from pathlib import Path
from player import Player


def main():
    #  check for _internal folder in base, if exist log there else log in base
    log_file = (
        (
            Path(__file__).parent / "_internal"
            if (Path(__file__).parent / "_internal").exists()
            else Path(__file__).parent
        )
    ) / "game_log.log"

    # Configure logging for debugging and tracking errors
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - line: %(lineno)d - %(message)s",
        filename=log_file,
        filemode="w",
    )


class Game(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        logging.info("Initializing main window")

        # if _internal exists look for icon in it, else look in base
        icon_path = (
            Path(__file__).parent.parent / "_internal"
            if (Path(__file__).parent.parent / "_internal").exists()
            else Path(__file__).parent.parent / "res"
        ) / "icon.ico"
        self.iconbitmap(icon_path)

        # Initially hide the main window and open the sidekick window for player setup
        self.withdraw()
        Sidekick(self)

        # Initialize game state variables
        self.current_player = 0  # Index for the active player
        self.final_player = 0  # Index of the player that triggered the final round
        self.turn_points = 0  # Points accumulated in the current turn
        self.player_list = []  # List to store all player objects
        self.unlocked_dice = []  # Dice available for the next roll
        self.current_rolls = []  # Most recent dice roll results
        self.rolls_to_score = []  # Dice values selected for scoring
        self.final_round = False  # Flag to indicate the final round has started
        self.dice_locked = (
            True  # Indicates if dice are locked (prevents immediate re-roll)
        )
        self.winner_found = False  # Set to True once a winner is determined
        self.dice_rolled = (
            False  # True if dice have been rolled during the current turn
        )
        self.default_text_color = ""

        # Set up the main window appearance and behavior
        self.title("Game")
        self.geometry("640x400")
        self.resizable(False, False)

        # Define the grid layout for UI elements
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create lists to keep track of dynamically generated UI components
        self.dice_list = []  # List of dice label widgets
        self.checkbox_list = []  # List of checkboxes for locking dice
        self.player_frame_list = []  # List of frames showing each player's info

        # Build the game board interface
        self._create_game_board()

    # -------------------------------------------------------------------------
    # UI Creation Methods
    # -------------------------------------------------------------------------
    def _create_game_board(self):
        """Initializes the main sections of the game board UI."""

        self._create_dice_frame()
        self._create_checkbox_frame()
        self._create_player_frame()
        self._create_control_buttons()

    def _create_dice_frame(self):
        """Creates a frame to display dice and initializes six dice labels."""

        self.dice_frame = customtkinter.CTkFrame(self)
        self.dice_frame.grid_columnconfigure(0, weight=1)
        self.dice_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.dice_frame.grid_propagate(False)
        self.dice_frame.grid(column=1, row=0, padx=(0, 10), pady=10, sticky="nsew")

        # Create six dice labels with default text and store them in the dice_list
        for i in range(6):
            dice = customtkinter.CTkLabel(
                self.dice_frame, text="-", font=("Arial", 25, "bold")
            )
            dice.roll = 0  # Initialize each dice's roll value
            dice.grid(row=i, column=0, sticky="ew")
            self.dice_list.append(dice)

        # At start, all dice are available to roll
        self.unlocked_dice = self.dice_list

    def _create_checkbox_frame(self):
        """Creates a frame with a checkbox for each dice to allow locking them."""

        self.checkbox_frame = customtkinter.CTkFrame(self)
        self.checkbox_frame.grid_columnconfigure(0, weight=1)
        self.checkbox_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.checkbox_frame.grid_propagate(False)
        self.checkbox_frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        # Add a checkbox for every dice
        for i in range(6):
            checkbox = customtkinter.CTkCheckBox(
                self.checkbox_frame, text="Lock die --->", font=("Arial", 14, "bold")
            )
            checkbox.grid(row=i, column=0)
            self.checkbox_list.append(checkbox)

    def _create_player_frame(self):
        """Creates a panel to hold player information like names and scores."""

        self.player_holder_frame = customtkinter.CTkFrame(self)
        self.player_holder_frame.grid_columnconfigure(0, weight=1)
        self.player_holder_frame.grid_propagate(False)
        self.player_holder_frame.grid(
            column=2, row=0, padx=(0, 10), pady=10, sticky="nsew"
        )

    def _create_control_buttons(self):
        """Creates control buttons and a label for displaying turn points."""

        # Button to roll dice
        self.roll_button = customtkinter.CTkButton(
            self, text="Roll dice", command=self.roll_dice, font=("Arial", 17, "bold")
        )
        # Button to end the current turn
        self.end_turn_button = customtkinter.CTkButton(
            self, text="End turn", command=self.end_turn, font=("Arial", 17, "bold")
        )
        # Button to lock selected dice for scoring
        self.lock_dice_button = customtkinter.CTkButton(
            self, text="Lock dice", command=self.lock_dice, font=("Arial", 17, "bold")
        )
        # Label to show points accumulated during the turn
        self.turn_points_label = customtkinter.CTkLabel(
            self, text="Turn points: 0", font=("Arial", 17, "bold")
        )
        self.default_text_color = self.turn_points_label.cget("text_color")

        # Place the control buttons and label within the grid layout
        self.roll_button.grid(
            column=1,
            row=1,
            rowspan=2,
            padx=(0, 10),
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
            column=0,
            row=1,
            padx=10,
            pady=(0, 10),
            sticky="nsew",
        )
        self.turn_points_label.grid(
            column=0,
            row=2,
            padx=10,
            pady=(0, 10),
            sticky="nsew",
        )

    # -------------------------------------------------------------------------
    # Game Setup & Player Management Methods
    # -------------------------------------------------------------------------
    def start_game(self, player_list):
        """Begins the game by showing the main window and initializing players."""

        self.deiconify()  # Make the main window visible

        # Store the list of players and set up their UI elements
        self.player_list = player_list

        for player in player_list:
            self.load_player(player)

        # Highlight the current active player
        self.highlight_current_player()

        logging.info(
            "Starting game with players: "
            + ", ".join([player.name for player in player_list])
        )

    def load_player(self, player):
        """Creates the UI elements to display a player's name and score."""

        player_name = player.name

        logging.info(f"Loading player: {player_name}")

        # Create a frame for the player's information within the player panel
        player_frame = customtkinter.CTkFrame(self.player_holder_frame)
        player_frame.grid_columnconfigure((0, 1), weight=1)
        player_frame.grid_rowconfigure(0, weight=1)
        player_frame.grid(column=0, padx=10, pady=(10, 0), sticky="ew")

        # Display the player's name
        player_label = customtkinter.CTkLabel(
            player_frame, text=player_name, font=("Arial", 14, "bold")
        )
        player_label.grid(column=0, row=0)

        # Display the player's points
        points_label = customtkinter.CTkLabel(
            player_frame, text=player.points, font=("Arial", 14, "bold")
        )
        player_frame.points_label = points_label
        points_label.grid(column=1, row=0)

        # Save the frame reference for future updates (like score changes)
        self.player_frame_list.append(player_frame)

    def update_points(self):
        """Refreshes the score labels for all players."""

        for i, player in enumerate(self.player_list):
            self.player_frame_list[i].points_label.configure(text=player.points)

    def highlight_current_player(self):
        """Visually indicates which player is currently active."""

        # Reset the highlight of the previous player
        self.player_frame_list[
            (self.current_player - 1) % len(self.player_list)
        ].configure(fg_color=["gray81", "gray20"])

        # Highlight the current player's frame in green
        self.player_frame_list[self.current_player].configure(fg_color="green")

    # -------------------------------------------------------------------------
    # Dice Rolling & Locking Methods
    # -------------------------------------------------------------------------
    def roll_dice(self):
        """Rolls the unlocked dice and updates the UI with the results."""

        logging.info("Attempting to roll dice")

        if self.dice_locked:
            self.dice_rolled = True

            # Roll dice for each unlocked die
            self.current_rolls = functions.dice_rolls(len(self.unlocked_dice))

            # Update each die's display with its new value
            for i, dice in enumerate(self.unlocked_dice):
                dice.roll = self.current_rolls[i]
                dice.configure(text=dice.roll)

            logging.debug(f"Dice rolled with values: {self.current_rolls}")

            # If no dice score any points, automatically end the turn
            if functions.points_calc(self.current_rolls) == 0:
                logging.info(
                    "No scoring dice rolled; turn points reset to 0 and ending turn"
                )

                self.turn_points = 0
                self.end_turn()

            else:
                # Allow player to select dice to lock for scoring
                self.dice_locked = False

        else:
            # Inform the user that they must lock at least one die before re-rolling
            logging.warning(
                "Dice roll prevented: No dice locked. Please lock at least one die."
            )

            CTkMessagebox(
                self,
                title="Error",
                message="Please lock at least one die!",
                icon="warning",
                font=("Arial", 14, "bold"),
            )

    def lock_dice(self):
        """Locks dice based on user selection and updates points for locked dice."""

        if self.dice_rolled:
            logging.info("Locking selected dice")

            self.unlocked_dice = []  # Prepare list for dice that will remain unlocked
            self.rolls_to_score = (
                []
            )  # Prepare list for dice that are locked for scoring

            locked_die = False  # Flag to indicate if at least one die was locked

            # Check each checkbox to determine whether to lock its corresponding die
            for i, checkbox in enumerate(self.checkbox_list):
                if checkbox.cget("state") == "normal" and checkbox.get() == 0:
                    # Keep this die unlocked for the next roll
                    self.unlocked_dice.append(self.dice_list[i])

                elif checkbox.cget("state") == "normal" and checkbox.get() == 1:
                    # Lock this die and mark its value for scoring
                    locked_die = True
                    checkbox.configure(state="disabled")
                    self.dice_list[i].configure(bg_color=self.default_text_color)
                    self.rolls_to_score.append(self.dice_list[i].roll)

            if locked_die:
                logging.info(f"Locked dice values: {self.rolls_to_score}")

                self.calculate_turn_points()

                # Allow dice to be rolled again only if they are unlocked
                self.dice_locked = True

                # If no unlocked dice left end turn
                if len(self.unlocked_dice) == 0:
                    self.end_turn()

        else:
            # Alert the user if they try to lock dice before any roll
            logging.warning("Lock dice attempted without rolling dice first")

            CTkMessagebox(
                self,
                title="Error",
                message="Can't lock unrolled dice!",
                icon="warning",
                font=("Arial", 14, "bold"),
            )

    def calculate_turn_points(self):
        """Calculates points for the current turn based on the locked dice values."""

        points = functions.points_calc(self.rolls_to_score)

        logging.debug(
            f"Calculating turn points. Current turn points: {self.turn_points}, points from roll: {points}"
        )

        self.turn_points += points
        self.turn_points_label.configure(text=f"Turn points: {self.turn_points}")

    # -------------------------------------------------------------------------
    # Turn End & Reset Methods
    # -------------------------------------------------------------------------
    def end_turn(self):
        """Ends the current turn, updates scores, and resets the board for the next player."""

        if self.dice_rolled:
            if self.dice_locked:
                # Update the current player's total points with the turn's accumulated points
                self.player_list[self.current_player].add_points(self.turn_points)
                self.update_points()

                # Check for win conditions or trigger the final round if needed
                self.check_winner()

                logging.info(
                    f"Ending turn for player {self.player_list[self.current_player].name} with turn points: {self.turn_points}"
                )

                # Move to the next player in a cyclic order
                self.current_player = (self.current_player + 1) % len(self.player_list)
                self.highlight_current_player()

                # Reset turn-specific variables and UI elements for the next turn
                self.turn_points = 0
                self.reset_board()
                self.dice_rolled = False

                # Close the game window if a winner has been declared
                if self.winner_found:
                    self.destroy()

            else:
                # Warn if a player tries to end their turn without locking any dice
                logging.warning("End turn attempt failed: No dice locked for scoring")

                CTkMessagebox(
                    self,
                    title="Error",
                    message="Please lock at least one die!",
                    icon="warning",
                    font=("Arial", 14, "bold"),
                )

        else:
            # Warn if a player tries to end their turn without having rolled the dice
            logging.warning("End turn attempt failed: Dice have not been rolled yet")

            CTkMessagebox(
                self,
                title="Error",
                message="Can't end turn with unrolled dice!",
                icon="warning",
                font=("Arial", 14, "bold"),
            )

    def reset_checkboxes(self):
        """Resets all checkboxes to be selectable and unselected for the new turn."""

        for checkbox in self.checkbox_list:
            checkbox.configure(state="normal")
            checkbox.deselect()

    def reset_dice(self):
        """Clears the dice display back to the default placeholder."""

        for dice in self.dice_list:
            dice.configure(text="-", bg_color="transparent")

    def reset_board(self):
        """Resets the game board UI for the next turn."""

        self.reset_checkboxes()
        self.reset_dice()
        self.lock_dice()  # Resets the dice locking state
        self.turn_points_label.configure(text="Turn points: 0")

    # -------------------------------------------------------------------------
    # Winning Condition Check Method
    # -------------------------------------------------------------------------
    def check_winner(self):
        """Determines if the game has been won and announces the winner if conditions are met."""

        if self.final_round:
            # If in final round, check if the turn rotation has returned to the player who initiated it
            if (self.current_player + 1) % len(self.player_list) == self.final_player:
                winner = functions.find_winner(self.player_list)

                logging.info(
                    f"Winner determined: {winner.name} with {winner.points} points"
                )

                winner_message = CTkMessagebox(
                    self,
                    title="Winner",
                    message=f"The winner is: {winner.name} with {winner.points} points!",
                    icon="check",
                    font=("Arial", 14, "bold"),
                )
                winner_message.get()
                self.winner_found = True

        elif self.player_list[self.current_player].points >= 10000:
            # If a player's score reaches or exceeds 10,000 points, start the final round
            logging.info(
                f"Final round initiated by player {self.player_list[self.current_player].name}"
            )

            self.final_round = True
            self.final_player = self.current_player


class Sidekick(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        # if _internal exists look for icon in it, else look in base
        icon_path = (
            Path(__file__).parent.parent / "_internal"
            if (Path(__file__).parent.parent / "_internal").exists()
            else Path(__file__).parent.parent / "res"
        ) / "icon.ico"
        self.after(200, lambda: self.iconbitmap(icon_path))

        # Initialize variables to manage player entry
        self.player_list = []  # List to hold player objects
        self.starting_game = False  # Flag to indicate if the game has been started

        self.title("Sidekick")
        self.geometry("220x400")
        self.resizable(False, False)

        # Set up grid configuration for this window
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Build the UI for player entry and control buttons
        self._create_interface()

        # Ensure proper cleanup when the window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        logging.info("Sidekick window opened")

    # -------------------------------------------------------------------------
    # Sidekick UI and Player Management Methods
    # -------------------------------------------------------------------------
    def _create_interface(self):
        """Constructs the UI components for player entry and game start."""

        self.player_holder_frame = customtkinter.CTkFrame(self)
        self.player_holder_frame.grid_columnconfigure(0, weight=1)
        self.player_holder_frame.grid_propagate(False)
        self.player_holder_frame.grid(
            column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

        # Input field for entering a player's name
        self.name_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter Player name"
        )
        self.name_entry.grid(
            column=0, row=1, columnspan=2, padx=10, pady=(0, 10), sticky="nsew"
        )

        # Button to add the player based on the entered name
        self.add_player_button = customtkinter.CTkButton(
            self, text="Add player", command=self.add_player, font=("Arial", 14, "bold")
        )
        self.add_player_button.grid(
            column=0, row=2, padx=10, pady=(0, 10), sticky="nsew"
        )

        # Button to start the game; initially disabled until there are at least 2 players
        self.start_game_button = customtkinter.CTkButton(
            self,
            text="Start game",
            command=self.start_game,
            fg_color="red",
            hover_color="#0a5c0d",
            text_color_disabled="#DCE4EE",
            state="disabled",
            font=("Arial", 14, "bold"),
        )
        self.start_game_button.grid(
            column=1, row=2, padx=(0, 10), pady=(0, 10), sticky="nsew"
        )

    def add_player(self):
        """Adds a new player to the game if a valid name is provided."""

        player_name = self.name_entry.get().strip()

        if player_name and len(self.player_list) < 6:
            # Clear the input field after adding the player
            self.name_entry.delete(0, customtkinter.END)

            new_player = Player(player_name)
            self.player_list.append(new_player)

            # Create a frame in the sidekick window to display the new player's info
            player_frame = customtkinter.CTkFrame(self.player_holder_frame)
            player_frame.grid_columnconfigure(0, weight=1)
            player_frame.grid_columnconfigure(1, weight=0)
            player_frame.grid_rowconfigure(0, weight=1)
            player_frame.grid(column=0, padx=10, pady=(10, 0), sticky="ew")

            # Show the player's name
            player_label = customtkinter.CTkLabel(
                player_frame, text=player_name, font=("Arial", 14, "bold")
            )
            player_label.grid(column=0, row=0)

            # Button to allow removal of the player if needed
            delete_button = customtkinter.CTkButton(
                player_frame,
                width=10,
                text="X",
                command=lambda f=player_frame, p=new_player: self.delete_player(f, p),
                font=("Arial", 14, "bold"),
            )
            delete_button.grid(column=1, row=0, sticky="e")

            # Update the state of the start game button based on number of players
            self.update_start_button_state()

            logging.info(
                f"Added player: {player_name}. Total players: {len(self.player_list)}"
            )

    def delete_player(self, frame, player):
        """Removes a player from the list and updates the UI."""

        self.player_list.remove(player)
        frame.destroy()

        logging.info(
            f"Deleted player: {player.name}. Total players remaining: {len(self.player_list)}"
        )

        self.update_start_button_state()

    def update_start_button_state(self):
        """Enables the start button when at least 2 players are added; disables it otherwise."""

        if len(self.player_list) >= 2:
            self.start_game_button.configure(fg_color="green", state="normal")
        else:
            self.start_game_button.configure(fg_color="red", state="disabled")

    def start_game(self):
        """Initiates the game by sending the player list to the main game window and closing sidekick."""

        self.starting_game = True

        logging.info("Starting game from Sidekick interface")

        self.master.start_game(self.player_list)
        self.destroy()

    def on_close(self):
        """Handles the window close event by exiting the game if the game hasn't been started."""

        if not self.starting_game:
            logging.info("Sidekick closed without starting game. Exiting application")

            self.master.destroy()


if __name__ == "__main__":
    main()
    app = Game()
    app.mainloop()
