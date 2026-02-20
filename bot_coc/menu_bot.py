###############################
###############################
###                         ###        
###   BOT CLASH OF CLANS    ###
###          BY             ###
###       KISAPULGA         ###
###                         ###
###############################
###############################

from controller import Controller
from view import View
from bot import Bot
from features import farm_mdo_all_pc

farmMDO = farm_mdo_all_pc.FarmMDO()

view = View()
bot = Bot(farmMDO)

controller = Controller(view,bot)
controller.RunProg()