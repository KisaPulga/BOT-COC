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
from bot_coc.features import FarmMDO

farmMDO = FarmMDO.FarmMDO()

view = View()
bot = Bot(farmMDO)

controller = Controller(view,bot)
controller.RunProg()