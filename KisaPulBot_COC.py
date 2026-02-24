###############################
###############################
###                         ###        
###   BOT CLASH OF CLANS    ###
###          BY             ###
###       KISAPULGA         ###
###                         ###
###############################
###############################

from bot_coc.controller import Controller
from bot_coc.view import View
from bot_coc.bot import Bot

view = View()
bot = Bot()


controller = Controller(view,bot)
controller.RunProg()