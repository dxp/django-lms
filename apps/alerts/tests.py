from django.core.urlresolvers import reverse

import libs.test_utils as test_utils
from alerts.models import Alert

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
        
