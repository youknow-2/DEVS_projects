import random

from SimulationEngine.ClassicDEVS.DEVSAtomicModel import DEVSAtomicModel
from modeling.messages.ball import Ball


INF = float('inf')

PLAYER_A = 'Player A'
PLAYER_B = 'Player B'


def get_opponent_of_player(player):
    if player == PLAYER_A:
        return PLAYER_B
    elif player == PLAYER_B:
        return PLAYER_A


class Referee(DEVSAtomicModel):

    def __init__(self, ID):
        super().__init__(ID)

        self.addStateVariable('state', 'INIT')

        self.addInputPort('ball_from_players')

        self.addOutputPort('ball_to_player_A')
        self.addOutputPort('ball_to_player_B')
        
        self.match: Match
        self.ball: Ball

    def funcExternalTransition(self, strPort, event):
        state = self.getStateValue('state')
        if state == 'INIT':
            pass
        elif state == 'SERVE_ALLOCATTION':
            pass
        elif state == 'WAIT':
            if strPort == 'ball_from_players':
                self.ball = event
                self.setStateValue('state', 'JUDGEMENT')
        elif state == 'JUDGEMENT':
            pass
        elif state == 'GAMEOVER':
            pass

    def funcOutput(self):
        state = self.getStateValue('state')
        if state == 'INIT':
            pass
        elif state == 'SERVE_ALLOCATTION':
            next_server = self.match.get_current_server()
            outputPort = self.getOutputPortForPlayer(next_server)
            self.addOutputEvent(outputPort, Ball() )
            print(1)
        elif state == 'WAIT':
            pass
        elif state == 'JUDGEMENT':
            pass
        elif state == 'GAMEOVER':
            pass

    def funcInternalTransition(self):
        state = self.getStateValue('state')
        if state == 'INIT':
            first_server = random.choice([PLAYER_A, PLAYER_B])
            self.match = Match(first_server)
            self.setStateValue('state', 'SERVE_ALLOCATTION')
        elif state == 'SERVE_ALLOCATTION':
            self.setStateValue('state', 'WAIT')
        elif state == 'WAIT':
            pass
        elif state == 'JUDGEMENT':
            self.match.judgement(self.ball)
            if self.match.is_ended():
                self.match.analysis()
                self.setStateValue('state', 'GAMEOVER')
            else:
                self.setStateValue('state', 'SERVE_ALLOCATTION')
        elif state == 'GAMEOVER':
            pass

    def funcTimeAdvance(self):
        state = self.getStateValue('state')
        if state == 'INIT':
            return 0
        elif state == 'SERVE_ALLOCATTION':
            return 0
        elif state == 'WAIT':
            return INF
        elif state == 'JUDGEMENT':
            return 0
        elif state == 'GAMEOVER':
            return INF
        self.ball.attack_power

    def funcSelect(self):
        pass
    
    def getOutputPortForPlayer(self, player):
        if player == PLAYER_A:
            return 'ball_to_player_A'
        elif player == PLAYER_B:
            return 'ball_to_player_B'
    
    
