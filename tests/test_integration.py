from html_update_checker import (
    Homepage,
    User
)

from html_update_checker.episode_parser_implementations import MediaitemEpisodeParser

class TestIntegration:
    def test_integration(self):
        import start
        import schedule
        
        user = User("test@test.com")
        user.add_homepage_notifications(Homepage("http://dragonball-tube.com/dragonball-super-episoden-streams", MediaitemEpisodeParser, "Dragonball Super Anime"))
        schedule.run_all()