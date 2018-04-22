from configparser import ConfigParser

config = ConfigParser()

# parse existing file
config.read('config.ini')

SERVER = config.get('Login', 'SERVER')
USER = config.get('Login', 'USER')
PASSWORD = config.get('Login', 'PASSWORD')
__HTTP = 'http://'

# urls
LOGIN_PAGE = config.get('Login', 'LOGIN_PAGE')
MAIN_PAGE = __HTTP + SERVER + '/game/index.php'
OVERVIEW_PAGE = MAIN_PAGE + '?page=overview'
RESOURCE_PAGE = MAIN_PAGE + '?page=resources'
STATION_PAGE = MAIN_PAGE + '?page=station'
RESEARCH_PAGE = MAIN_PAGE + '?page=research'
SHIPYARD_PAGE = MAIN_PAGE + '?page=shipyard'
DEFENSE_PAGE = MAIN_PAGE + '?page=defense'
FLEET_PAGE = MAIN_PAGE + '?page=fleet1'
GALAXY_PAGE = MAIN_PAGE + '?page=galaxy'

#  building pages
METAL_MINE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=1'
CRYSTAL_MINE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=2'
DEUTERIUM_MINE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=3'
SOLAR_URL = MAIN_PAGE + '?page=resources&ajax=1&type=4'
FUSION_URL = MAIN_PAGE + '?page=resources&ajax=1&type=12'
METAL_STORAGE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=22'
CRYSTAL_STORAGE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=23'
DEUTERIUM_STORAGE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=24'
HIDDEN_METAL_STORAGE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=25'
HIDDEN_CRYSTAL_STORAGE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=26'
HIDDEN_DEUTERIUM_STORAGE_URL = MAIN_PAGE + '?page=resources&ajax=1&type=27'

ROBOTICS = MAIN_PAGE + 'page=station&ajax=1&type=14'
SHIPYARD = MAIN_PAGE + 'page=station&ajax=1&type=21'
RESEARCH_LAB = MAIN_PAGE + 'page=station&ajax=1&type=31'

# regex
# resources
FIND_RESOURCE_ACT_CAP_PROD = '."{name}":."resources":."actualFormat":"[0-9\.]+","actual":[0-9]+,"max":[0-9]+,"production":[0-9\.]+.'
FIND_ENERGY = '"energy":."resources":."actual":.{0,1}[0-9]+,"actualFormat":".{0,1}[0-9\.]+"'

# buildings
FIND_COST = '"[\w]+ tooltip" title="[0-9\.]+'
FIND_LEVEL = '<span class="level">.{1,20}[0-9]+.{1,20}<span class="'
FIND_ENERGYCOST = '<span class="time">.{0,30}[0-9\.]+'
FIND_DURATION = '<span class="time" id="buildDuration">.{1,20}[0-9\.]*.{1,5}[0-9\.]*.{1,5}[0-9\.]*'
FIND_BUILDING_LINK = 'sendBuildRequest.{0,300}, null, 1'
FIND_ACTUAL_BUILDING_TIME = "new bauCountdown.getElementByIdWithCache..'b_supply.{1,3}.'.,[0-9]*,[0-9]*"

# planets
FIND_PLANET_IMAGE = '<div id="planet" style="background.image.url.{0,300}\)">'

# universe
FIND_UNIVERSE_SPEED = '"ogame-universe-speed" content="."'
FIND_UNIVERSE_SPEED_FLEET = '"ogame-universe-speed-fleet" content="."'

# header dict
HEADERS_DICT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

# helper methodes
def return_int_if_exists(value, index):
    try:
        x = int(value[index])
    except IndexError:
        x = 0
    except TypeError:
        print('Could not convert value to int!')
        x = None
    return x
