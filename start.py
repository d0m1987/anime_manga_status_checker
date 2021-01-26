import time
import schedule
from decouple import config
from html_update_checker.user import User
from html_update_checker.homepage import Homepage
from html_update_checker.episode_parser_implementations.mediaitem import MediaitemEpisodeParser
from html_update_checker.episode_parser_implementations.sagatable import SagatableEpisodeParser

#################################
#   Create users to be notified #
#################################
user = User(config("USER_EMAIL"))

#################################
#   Register user for updates   #
#################################
user.add_homepage_notifications([
    Homepage("https://dragonball-tube.com/dragonball-super-episoden-streams", MediaitemEpisodeParser),
    Homepage("http://dragonball-tube.com/dragonball-super-mangaliste", MediaitemEpisodeParser),
    Homepage("http://dragonball-tube.com/galactic-patrol-mangaliste", MediaitemEpisodeParser),
    Homepage("https://onepiece-tube.com/episoden-streams", MediaitemEpisodeParser),
    Homepage("https://onepiece-tube.com/kapitel-mangaliste", SagatableEpisodeParser),
    Homepage("http://fairytail-tube.org/episoden-streams", MediaitemEpisodeParser),
    Homepage("http://fairytail-tube.org/100-years-quest-mangaliste", MediaitemEpisodeParser),
    Homepage("http://fairytail-tube.org/edens-zero-mangaliste", MediaitemEpisodeParser),
    Homepage("http://naruto-tube.org/boruto-episoden-streams", MediaitemEpisodeParser),
    Homepage("http://naruto-tube.org/boruto-kapitel-mangaliste", MediaitemEpisodeParser),
])

#################################################
#   Regularly fetch episodes and notify users   #
#################################################
def update_episodes_and_notify_users():
    for homepage in Homepage.homepages.values():
        homepage.episodes_update()
    user.send_updates()

schedule.every(1).minute.do(update_episodes_and_notify_users)

while True:
    try:
        schedule.run_pending()
    except Exception as e:
        print(e)
    print("Successfully ran checks")
    time.sleep(60)
