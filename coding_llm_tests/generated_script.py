import datetime

# Get today's date
today = datetime.datetime.now()

# Check if today is a weekday (Monday to Friday)
if today.weekday() < 5:  # Monday is 0 and Sunday is 6
    print("Hello, it's a weekday")
else:
    print("Hello, it's the weekend")