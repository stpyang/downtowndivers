'''Copyright 2016 DDNY. All Rights Reserved.'''

import functools

from django.urls import reverse

from registration.factory import RandomUserFactory, MemberFactory


def test_login_required(path):
    '''decorator to test the login_required decorator'''
    def _login_required_decorator(test_function):
        '''decorator to test the login_required decorator'''
        @functools.wraps(test_function)
        def wrapper(self): #pylint: disable=unused-variable
            '''decorator to test the login_required decorator'''
            self.client.logout()
            response = self.client.get(path)
            self.assertRedirects(
                response,
                expected_url="signin/?next=" + path,
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True,
            )
        return test_function
    return _login_required_decorator


# TODO(stpyang): fix
def test_consent_required(path):
    '''decorator to test the consent_required decorator'''
    def _consent_required_decorator(test_function):
        '''decorator to test the consent_required decorator'''
        @functools.wraps(test_function)
        def wrapper(self): #pylint: disable=unused-variable
            '''decorator to test the consent_required decorator'''
            user = RandomUserFactory.create()
            member = MemberFactory.create(user=user)
            self.assertTrue(
                self.client.login(
                    username=member.username,
                    password="password",
                )
            )
            response = self.client.get(path)
            self.assertRedirects(
                response,
                expected_url=reverse("consent_form"),
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True,
            )
            self.client.logout()
        return test_function
    return _consent_required_decorator
