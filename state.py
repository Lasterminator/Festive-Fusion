import json

class GameMemento:
    def __init__(self, level, player_score, player_health, level_data):
        self._level = level
        self._player_score = player_score
        self._player_health = player_health
        self._level_data = level_data

    def get_state(self):
        return {
            'level': self._level,
            'player_score': self._player_score,
            'player_health': self._player_health,
            'level_data': self._level_data
        }

class GameCaretaker:
    def __init__(self):
        self._mementos = []
        self._current = -1

    def backup(self, memento):
        self._mementos.append(memento)
        self._current = len(self._mementos) - 1

    def undo(self):
        if self._current > 0:
            self._current -= 1
            return self._mementos[self._current]
        return None

    def get_current_memento(self):
        if self._current >= 0:
            return self._mementos[self._current]
        return None

    def save_to_file(self, filename='save_game.json'):
        if self._current >= 0:
            state = self._mementos[self._current].get_state()
            with open(filename, 'w') as f:
                json.dump(state, f, indent=4)

    def load_from_file(self, filename='save_game.json'):
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            
            memento = GameMemento(
                level=state.get('level', 1),
                player_score=state.get('player_score', 0),
                player_health=state.get('player_health', 100),
                level_data=state.get('level_data', {})
            )
            self.backup(memento)
            return memento
        except FileNotFoundError:
            return None