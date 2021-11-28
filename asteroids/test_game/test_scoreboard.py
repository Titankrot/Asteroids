import pytest
import json
from asteroids import scoreboard
import os.path
from mock import Mock, patch, MagicMock
import asteroids.screen
from asteroids.screen import PYGAME


pygame = PYGAME

filename = os.path.join("asteroids", "test_game", "score.dat")
pygame.init()
@pytest.fixture()
def reset_score_dat(request):
    score = scoreboard.Scores(filename)
    pygame.init()

    def resource_teardown():
        score.save()
    request.addfinalizer(resource_teardown)


def test_escape():
    scoretable = scoreboard.ScoreTable(filename, 0)
    scoretable.update(pygame.K_ESCAPE)
    assert not scoretable.is_work


def test_input(reset_score_dat):
    scoretable = scoreboard.ScoreTable(filename, 51)
    scoretable.update(pygame.K_t)
    scoretable.update(pygame.K_k)
    scoretable.update(pygame.K_BACKSPACE)
    scoretable.update(pygame.K_e)
    scoretable.update(pygame.K_s)
    scoretable.update(pygame.K_t)
    scoretable.update(pygame.K_RETURN)
    assert scoretable.is_work
    scoretable.update(pygame.K_RETURN)
    scores = scoretable.scores.get_score()
    for i in scores:
        print(i)
    score = scores[1]
    assert not scoretable.is_work
    assert 51 == score[1]
    assert "test" == score[0]


def test_draw():
    def blit():
        pass
    scoretable = scoreboard.ScoreTable(filename, 0)
    mock_window = Mock()
    mock_window.take(blit)
    pygame.display.set_mode((1, 1))
    scoretable.draw(mock_window, pygame.Surface((1, 1)), 0)
    assert 3 == mock_window.blit.call_count
    scoretable.is_name_accept = True
    scoretable.draw(mock_window, pygame.Surface((1, 1)), 0)
    assert 8 == mock_window.blit.call_count
