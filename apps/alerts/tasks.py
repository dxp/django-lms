from celery.decorators import task

@task()
def alert_userlist(alert, userlist):
    """
    This takes a mostly complete alert (minus the sent_to) and applies it to all the users in the list
    """

    for user in userlist:
        # Set the id to None to create a new alert
        alert.id = None
        alert.sent_to = user
        alert.save()
