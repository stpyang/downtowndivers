'''Copyright 2016 DDNY. All Rights Reserved.'''

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class TankWarningEmail(EmailMultiAlternatives):
    ''' A friendly automated message about tanks
        with old or missing hydro/vip data'''
    def __init__(self, blender):
        self.blender = blender
        self.text_content = get_template("fillstation/tank_warning.txt")
        self.html_content = get_template("fillstation/tank_warning.html")
        self.warnings = []
        self.warning_number = 1
        self.cc = []
        if blender != settings.TANK_NAZI:
            self.cc = [blender]
        super(TankWarningEmail, self).__init__(
            subject="DDNY automated warning: hydro/vip",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.TANK_NAZI],
            cc=self.cc,
        )

    def add(self,
            tank_code,
            psi_start,
            psi_end,
            gas_name,
            service,
            service_date):
        '''add one warning about tank misuse'''
        self.warnings += ({
            "tank_code": tank_code,
            "psi": int(psi_end) - int(psi_start),
            "gas_name": gas_name,
            "service": service,
            "service_date": service_date,
        },)

    def send(self, fail_silently=False):
        '''https://docs.djangoproject.com/en/2.2/topics/email/'''
        context = {
            "blender": self.blender,
            "warnings": self.warnings,
        }
        self.body = self.text_content.render(context)
        html = self.html_content.render(context)
        self.attach_alternative(html, "text/html")
        super(TankWarningEmail, self).send(fail_silently)
