from typing import List
from html_update_checker.user import User
from html_update_checker.homepage import Homepage
from html_update_checker.episode import EpisodeParser

class TestUser:

    def test_user_object_creation(self):
        email = "testuser@testmail.com"
        user = User(email)

class TestUserHomepageNotifications:

    def test_add_homepage_notifications_single_homepage(self):
        from tests.test_episode import EpisodeParserForTests
        
        user = User("testuser@testmail.com")

        homepage = Homepage("www.test.com",EpisodeParserForTests)
        user.add_homepage_notifications(homepage)
        assert user.homepages[homepage.url] == homepage
    
    def test_add_homepage_notifications_multiple_homepages(self):
        from tests.test_episode import EpisodeParserForTests
        
        user = User("testuser@testmail.com")

        homepage1 = Homepage("www.test1.com",EpisodeParserForTests)
        homepage2 = Homepage("www.test2.com",EpisodeParserForTests)
        homepages = [homepage1,homepage2]
        user.add_homepage_notifications(homepages)
        
        assert len(user.homepages) == len(homepages)
        for homepage in homepages:
            assert homepage in user.homepages.values()
    
    def test_remove_homepage_notifications_single_homepage(self):
        from tests.test_episode import EpisodeParserForTests
        
        user = User("testuser@testmail.com")

        homepage = Homepage("www.test.com",EpisodeParserForTests)
        user.add_homepage_notifications(homepage)
        user.remove_homepage_notifications(homepage)
        
        assert len(user.homepages) == 0
    
    def test_remove_homepage_notifications_multiple_homepages(self):
        from tests.test_episode import EpisodeParserForTests
        
        user = User("testuser@testmail.com")

        homepage1 = Homepage("www.test1.com",EpisodeParserForTests)
        homepage2 = Homepage("www.test2.com",EpisodeParserForTests)
        homepages = [homepage1,homepage2]
        user.add_homepage_notifications(homepages)
        user.remove_homepage_notifications(homepages)

        assert len(user.homepages) == 0