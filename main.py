import logging
from dota2gsipy.server import GSIServer
import time
import winsound
import sys

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    # Initialize server
    logger.info("Starting GSI Server...")
    server = GSIServer(("localhost", 4000), "TOKENHERE")
    server.start_server()
    logger.info("GSI Server started successfully")

    def play_alert():
        try:
            winsound.Beep(1000, 500)
        except:
            logger.error("Could not play sound alert")

    def convert_to_seconds(clock_time):
        try:
            if clock_time is None:
                return 0
            minutes, seconds = map(int, clock_time.split(':'))
            return minutes * 60 + seconds
        except:
            return 0

    def should_alert(clock_time):
        seconds = convert_to_seconds(clock_time)
        if seconds == 105:  # 1:45
            return True
        if seconds > 105 and (seconds - 105) % 120 == 0:
            return True
        return False

    last_alert_time = 0
    logger.info("Starting main loop...")

    while True:
        try:
            clock_time = server.game_state.map.clock_time
            
            if clock_time:
                logger.debug(f"Current game time: {clock_time}")
                
            if clock_time and should_alert(clock_time):
                current_time = time.time()
                if current_time - last_alert_time >= 1:
                    play_alert()
                    logger.info(f"Alert triggered at game time: {clock_time}")
                    last_alert_time = current_time
            
            time.sleep(0.1)
            
        except AttributeError:
            # Game state might not be available yet
            time.sleep(0.1)
            continue
        except KeyboardInterrupt:
            logger.info("Program terminated by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            time.sleep(0.1)
            continue

except Exception as e:
    logger.error(f"Failed to start: {str(e)}")
    input("Press Enter to exit...")  # This will keep the window open