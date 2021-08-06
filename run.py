import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from scraper import create_app
from update_tickers import ut
from yfinance import yf


app = create_app()

sched = BackgroundScheduler(daemon=True)
sched.add_job(lambda: ut(app), 'cron', hour=4)
sched.add_job(lambda: yf(app), 'interval', seconds=300)
sched.start()

@atexit.register
def close():
    print('Shutting down background tasks ...')
    sched.shutdown(wait=False)
    print('Success!')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
