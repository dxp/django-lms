from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import libs.test_utils as test_utils
from alerts.models import Alert
from alerts.tasks import alert_userlist

class AlertTest(test_utils.AuthenticatedTest):
    def test_acknowlege(self):
        """
        Tests the user acknowledgeing and deleteing an alert
        """

        # Create the alert
        alert = Alert.objects.create(sent_by = 'Tester',
                                     sent_to = self.user,
                                     title = 'Test title',
                                     details = 'No details',
                                     level = 'Notice',)
        
        self.c.post(reverse('alerts:acknowledge'), {'pk':alert.id})

        with self.assertRaises(Alert.DoesNotExist):
            Alert.objects.get(id = alert.id)
        
    def test_alert_all(self):
        """
        Tests the ability of the system to alert all users
        """

        # Create a load of users
        for i in range(0, 100):
            User.objects.create(username = 'user_%s' %(i))

        users = User.objects.all()

        # Create the alert
        alert = Alert(sent_by = 'Tester',
                      title = 'Test title',
                      details = 'No details',
                      level = 'Notice',)

        alert_userlist(alert, users)

        self.assertEquals(len(Alert.objects.all()), len(User.objects.all()))
        
