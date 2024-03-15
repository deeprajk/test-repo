import datetime
import boto3

def lambda_handler(event, context):
    # Get the current date
    today = datetime.date.today()

    # Find the 2nd Tuesday of the month
    second_tuesday = today.replace(day=1)
    while second_tuesday.weekday() != 1:  # 1 represents Tuesday
        second_tuesday += datetime.timedelta(days=1)
    second_tuesday += datetime.timedelta(days=7)  # Move to the 2nd Tuesday

    # Calculate the Thursday after the 2nd Tuesday
    thursday_after_second_tuesday = second_tuesday + datetime.timedelta(days=2)

    # Check if it falls on the 2nd or 3rd Thursday
    if thursday_after_second_tuesday.day <= 14:  # 2nd Thursday
        enable_schedule = 'Schedule A'
        disable_schedule = 'Schedule B'
    else:  # 3rd Thursday
        enable_schedule = 'Schedule B'
        disable_schedule = 'Schedule A'

    # Enable and disable schedules in EventBridge
    client = boto3.client('events')

    # Disable the current enabled schedule
    client.disable_rule(Name=disable_schedule)

    # Enable the new schedule
    client.enable_rule(Name=enable_schedule)

    return {
        'statusCode': 200,
        'body': f'Enabled {enable_schedule} and disabled {disable_schedule}'
    }
