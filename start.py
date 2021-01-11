import time
import schedule
from decouple import config
from html_update_checker.user import User
from html_update_checker.homepage import Homepage
from html_update_checker.episode_parser_implementations.dragonball_super_anime import DragonballSuperAnimeEpisodeParser

#################################
#   Create users to be notified #
#################################
user = User(config("USER_EMAIL"))

#########################
#   Create homepages    #
#########################
dragonball_super_anime = Homepage("https://dragonball-tube.com/dragonball-super-episoden-streams", DragonballSuperAnimeEpisodeParser)

#################################
#   Register user for updates   #
#################################
user.add_homepage_notifications(dragonball_super_anime)

#################################################
#   Regularly fetch episodes and notify users   #
#################################################
def update_episodes_and_notify_users():
    for homepage in Homepage.homepages.values():
        homepage.episodes_update()
    user.send_updates()

schedule.every(1).hour.do(update_episodes_and_notify_users)

while True:
    schedule.run_pending()
    time.sleep(60)
