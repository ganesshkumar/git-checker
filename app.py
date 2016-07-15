from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram_helper import send_message
from contribution_checker import did_contribute

scheduler = None
skip_hours = [i for i in xrange(1,15)]

def init_scheduler():
    global scheduler
    scheduler = BlockingScheduler()
    scheduler.daemonic = False

def start_checker():
    scheduler.add_job(notify_contribution, 'interval', seconds=60)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

def notify_contribution():
    today = datetime.today()

    if today.time().minute is not 0 or today.time().hour in skip_hours:
        return

    # Will be reached only on the 0th minute of non skip hours
    if not did_contribute(today.date()):
        message = "You haven\'t contributed for the day";
    else:
        message = "You have contributed for the day. Keep it up!"
    print "Sending message: " + message
    send_message(message)
    print '\n'

if __name__ == "__main__":
    print "Staring git-checker"
    init_scheduler()
    start_checker()
