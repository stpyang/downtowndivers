'''Copyright 2020 Downtown Divers New York. All Rights Reserved.'''

from django.conf import settings

from googleapiclient.discovery import build


CALENDAR_ID = 'gizmo.santore@gmail.com'

google_service = build('calendar', 'v3', credentials=settings.GOOGLE_CREDENTIALS)
