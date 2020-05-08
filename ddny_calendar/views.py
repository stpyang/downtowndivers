'''Copyright 2020 DDNY. All Rights Reserved.'''

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ddny_calendar.google_service import google_service, CALENDAR_ID
from ddny.decorators import consent_required


def __fullcalendar_event_to_google_event(request):
    '''
        https://fullcalendar.io/docs/event-object
        https://developers.google.com/calendar/v3/reference/events
    '''

    event_summary = request.POST.get('title')
    event_start = {
        'dateTime': request.POST.get('start'),
        'timeZone': 'America/New_York',
    }
    event_end = {
        'dateTime': request.POST.get('end'),
        'timeZone': 'America/New_York',
    }
    if request.POST.get('all_day') == 'true':
        event_start = {
            'date': request.POST.get('start'),
            'timeZone': 'America/New_York',
        }
        event_end = {
            'date': request.POST.get('end'),
            'timeZone': 'America/New_York',
        }
    return {
        'summary': event_summary,
        'start': event_start,
        'end': event_end,
    }


@csrf_exempt
@consent_required
@login_required
def add_event(request):
    '''add an event'''
    try:
        event = __fullcalendar_event_to_google_event(request)
        returned_event = google_service.events().insert(
            calendarId=CALENDAR_ID, body=event
        ).execute()
        return JsonResponse({'id': returned_event['id'], 'success': True})
    except ValidationError as exception:
        return JsonResponse({'success': False, 'error': str(exception)})


@csrf_exempt
@consent_required
@login_required
def update_event(request):
    '''update an event'''
    try:
        event_id = request.POST.get('id')
        event = google_service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()
        updated_event = __fullcalendar_event_to_google_event(request)
        event['summary'] = updated_event['summary']
        event['start'] = updated_event['start']
        event['end'] = updated_event['end']
        returned_event = google_service.events().update(
            calendarId=CALENDAR_ID, eventId=event_id, body=event
        ).execute()
        return JsonResponse({'id': returned_event['id'], 'success': True})
    except (ObjectDoesNotExist, ValidationError) as exception:
        return JsonResponse({'success': False, 'error': str(exception)})


@csrf_exempt
@consent_required
@login_required
def delete_event(request):
    '''delete an event'''
    try:
        event_id = request.POST.get('id')
        google_service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        return JsonResponse({'success': True})
    except ObjectDoesNotExist as exception:
        return JsonResponse({'success': False, 'error': str(exception)})
