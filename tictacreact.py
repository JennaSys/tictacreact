# Reference: https://reactjs.org/tutorial/tutorial.html

from pyreact import Component, render, element


def square(props):
    return element('button', {'className': 'square', 'onClick': props.onClick}, props.value, )


class Board(Component):
    def render_square(self, i):
        return element(square, {'value': self.props['squares'][i], 'onClick': lambda: self.props['onClick'](i)})

    def render(self):
        rows = []
        for row in range(3):
            new_row = []
            for col in range(3):
                new_row.append(self.render_square((row * 3) + col))
            rows.append(element('div', {'className': 'board-row'}, *new_row))

        return element('div', None, *rows)


class Game(Component):
    def __init__(self, props):
        super().__init__(props)

        self.state = {
            'history': [{
                'squares': [None for _ in range(9)],
            }],
            'stepNumber': 0,
            'xIsNext': True,
        }

    @staticmethod
    def copy_list(old_list, dict_key):
        # Deep copy of list containing dictionaries with single entry
        new_list = []
        for dict_entry in old_list:
            new_list.append({dict_key: dict_entry[dict_key][:]})
        return new_list

    def handle_click(self, i):
        new_history = self.copy_list(self.state['history'][:self.state['stepNumber'] + 1], 'squares')
        history = self.state['history'][:self.state['stepNumber'] + 1]
        current = history[len(history) - 1]
        new_squares = current['squares']

        if calculate_winner(new_squares) or (new_squares[i] is not None):
            return
        new_squares[i] = 'X' if self.state['xIsNext'] else 'O'

        new_history.append({'squares': new_squares})
        self.setState({
            'history': new_history,
            'stepNumber': len(history),
            'xIsNext': not self.state['xIsNext'],
        })

    def jump_to(self, step):
        self.setState({
            'stepNumber': step,
            'xIsNext': (step % 2) == 0,
        })

    def get_move(self, move):
        desc = ('Go to move #' + str(move)) if move > 0 else 'Go to game start'
        return element('li', {'key': move},
                       element('button', {'className': 'move-history', 'onClick': lambda: self.jump_to(move)}, desc)
                       )

    def render(self):
        history = self.state['history'][:]
        current = history[self.state['stepNumber']]
        winner = calculate_winner(current['squares'])
        moves = [self.get_move(move) for move in range(len(history))]

        if winner is not None:
            status = 'Winner: {}'.format(winner)
        elif self.state['stepNumber'] == 9:
            status = 'No Winner'
        else:
            status = 'Next player: {}'.format('X' if self.state['xIsNext'] else 'O')

        return element('div', {'className': 'game'},
                       element('div', {'className': 'game-board'},
                               element(Board, {
                                   'squares': current['squares'],
                                   'onClick': lambda i: self.handle_click(i),
                               }),
                               element('div', {'className': 'game-status'}, status),
                               ),
                       element('div', {'className': 'game-info'}, 'Move History',
                               element('ol', None, moves),
                               ),

                       )


# Render the component in a 'container' div
render(Game, None, 'root')


def calculate_winner(squares):
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    for i, line in enumerate(lines):
        a, b, c = line
        if (squares[a] is not None) and (squares[a] == squares[b]) and (squares[a] == squares[c]):
            return squares[a]
    return None
