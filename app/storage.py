from apscheduler.schedulers.background import BackgroundScheduler
import os
import time

def cleanup_temp_files():
    folder = '/path/to/temp/files'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        # If the file is more than an hour old, delete it
        if os.path.getmtime(file_path) < time.time() - 1 * 3600:
            os.remove(file_path)

scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_temp_files, 'interval', hours=1)
scheduler.start()