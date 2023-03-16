# -*- coding: utf-8 -*-


import arcade

from . import constants
from . import globals
from .components.position import Position
from .exceptions import InvalidGameState
from .pathfinding import Pathfinder
from .sprite_tracker import SpriteTracker
from .states import State


class Game(arcade.Window):
    """Main game class."""

    def __init__(
        self,
        width,
        height,
        title,
        grid,
        beings,
    ):
        super().__init__(width, height, title)
        self.x = 0
        self.y = 0
        self.background_color = arcade.color.DARK_BLUE_GRAY
        self.grid = grid
        self.beings = beings
        self.pathfinder = Pathfinder(self.grid)
        self.active_player = None
        self.sprite_tracker = SpriteTracker(self.beings, self.grid)
        # first_frame and initialized are hacks to allow removing from the spritelists.
        # Will be removed when stuff like main menu will be implemented - that way, window will be spawned and
        # GPU resources allocated long time before removing sprites.
        self.first_frame = True
        self.initialized = False

    def on_draw(self):
        self.clear()
        self.grid.sprite_list.draw()
        self.grid.map_objects.sprite_list.draw()
        self.beings.player_sprite_list.draw()
        self.beings.enemy_sprite_list.draw()
        self.sprite_tracker.draw()
        if self.first_frame:
            self.first_frame = False
            self.initialized = True

    def on_key_press(self, key, modifiers):
        # TODO: TESTING ONLY, remove later!
        if globals.state == State.ENEMY_TURN:
            return
        if key == arcade.key.ENTER:
            if globals.state == State.MOVE:
                globals.state = State.TARGET
            else:
                globals.state = State.MOVE
        elif key == arcade.key.SPACE and globals.state == State.PLAY:
            globals.state = State.ENEMY_TURN

    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y
        # TODO: Probably safe for removal, but more testing is necessary.

    #        if self.active_player:
    #            target_position = Position(x, y).return_px_to_cell()
    #            self.pathfinder.set_up_path_grid(self.beings)
    #            self.pathfinder.find_path(self.active_player.cell_position, target_position)

    def on_mouse_press(self, x, y, button, modifiers):
        if globals.state == State.ENEMY_TURN:
            return
        player_under_cursor = self.beings.find_player_by_px_position(x, y)
        # Possible clicks: MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT
        # Possible states: State.PLAY, State.MOVE, State.TARGET
        # Possible modifiers (not these passed as argument to this method, mind!):
        #     - not / player is active
        #     - not / player_under_cursor
        #     - active player is (not) player_under_cursor
        #     - active player moved or attacked already
        if button == arcade.MOUSE_BUTTON_LEFT:
            if globals.state == State.PLAY:
                if not self.active_player:
                    if player_under_cursor and not player_under_cursor.moved:
                        # Select player under the cursor if not currently active
                        # and set mode to MOVE if active_player did not move yet this turn.
                        self.active_player = player_under_cursor
                        self.active_player.active = True
                        globals.state = State.MOVE
                    elif (
                        player_under_cursor
                        and player_under_cursor.moved
                        and not player_under_cursor.attacked
                    ):
                        # Select player under the cursor if not currently active
                        # and set mode to TARGET if active player already moved, but did not attack yet
                        self.active_player = player_under_cursor
                        self.active_player.active = True
                        globals.state = State.TARGET
                    else:
                        # Do nothing if player being that is being clicked on already moved and attacked this turn.
                        # TODO: Add some kind of "info screen" so one still could see some info about player being
                        #       being selected.
                        pass
                else:
                    # Should not be possible. When there is active player, game needs to be in MOVE or TARGET state.
                    # ...maybe unless player just attacked, and still is selected but has no actions left?
                    # Need to think this over.
                    raise InvalidGameState(
                        "When there is active player game needs to be in MOVE or TARGET state, but it is in PLAY state."
                    )
            elif globals.state == State.MOVE:
                if self.active_player:
                    if player_under_cursor:
                        if self.active_player is player_under_cursor:
                            if not self.active_player.attacked:
                                globals.state = State.TARGET
                            elif self.active_player.attacked:
                                # Should not be possible. If active_player already attacked, it can not be in MOVE mode.
                                raise InvalidGameState(
                                    "If active player already attacked, it can not be in MOVE mode."
                                )
                        elif self.active_player is not player_under_cursor:
                            # Deselect currently selected player being if another player being is being clicked on.
                            self.active_player.active = False
                            self.active_player = None
                            if not player_under_cursor.moved:
                                # Activate newly selected player being and set it in MOVE mode
                                # if not moved yet this turn.
                                self.active_player = player_under_cursor
                                self.active_player.active = True
                                globals.state = State.MOVE
                            elif not player_under_cursor.attacked:
                                # Activate newly selected player being and set it in TARGET MODE
                                # if already moved but did not attack this turn yet.
                                self.active_player = player_under_cursor
                                self.active_player.active = True
                                globals.state = State.TARGET
                            else:
                                # Do nothing if clicked player being already attacked and moved this turn.
                                pass
                    elif not player_under_cursor:
                        if not self.active_player.moved:
                            if self.pathfinder.last_path:
                                # Move active player that not moved yet to desired cell.
                                # Use the pathfinder coords at the position equal to player range.
                                # If not possible (because path is shorter), use the last coords in path.
                                # Last coords in path are equal to mouse position in cell_position, if hovered
                                # over the available tile.
                                try:
                                    self.active_player.move_to(
                                        self.pathfinder.last_path[
                                            self.active_player.range
                                        ][0],
                                        self.pathfinder.last_path[
                                            self.active_player.range
                                        ][1],
                                    )
                                except IndexError:
                                    self.active_player.move_to(
                                        self.pathfinder.last_path[-1][0],
                                        self.pathfinder.last_path[-1][1],
                                    )
                                finally:
                                    self.pathfinder.last_path = ()
                                    # TODO: Currently it makes sense to set player into TARGET mode after every move,
                                    #       but in future I want to equip every player being in multiple attacks.
                                    #       Will this fit?
                                    globals.state = State.TARGET
                        elif self.active_player.moved:
                            # Do not allow to move player that already moved during this turn.
                            pass
                else:
                    # Should not be possible. If game is in MOVE mode (or TARGET, for that matter), a player being
                    # must be active.
                    raise InvalidGameState(
                        "If game is in MOVE mode, a player being must be active."
                    )
            elif globals.state == State.TARGET:
                if self.active_player:
                    if self.active_player.attacked:
                        # Should not be possible. After attack player should be deselected and game mode set to PLAY.
                        raise InvalidGameState(
                            "Player that already attacked can not be active."
                        )
                    elif not self.active_player.attacked:
                        # Perform attack if possible.
                        try:
                            self.active_player.attack.perform(
                                self.beings, self.grid.map_objects, x, y
                            )
                        except TypeError:
                            pass  # Catch-all exception for attacks.
                        finally:
                            # After attack, deselect the player since moving unit is not forbidden after attack.
                            globals.state = State.PLAY
                            self.active_player.active = False
                            self.active_player = None
                else:
                    raise InvalidGameState(
                        "If game is in TARGET mode, a player being must be active."
                    )
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if globals.state == State.PLAY:
                pass
            elif globals.state == State.MOVE:
                if self.active_player and self.active_player.active:
                    self.active_player.active = False
                    self.active_player = None
                    globals.state = State.PLAY
                else:
                    # Should not be possible. If game is in MOVE state, then a player being must be active.
                    raise InvalidGameState(
                        "If game is in MOVE state, a player being must be active."
                    )
            elif globals.state == State.TARGET:
                if self.active_player and self.active_player.active:
                    if self.active_player.moved:
                        # Deselect player and return game to the PLAY state if active_player already moved.
                        self.active_player.active = False
                        self.active_player = None
                        globals.state = State.PLAY
                    else:
                        # Switch game state to MOVE
                        globals.state = State.MOVE
                else:
                    # Should not be possible. If game is in MOVE state, then a player being must be active.
                    raise InvalidGameState(
                        "If game is in TARGET state, a player being must be active."
                    )

    def on_update(self, delta_time):
        if globals.state == State.GENERATE_MAP and self.initialized:
            self.grid.generate_map()
            globals.state = State.PLAY
            for i in range(constants.PLAYER_BEINGS_NO):
                self.beings.spawn_player_being()
            for i in range(constants.ENEMY_BEINGS_INITIAL_NO):
                self.beings.spawn_enemy_being()
        if self.initialized:
            self.active_player = self.beings.find_active_player()
            if self.active_player is None:
                self.pathfinder.last_path = ()
                if globals.state != State.ENEMY_TURN:
                    globals.state = State.PLAY
            mouse_position = Position(self.x, self.y).return_px_to_cell()
            self.sprite_tracker.mouse_position = mouse_position
            self.sprite_tracker.player = self.active_player
            self.sprite_tracker.track()
            # Remove dead enemies on_update before checking for enemy turn
            # allows to apply environmental effect before the enemy can act.
            for enemy in self.beings.enemy_beings:
                if enemy.hp <= 0:
                    self.beings.remove_enemy_being(enemy)
            if globals.state == State.ENEMY_TURN:
                for enemy in self.beings.enemy_beings:
                    print(
                        f"enemy at {enemy.cell_position.x}, {enemy.cell_position.y} acts..."
                    )
                    enemy.ai.gather_map_info(self.grid, self.beings)
                    # TODO: Act, using enemy.ai.info data as weighted average.
                globals.state = State.PLAY
                for player in self.beings.player_beings:
                    player.moved = False
                    player.attacked = False
                print("player's turn")
