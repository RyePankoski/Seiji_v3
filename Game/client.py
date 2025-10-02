import pygame.display
from Util.constants import *
from Game.board import Board
from Game.tray import Tray
from Render.sound_manager import SoundManager
from Game.piece import Piece
from Render.background import Background
from Util.util import *


class Client:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_desktop_sizes()[0]
        self.board_rect = pygame.Rect(0, 0, LINE_LENGTH, LINE_LENGTH)
        self.board = Board(self.screen, self.board_rect)
        self.trays = []
        self.init_trays()
        self.selected_piece_from_tray = None
        self.selected_piece_on_board = None
        self.placed_monarch = False
        self.back_ground = Background(self.screen)

    def run(self, mouse_pos):
        if mouse_pos is not None:
            self.handle_board_click(mouse_pos)
            self.handle_tray_click(mouse_pos)
            self.board.check_for_promotions()

        self.back_ground.run()
        self.render_calls()

    def handle_tray_click(self, mouse_pos):
        for tray in self.trays:
            result = tray.get_clicked_slot(*mouse_pos)
            if result is not None:
                piece, player = result
                self.selected_piece_from_tray = piece, player
                self.board.selected_tray_piece_player = player
                SoundManager.play_sound("pick_up")
                return

        self.selected_piece_from_tray = None
        self.board.selected_tray_piece_player = None

    def handle_board_click(self, mouse_pos):
        board_cell = self.board.get_clicked_slot(*mouse_pos)

        if board_cell is None:
            if self.selected_piece_on_board is not None:
                SoundManager.play_sound("de_select")
            self.selected_piece_on_board = None
            self.board.selected_piece_on_board = None
            return

        cell_x, cell_y = board_cell

        # If we have a piece selected and click on a new square, move it there.
        if self.selected_piece_on_board is not None:

            piece = self.selected_piece_on_board
            valid_moves = self.board.get_valid_moves(piece)

            if (cell_x, cell_y) == (piece.cx, piece.cy):
                SoundManager.play_sound("de_select")
                self.selected_piece_on_board = None
                self.board.selected_piece_on_board = None
                return

            if (cell_x, cell_y) not in valid_moves:
                SoundManager.play_sound("error")
                self.selected_piece_on_board = None
                self.board.selected_piece_on_board = None
                return

            prev_cell_x, prev_cell_y = piece.cx, piece.cy

            # See if we are trying to move a piece to an occupied slot.
            if has_val_at_key(self.board.pieces, (cell_x, cell_y)):
                other_piece = self.board.pieces[(cell_x, cell_y)]

                if piece.player == other_piece.player:
                    return
                elif piece.piece_type == "advisor" and not piece.is_promoted:
                    return
                else:
                    SoundManager.play_sound("capture")
                    for tray in self.trays:
                        if tray.player == piece.player:
                            tray.pieces.append(other_piece.piece_type)

            # Update piece position
            piece.cx = cell_x
            piece.cy = cell_y

            del self.board.pieces[(prev_cell_x, prev_cell_y)]
            self.board.pieces[(cell_x, cell_y)] = piece
            SoundManager.play_sound("slide")
            self.selected_piece_on_board = None
            self.board.selected_piece_on_board = None
            return

        # Check to see if we are clicking on a piece on the board
        if has_val_at_key(self.board.pieces, (cell_x, cell_y)):
            piece = self.board.pieces[(cell_x, cell_y)]
            self.selected_piece_on_board = piece
            self.board.selected_piece_on_board = piece
            SoundManager.play_sound("select_piece")
            return

        # Early return if we have no tray piece selected
        if self.selected_piece_from_tray is None:
            return

        # If we have a tray piece selected, try to place it where there is nothing on the board.
        if not has_val_at_key(self.board.pieces, (cell_x, cell_y)):
            piece_type, player = self.selected_piece_from_tray
            valid_placement_squares = self.board.get_valid_placement_squares(player)

            # Ensure that the first piece placed is the monarch
            if not self.placed_monarch and piece_type != "monarch":
                SoundManager.play_sound("error")
                self.selected_piece_from_tray = None
                return

            if (cell_x, cell_y) in valid_placement_squares or piece_type == "monarch" or piece_type == "spy":
                self.board.pieces[(cell_x, cell_y)] = Piece(cell_x, cell_y, piece_type, player)

                if piece_type == "monarch":
                    self.placed_monarch = True

                # Update the trays to reflect the change
                for tray in self.trays:
                    if tray.player == player:
                        tray.pieces.remove(piece_type)

                self.selected_piece_from_tray = None
                SoundManager.play_sound("place")
            else:
                SoundManager.play_sound("error")

    def init_trays(self):
        player_1_tray = Tray(
            self.board_rect.right + 20,
            self.board_rect.top,
            600,
            400,
            1
        )

        player_2_tray = Tray(
            self.board_rect.right + 20,
            self.board_rect.bottom - 400,
            600,
            400,
            2
        )

        self.trays.append(player_1_tray)
        self.trays.append(player_2_tray)

    def render_calls(self):
        self.board.draw()
        for tray in self.trays:
            tray.draw(self.screen)