class Match():
    
    def __init__(self, first_server):
        self.match_score = {PLAYER_A:0, PLAYER_B:0}
        self.match_over = False
        self.games = []
        self.start_new_game(first_server)
        
    def start_new_game(self, first_server):
        game_number = len(self.games) + 1
        self.current_game = self.Game(game_number, first_server)
        self.games.append(self.current_game)
        
    def judgement(self, ball:Ball):
        self.current_game.judgement(ball)
        if self.current_game.is_ended():
            self.match_score_judgement()
            if self.is_ended():
                pass
            else:
                current_first_server = self.get_first_server()
                new_first_server = get_opponent_of_player(current_first_server)
                self.start_new_game(new_first_server)
        
    def match_score_judgement(self):
        game_winner = self.current_game.get_game_winner()
        self.match_score[game_winner] += 1
        if self.match_score[game_winner] == 4:
            self.match_winner = game_winner
            self.match_over = True
            
    def is_ended(self):
        return self.match_over
        
    def get_first_server(self):
        return self.current_game.get_first_server()
    
    def get_current_server(self):
        return self.current_game.get_current_server()
    
    def analysis(self):
        game: Match.Game
        for game in self.games:
            game.analysis()
        self.log_match_score()
        
    def log_match_score(self):
            print('[Match]')
            print('(Player A) {0:>2} : {1:>2} (Player B)'.format(
                self.match_score[PLAYER_A], 
                self.match_score[PLAYER_B]
                ))
            print()

    class Game():
        
        WIDTH_OF_LOG_LINE = 81
        
        def __init__(self, game_number, first_server):
            self.game_number = game_number
            self.score = {PLAYER_A:0, PLAYER_B:0}
            self.total_serve_miss = {PLAYER_A:0, PLAYER_B:0}
            self.total_serve_miss_score = {PLAYER_A:0, PLAYER_B:0}
            self.total_receive_failure = {PLAYER_A:0, PLAYER_B:0}
            self.first_server = first_server
            self.current_server = first_server
            self.game_over = False
            self.is_deuce = False
            self.init_serve_count()
            self.log_game_separator()
            
        def judgement(self, ball: Ball):
            self.score_judgement(ball)
            self.game_judgement()
            
        def score_judgement(self, ball: Ball):
            if ball.is_serve_miss():
                self.serve_miss_count += 1
                self.total_serve_miss[self.current_server] += 1
                if self.serve_miss_count == 2:
                    self.serve_count += 1
                    self.serve_miss_count = 0
                    self.total_serve_miss_score[self.current_server] += 1
                    scorer = get_opponent_of_player(self.current_server)
                    self.add_score(scorer)
            else:
                self.serve_count += 1
                self.serve_miss_count = 0
                scorer = ball.get_scorer()
                self.add_score(scorer)
                self.total_receive_failure[ball.failed_player] += 1

        def add_score(self, scorer):
            self.score[scorer] += 1
            self.update_to_next_server()
            self.log_score()
            self.log_score_separator()
            
        def update_to_next_server(self):
            if self.should_change_server():
                self.init_serve_count()
                next_server = get_opponent_of_player(self.current_server)
                self.current_server = next_server

        def should_change_server(self):
            if self.is_deuce:
                return self.serve_count == 1
            else:
                return self.serve_count == 2
            
        def init_serve_count(self):
            self.serve_count = 0
            self.serve_miss_count = 0

        def game_judgement(self):
            if self.is_deuce:
                if self.score[PLAYER_A] - self.score[PLAYER_B] == 2:
                    self.end_of_game(PLAYER_A)
                elif self.score[PLAYER_B] - self.score[PLAYER_A] == 2:
                    self.end_of_game(PLAYER_B)
                else:
                    pass
            else:
                if self.score[PLAYER_A] == 11:
                    self.end_of_game(PLAYER_A)
                elif self.score[PLAYER_B] == 11:
                    self.end_of_game(PLAYER_B)
                elif self.score[PLAYER_A] == self.score[PLAYER_B] == 10:
                    self.is_deuce = True
                else:
                    pass

        def end_of_game(self, winner):
            self.game_winner = winner
            self.game_over = True
            print('\n')
            
        def is_ended(self):
            return self.game_over
        
        def get_game_winner(self):
            return self.game_winner
            
        def get_current_server(self):
            return self.current_server
        
        def get_first_server(self):
            return self.first_server
        
        def analysis(self):
            print('[Game %d]' % self.game_number)
            self.log_score()
            self.log_analysis_of_player(PLAYER_A)
            self.log_analysis_of_player(PLAYER_B)
            print()
            
        def log_game_separator(self):
            separator = f'{{0:=^{self.WIDTH_OF_LOG_LINE}}}'
            str_game = ' Game %d ' % self.game_number
            print(separator.format(str_game))
            
        def log_score(self):
            print('(Player A) {0:>2} : {1:>2} (Player B)'.format(
                self.score[PLAYER_A], 
                self.score[PLAYER_B]
                ))
        
        def log_score_separator(self):
            print('-' * self.WIDTH_OF_LOG_LINE)
            
        def log_analysis_of_player(self, player):
            serve_miss = self.total_serve_miss[player]
            serve_miss_score = self.total_serve_miss_score[player]
            receive_fail = self.total_receive_failure[player]
            print(player + ' missed serve : %d' % serve_miss)
            print(player + ' missed serve (score) : %d' % serve_miss_score)
            print(player + ' failed to receive : %d' % receive_fail)