import requests

URL = "url"

HEADERS = {
  'Authorization': 'Bearer <access key>'
}

PRIORITY_ORDER = {
    "placement": 1,
    "result":    2,
    "event":     3
}

nval = int(input("Enter value of n"))

def fetch_notifications():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("notifications", [])


def get_priority_score(notification):
    notification_type = notification.get("Type", "").lower()
    return PRIORITY_ORDER.get(notification_type, 999)


def get_priority_inbox(notifications, top_n=nval):
    known_types = set(PRIORITY_ORDER.keys())
    filtered = [
        n for n in notifications
        if n.get("Type", "").lower() in known_types
    ]
    sorted_notifications = sorted(
        filtered,
        key=lambda n: (get_priority_score(n), n.get("Timestamp", ""))
    )
    return sorted_notifications[:top_n]


def display_priority_inbox(top_notifications):
    print(f"Priority inbox ")
    

    if not top_notifications:
        print("  No notifications found.")
        return

    for rank, notif in enumerate(top_notifications, start=1):
        notif_type = notif.get("Type", "Unknown")
        message    = notif.get("Message", "No message")
        timestamp  = notif.get("Timestamp", "N/A")
        priority   = get_priority_score(notif)

        print(f"\n   [{notif_type}]  (Priority Level: {priority})")
        print(f"Message   : {message}")
        print(f"Timestamp : {timestamp}")



if __name__ == "__main__":
    all_notifications = fetch_notifications()
    print(f"Fetched {len(all_notifications)} notifications from API.\n")

    inbox = get_priority_inbox(all_notifications, top_n=nval)
    display_priority_inbox(inbox) 
