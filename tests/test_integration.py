from html_update_checker import (
    Homepage,
    User
)

from html_update_checker.episode_parser_implementations import DragonballSuperAnimeEpisodeParser

class TestIntegration:
    def test_integration(self):
        user = User("test@test.com")
        user.add_homepage_notifications(Homepage("http://dragonball-tube.com/dragonball-super-episoden-streams", DragonballSuperAnimeEpisodeParser, "Dragonball Super Anime"))
