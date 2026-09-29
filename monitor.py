import psutil
import time
from plyer import notification
from storage import load_config, load_usage_data, save_usage_data, get_today_key

def get_running_target_processes(monitored_apps):
    running = {}
    monitored_lower = {name.lower(): name for name in monitored_apps}

    for proc in psutil.process_iter(['name']):
        name = proc.info['name']
        if name and name.lower() in monitored_lower:
            original_name = monitored_lower[name.lower()]
            running[original_name] = proc
    return running

def kill_process(proc, app_name):
    
    try:
        proc.kill()
        print(f"Killed {app_name} (time limit exceeded)")
    except psutil.NoSuchProcess:
        pass
    except Exception as e:
        print(f"Error while killing {app_name}: {e}")

    try:
        notification.notify(
            title="Daily_Use_Organizer",
            message=f"{app_name} was closed because you exceeded your daily time limit",
            timeout=5
        )
    except Exception as e:
        print(f"Notification failed (ignored): {e}")

def monitor_loop(stop_event=None):
    
    config = load_config()
    monitored_apps = config["monitored_apps"]
    interval = config["poll_interval_sec"]

    blocked_today = set()

    print("Monitoring:", list(monitored_apps.keys()))

    while True:
      if stop_event is not None and stop_event.is_set():
          print("Monitoring stopped")
          break

      try:
          data = load_usage_data()
          today = get_today_key()
          today_data = data.get(today, {})

          running = get_running_target_processes(monitored_apps)

          for app, proc in running.items():
              if app in blocked_today:
                  kill_process(proc, app)
                  continue

              today_data[app] = today_data.get(app, 0) + interval
              limit_sec = monitored_apps[app] * 60
              print(f"{app}: {today_data[app]}s / limit {limit_sec}s")

              if today_data[app] >= limit_sec:
                  blocked_today.add(app)
                  kill_process(proc, app)

          data[today] = today_data
          save_usage_data(data)
      except Exception as e:
          print(f"[monitor_loop] Unexpected error: {e}")

    time.sleep(interval)
if __name__ == "__main__":
    monitor_loop()