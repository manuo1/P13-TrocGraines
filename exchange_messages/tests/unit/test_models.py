from unittest import mock

from django.db.utils import Error
from django.test import TestCase

from exchange_messages.models import ExchangeMessageManager
from exchange_messages.text_constants import DELETED_MSG, GLOBAL_ERROR_MSG


class ExchangeMessagesModelsUnitTest(TestCase):
    def setUp(self):
        class MockUser:
            def __init__(self):
                self.username = 'testusername'
                self.email = 'testemail'
                self.password = 'testpassword'

        class MockExchangeMessage:
            def __init__(self):
                self.recipient = MockUser()
                self.subject = 'subject'
                self.message = 'message'
                self.sending_date = 'date'

            def save(self):
                pass

        class MockDiscussion:
            def __init__(self):
                self.sender = MockUser()
                self.exchange_message = MockExchangeMessage()

            def delete(self):
                pass

            def save(self):
                pass

        class MockDiscussionError:
            def __init__(self):
                self.sender = MockUser()
                self.exchange_message = MockExchangeMessage()

            def delete(self):
                raise Error

            def save(self):
                raise Error

        class MockFilter:
            def __init__(self):
                pass

            def order_by(self, test):
                discussions = 'discussion'
                return discussions

        self.filter = MockFilter()
        self.test_discussion = MockDiscussion()
        self.test_discussion_e = MockDiscussionError()
        self.exchange_message_manager = ExchangeMessageManager()
        self.exchange_message = MockExchangeMessage()
        self.discussion = MockDiscussion()
        self.exchange_message_data = {
            'recipient': MockUser(),
            'sender': MockUser(),
            'subject': 'subject',
            'message': 'message',
        }

    def test_delete_discussion_discussions_success(self):
        with mock.patch(
            'exchange_messages.models.get_object_or_404',
            return_value=self.test_discussion,
        ):
            messages = self.exchange_message_manager.delete_discussion('1234')
            self.assertTrue(messages == [{40: DELETED_MSG}])

    def test_delete_discussion_discussions_error(self):
        with mock.patch(
            'exchange_messages.models.get_object_or_404',
            return_value=self.test_discussion_e,
        ):
            messages = self.exchange_message_manager.delete_discussion('1234')
            self.assertTrue(messages == [{40: GLOBAL_ERROR_MSG}])

    def test_get_user_discussions(self):

        with mock.patch(
            'exchange_messages.models.Discussion.objects.filter',
            return_value=self.filter,
        ):
            discussions = self.exchange_message_manager.get_user_discussions(
                '1234'
            )
            self.assertTrue('discussion' in discussions)

    def test_save_exchange_message_succes(self):
        with mock.patch(
            'exchange_messages.models.ExchangeMessage',
            return_value=self.exchange_message,
        ):
            with mock.patch(
                'exchange_messages.models.Discussion',
                return_value=self.discussion,
            ):

                with mock.patch(
                    'django.db.models.Model.save', return_value=True
                ):
                    value = (
                        self.exchange_message_manager.save_exchange_message(
                            **self.exchange_message_data
                        )
                    )
                    self.assertTrue(value)

    def test_save_exchange_message_error(self):
        with mock.patch(
            'exchange_messages.models.ExchangeMessage',
            return_value=self.exchange_message,
        ):
            with mock.patch(
                'exchange_messages.models.Discussion',
                return_value=self.test_discussion_e,
            ):

                with mock.patch(
                    'django.db.models.Model.save', return_value=True
                ):
                    value = (
                        self.exchange_message_manager.save_exchange_message(
                            **self.exchange_message_data
                        )
                    )
                    self.assertFalse(value)
