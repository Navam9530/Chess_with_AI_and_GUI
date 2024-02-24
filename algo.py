# Importing the Necessary Libraries
import chess as ch
import random as rd

class Search:

    # Class Parameters
    def __init__(self, bd, ai_level, human_color):
        self.bd = bd
        self.ai_level = ai_level
        self.human_color = human_color

    # Our pieces should be more on the board
    def get_piece_score(self, box):
        if self.bd.piece_type_at(box) == ch.PAWN:
            piece_score = 1
        elif self.bd.piece_type_at(box) == ch.KNIGHT:
            piece_score = 3.2
        elif self.bd.piece_type_at(box) == ch.BISHOP:
            piece_score = 3.33
        elif self.bd.piece_type_at(box) == ch.ROOK:
            piece_score = 5.1
        elif self.bd.piece_type_at(box) == ch.QUEEN:
            piece_score = 8.8
        else:
            piece_score = 0

        if self.bd.color_at(box) == self.human_color:
            return -piece_score
        else:
            return piece_score
    
    # We should not get mated but he should
    def get_mate_chance(self):
        if self.bd.legal_moves.count() == 0:
            if self.bd.turn == self.human_color:
                return 999
            else:
                return -999
        else:
            return 0
    
    # Getting the total weights of each node at the bottom level
    def get_total_score(self):
        total_score = 0
        for i in range(64):
            total_score += self.get_piece_score(ch.SQUARES[i])
        total_score += self.get_mate_chance() + rd.random()
        return total_score
    
    # Applying Min-Max Algorithm with Alpha-Beta Pruning Optimisation Technique
    def min_max(self, candidate, depth):
        if depth == self.ai_level or self.bd.legal_moves.count() == 0:
            return self.get_total_score()
        else:
            legal_moves = list(self.bd.legal_moves)
            new_candidate = None
            if depth % 2 != 0:
                new_candidate = float('-inf')
            else:
                new_candidate = float('inf')
            for i in legal_moves:
                self.bd.push(i)
                value = self.min_max(new_candidate, depth + 1)
                if (value > new_candidate) and (depth % 2 != 0): #type: ignore
                    new_candidate = value
                    if depth == 1:
                        move = i
                elif (value < new_candidate) and (depth % 2 == 0): #type: ignore
                    new_candidate = value
                if (candidate != None) and (value < candidate) and (depth % 2 == 0):
                    self.bd.pop()
                    break
                elif (candidate != None) and (value > candidate) and (depth % 2 != 0):
                    self.bd.pop()
                    break
                self.bd.pop()
            if depth > 1:
                return new_candidate
            else:
                return move #type: ignore
