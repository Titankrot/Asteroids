import json
import os.path
from asteroids.screen import PYGAME


pygame = PYGAME


class Scores:
    def __init__(self, filename):
        self._filename = filename
        if not os.path.exists(filename):
            with open(filename, 'x') as f:
                json.dump({}, f)
        with open(filename) as f:
            self._scores = json.load(f)

    def add_score(self, score, name):
        if name in self._scores.keys():
            if score > self._scores[name]:
                self._scores[name] = score
        if len(self._scores) < 10:
            self._scores[name] = score
        else:
            for i in self._scores.keys():
                if self._scores[i] < score:
                    self._scores[name] = score
                    score = self._scores.pop(i)
                    name = i

    def save(self):
        with open(self._filename, 'w') as f:
            json.dump(self._scores, f)

    def get_score(self):
        return sorted([(i, self._scores[i]) for i in self._scores],
                      key=lambda x: x[1], reverse=True)


class ScoreTable:
    def __init__(self, filename, new_score):
        self._filename = filename
        self.scores = Scores(filename)
        self.new_score = new_score
        self.is_name_accept = False
        self.is_work = True
        self.name = ""
        self.score_font = pygame.font.SysFont('arial', 25, 1, 1)

    def update(self, symbol):
        if symbol == pygame.K_ESCAPE:
            self.is_work = False
        elif not self.is_name_accept:
            if symbol == pygame.K_RETURN:
                self.scores.add_score(name=self.name, score=self.new_score)
                self.is_name_accept = True
            elif symbol == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif symbol == pygame.K_SPACE:
                self.name += " "
            else:
                self.name += pygame.key.name(symbol)
        elif symbol == pygame.K_RETURN:
            self.scores.save()
            self.is_work = False

    def draw(self, window, bg, bg_x):
        window.blit(bg, (bg_x, 0))
        i = 2
        if not self.is_name_accept:
            window.blit(
                self.score_font.render(
                    str.format("Your name:{0}",
                               self.name),
                    False, [255, 255, 255]), (10, 10 + 25 * i))
            i += 1
            window.blit(
                self.score_font.render(
                    str.format("Your score:{0}", self.new_score),
                    False, [255, 255, 255]), (10, 10 + 25 * i))
        else:
            window.blit(
                self.score_font.render(
                    str.format("Names:....Scores:"),
                    False, [255, 255, 255]), (10, 10))
            scores = self.scores.get_score()
            for couple in scores:
                window.blit(
                    self.score_font.render(
                        str.format("{0}....{1}", couple[0], couple[1]),
                        False, [255, 255, 255]), (10, 10 + 25 * i))
                i += 1
            i += 2
        pygame.display.update()
