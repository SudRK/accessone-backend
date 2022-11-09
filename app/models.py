# -*- encoding: utf-8 -*-
"""
"""
from django.conf import settings
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from dateutil import tz
# from PIL import Image, ImageDraw

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


from datetime import datetime
import datetime
from django.utils.timezone import localtime
from time import strftime
import re

from datetime import timedelta

from django.utils.timezone import get_fixed_timezone, utc

import uuid 


from django.contrib.auth.hashers import make_password

import random
import pytz
from pathlib import Path
import os
import json

from app.utils import getTime, splitat




# date_re = re.compile(
#     r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$'
# )

# time_re = re.compile(
#     r'(?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
#     r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
# )

# datetime_re = re.compile(
#     r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
#     r'[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
#     r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
#     r'(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$'
# )

# standard_duration_re = re.compile(
#     r'^'
#     r'(?:(?P<days>-?\d+) (days?, )?)?'
#     r'((?:(?P<hours>-?\d+):)(?=\d+:\d+))?'
#     r'(?:(?P<minutes>-?\d+):)?'
#     r'(?P<seconds>-?\d+)'
#     r'(?:\.(?P<microseconds>\d{1,6})\d{0,6})?'
#     r'$'
# )

# # Support the sections of ISO 8601 date representation that are accepted by
# # timedelta
# iso8601_duration_re = re.compile(
#     r'^(?P<sign>[-+]?)'
#     r'P'
#     r'(?:(?P<days>\d+(.\d+)?)D)?'
#     r'(?:T'
#     r'(?:(?P<hours>\d+(.\d+)?)H)?'
#     r'(?:(?P<minutes>\d+(.\d+)?)M)?'
#     r'(?:(?P<seconds>\d+(.\d+)?)S)?'
#     r')?'
#     r'$'
# )

# # Support PostgreSQL's day-time interval format, e.g. "3 days 04:05:06". The
# # year-month and mixed intervals cannot be converted to a timedelta and thus
# # aren't accepted.
# postgres_interval_re = re.compile(
#     r'^'
#     r'(?:(?P<days>-?\d+) (days? ?))?'
#     r'(?:(?P<sign>[-+])?'
#     r'(?P<hours>\d+):'
#     r'(?P<minutes>\d\d):'
#     r'(?P<seconds>\d\d)'
#     r'(?:\.(?P<microseconds>\d{1,6}))?'
#     r')?$'
# )


class residenceType(models.Model):
    residence_type = models.CharField(max_length=120, default='')
    def __str__(self):
        return self.residence_type
    class Meta:
        verbose_name = 'Location Type'
        verbose_name_plural = 'Location Types'


class appUserTypes(models.Model):
    app_user_type = models.CharField(max_length=120, default='')
    def __str__(self):
        return self.app_user_type
    class Meta:
        verbose_name = 'App User Type'
        verbose_name_plural = 'App User Type'


class visitorAccessTypes(models.Model):
    access_type = models.CharField(max_length=120, default='')
    main_account = models.CharField(max_length=120, default='')
    can_access_website = models.BooleanField(default=False)
    can_view_dashboard = models.BooleanField(default=False)
    can_view_users = models.BooleanField(default=False)
    can_edit_users = models.BooleanField(default=False)
    can_view_agents = models.BooleanField(default=False)
    can_edit_agents = models.BooleanField(default=False)
    can_view_locations = models.BooleanField(default=False)
    can_edit_locations = models.BooleanField(default=False)
    can_view_connections = models.BooleanField(default=False)
    can_edit_connections = models.BooleanField(default=False)
    can_view_acces_types = models.BooleanField(default=False)
    can_edit_acces_types = models.BooleanField(default=False)
    can_view_visitor_types = models.BooleanField(default=False)
    can_edit_visitor_types = models.BooleanField(default=False)
    can_view_access_passes = models.BooleanField(default=False)
    can_edit_access_passes = models.BooleanField(default=False)
    can_monitor = models.BooleanField(default=False)
    def __str__(self):
        return self.access_type
    class Meta:
        verbose_name = 'Access Type'
        verbose_name_plural = 'Access Type'


class Residence(models.Model):
    name = models.CharField(max_length=140, default='')
    address = models.TextField(max_length=2000, default='')
    contact_person = models.CharField(max_length=140, default='')
    contact_email = models.CharField(max_length=140, default='')
    contact_phone = models.CharField(max_length=140, default='')
    type = models.ForeignKey(residenceType, null=True, related_name='residence_type_from', on_delete=models.CASCADE)
    user = models.CharField(max_length=120, default='')
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.name)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class residenceSyndics(models.Model):
    residence = models.ForeignKey(Residence, null=True, related_name='residence_for_syndics', on_delete=models.CASCADE)
    syndics_name = models.CharField(max_length=140, default='')
    syndics_email = models.CharField(max_length=140, default='')
    syndics_phone = models.CharField(max_length=140, default='')
    def __str__(self):
        return self.syndics_name
    class Meta:
        verbose_name = 'Residence Syndic'
        verbose_name_plural = 'Residence Syndics'


class residenceAreas(models.Model):
    residence = models.ForeignKey(Residence, null=True, related_name='residence_for_areas', on_delete=models.CASCADE)
    area_name = models.CharField(max_length=140, default='')
    floor = models.CharField(max_length=140, default='', null=True, blank=True)
    area_prefix = models.CharField(max_length=140, default='')
    area_allotments_from = models.CharField(max_length=140, default='')
    area_allotments_to = models.CharField(max_length=140, default='')
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    code = models.CharField(max_length=120, default='', blank=True, unique=True)
    code_for_app = models.CharField(max_length=120, default='', blank=True, unique=True)
    company_logo = models.ImageField(upload_to='company_logo', blank=True)
    def __str__(self):
        return self.area_name
    class Meta:
        verbose_name = 'Residence Area'
        verbose_name_plural = 'Residence Areas'
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.code)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.code}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)




class AppUser(models.Model):
    name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=15, default='')
    email = models.CharField(max_length=50, default='')
    passcode = models.CharField(max_length=10, default = random.randint(1000,9999), unique=True, blank=True)
    id_passport_number = models.CharField(max_length=120, default='')
    vehicle_number = models.CharField(max_length=120, default='', null=True, blank=True)
    address = models.TextField(max_length=2000, default='')
    approved = models.BooleanField(default=True)
    is_child = models.BooleanField(default=False)
    parent_user = models.CharField(max_length=120, default='', null=True, blank=True)
    parent_user_url = models.CharField(max_length=120, default='', null=True, blank=True)
    usertype = models.ForeignKey(appUserTypes, null=True, blank=True, related_name='appusertype', on_delete=models.CASCADE)
    accesstype = models.ForeignKey(visitorAccessTypes, null=True, blank=True, related_name='appuseraccesstype', on_delete=models.CASCADE)
    residence = models.ForeignKey(Residence, null=True, blank=True, related_name='user_residence', on_delete=models.CASCADE)
    residence_area = models.ForeignKey(residenceAreas, null=True, blank=True, related_name='user_area', on_delete=models.CASCADE)
    login_date = models.DateTimeField(null=True, blank=True)
    logout_date = models.DateTimeField(null=True, blank=True)
    is_logged = models.BooleanField(default=False)
    browser_id = models.CharField(max_length=40, default='')
    push_id = models.CharField(max_length=40, default='')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'App User'
        verbose_name_plural = 'App Users'



class AppUserAssignedAreas(models.Model):
    user = models.ForeignKey(AppUser, null=True, blank=True, related_name='appuser_assigned', on_delete=models.CASCADE)
    residence_area = models.ForeignKey(residenceAreas, null=True, blank=True, related_name='assigned_user_area', on_delete=models.CASCADE)
    def __str__(self):
        return '***'
    class Meta:
        verbose_name = 'User Assigned Area'
        verbose_name_plural = 'User Assigned Areas'

class visitorType(models.Model):
    visitor_type = models.CharField(max_length=120, default='')
    user = models.CharField(max_length=120, default='')
    isPermanent = models.BooleanField(default=False)
    def __str__(self):
        return self.visitor_type
    class Meta:
        verbose_name = 'Visitor Type'
        verbose_name_plural = 'Visitor Types'

class visitorValidity(models.Model):
    visitor_validity = models.CharField(max_length=120, default='')
    def __str__(self): 
        return self.visitor_validity
    class Meta:
        verbose_name = 'Validity'
        verbose_name_plural = 'Validities'

class Status(models.Model):
    name = models.CharField(max_length=120, default='')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Connection Status'
        verbose_name_plural = 'Connection Statuses'


class Resident(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("ACTIVE", "active"),
        ("DEACTIVE", "deactive")
    )
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="PENDING")
    isActive = models.BooleanField(default=True)
    name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15, default='')
    email = models.EmailField(max_length=50, default='')
    address = models.TextField(max_length=2000, default='')
    push_id = models.CharField(max_length=50, default='', null=True)
    id_passport_number = models.CharField(max_length=120, default='')
    vehicle_number = models.CharField(max_length=120, default='', null=True, blank=True)
    block_zone = models.CharField(max_length=10, default='', null=True, blank=True)
    street_name = models.CharField(max_length=120, default='', null=True, blank=True)
    residence_number = models.CharField(max_length=10, default='', null=True, blank=True)
    number_of_resident = models.IntegerField(null=True)
    passcode = models.CharField(max_length=10, default = random.randint(1000,9999), unique=True, blank=True)
    location = models.CharField(max_length=100, default='', null=True, blank=True)
    recurrance_str = models.CharField(max_length=250, default='', null=True, blank=True)
    registered_on = models.DateTimeField(null=True, blank=True)
    activated_on = models.DateTimeField(null=True, blank=True)
    deactivated_on = models.DateTimeField(null=True, blank=True)
    activated_by = models.ForeignKey(AppUser, null=True, blank=True, related_name='activated_by', on_delete=models.CASCADE)
    deactivated_by = models.ForeignKey(AppUser, null=True, blank=True, related_name='deactivated_by', on_delete=models.CASCADE)
    time_from = models.DateTimeField(null=True, blank=True)
    time_to = models.DateTimeField(null=True, blank=True)
    residence_area = models.ForeignKey(residenceAreas, null=True, blank=True, related_name='residence_area', on_delete=models.CASCADE)
    is_logged = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='residents_qr_codes', blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Resident'
        verbose_name_plural = 'Residents'
    def save(self, *args, **kwargs):
        resident_pass_info = {"Name":self.name, 
                            "Phone": self.phone ,
                            "email": self.email, 
                            "address": self.address,
                            "id_passport_number":self.id_passport_number,
                            "vehicle_number" :self.vehicle_number,
                            "number_of_resident":str(self.number_of_resident),
                            "created_for_self":True,
        }              
        qrcode_img = qrcode.make(json.dumps(resident_pass_info))
        canvas = Image.new('RGB', (700, 700), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.passcode}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)



class Visitor(models.Model):
    name = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15, default='', null=True, blank=True)
    email = models.CharField(max_length=50, default='', null=True, blank=True)
    comment = models.CharField(max_length=100, default='', null=True, blank=True)
    validity_description = models.CharField(max_length=50, default='', null=True, blank=True)
    type = models.ForeignKey(visitorType, null=True, related_name='type', on_delete=models.CASCADE)
    timedatefrom = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles', null=True, blank=True)
    timedateto = models.DateTimeField(null=True, blank=True)
    registered_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    checkin_date = models.DateTimeField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    vehicle_number = models.CharField(max_length=250, default='')
    number_of_guests = models.IntegerField(default=1)
    resident = models.ForeignKey(Resident, null=True, blank=True, related_name='visitor_agent_checkin', on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, null=True, blank=True, related_name='user_agent_checkin', on_delete=models.CASCADE)
    checkout_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='visitor_resident', on_delete=models.CASCADE)
    residence_area = models.ForeignKey(residenceAreas, null=True, related_name='visitor_residence_area', on_delete=models.CASCADE)
    residence = models.ForeignKey(Residence, null=True, related_name='visitor_residence', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, null=True, related_name='visitor_status', on_delete=models.CASCADE)
    code = models.CharField(max_length=120, default='')
    checkin_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='visitor_agent_checkin', on_delete=models.CASCADE)
    checkout_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='visitor_agent_checkout', on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='visitor_qr_codes', blank=True)
    qr_code_share = models.ImageField(upload_to='visitor_qr_codes', blank=True)
    isPermanent   = models.BooleanField(default=False)
    isEnable      = models.BooleanField(default=True)
    recurrance_str = models.CharField(max_length=250, default='', null=True, blank=True)
    recurrance_str_human = models.CharField(max_length=250, default='', null=True, blank=True)
    time_from     = models.CharField(max_length=70, default='', null=True, blank=True)
    time_to       = models.CharField(max_length=70, default='', null=True, blank=True)
    number_of_checkin = models.IntegerField(default=0)
    number_of_ckeckout = models.IntegerField(default=0)
    isQuickPass   = models.BooleanField(default=False)
    isVaccineted   = models.BooleanField(default=False)
    mobile_notifications   = models.TextField(max_length=10000, default='', null=True, blank=True)
    web_notifications      = models.TextField(max_length=10000, default='', null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Connection'
        verbose_name_plural = 'Connections'
        
    def save(self, *args, **kwargs):
        self.code_dict={
            "code":self.code,
            "created_for_self":False
        }
        print(json.dumps(self.code_dict))
        qrcode_img = qrcode.make(json.dumps(self.code_dict))
        canvas = Image.new('RGB', (400,400), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.code}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG') 
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        
        qrcode_img_share = qrcode.make(json.dumps(self.code_dict))
    
        if(str(self.residence_area.residence.type)=="Residence"):
            canvas_share = Image.new('RGB', (400, 810), 'white')
            draw_share = ImageDraw.Draw(canvas_share)
            canvas_share.paste(qrcode_img_share)

            #font = ImageFont.load_default()
            # use a bitmap font
            font = ImageFont.truetype(os.path.join(Path(__file__).resolve().parent, 'arial.ttf'), 14)
    
            spacing = 10
            if self.residence_area.residence:
                text = 'Residence : ' + self.residence_area.residence.name
            if self.residence_area:
                text = 'Residence area: ' + self.residence_area.area_name
            
            if not self.user :
                text += '\nResident name: ' + self.resident.name
                text += '\nResident phone: ' + self.resident.phone
                text += '\nResident email: ' + self.resident.email
            if not self.resident :
                text += '\nResident name: ' + self.user.name
                text += '\nResident phone: ' + self.user.phone
                text += '\nResident email: ' + self.user.email
            
            text += '\nVisitor name: ' + self.name
            text += '\nVisitor email: ' + self.email
            text += '\nVisitor phone: ' + self.phone
            text += '\nVisitor type: ' + self.type.visitor_type
            text += '\nVisitor vehicle /s number: ' + self.vehicle_number
            
            if self.timedatefrom :
                text += '\nDate from: ' + str((self.timedatefrom).replace(tzinfo=tz.gettz('GMT+4')).strftime('%d/%m/%Y'))
            if self.timedateto:
                text += '\nDate to: ' + str((self.timedateto).replace(tzinfo=tz.gettz('GMT+4')).strftime('%d/%m/%Y'))
            if self.time_from and self.time_to and (not self.isPermanent):
                text += '\nTime interval: from ' + getTime(self.time_from) + ' to ' + getTime(self.time_to)
            text += '\nPass Recurrance: ' + splitat(self.recurrance_str_human)

            draw_share.text((30, 420), text, fill ="black", font = font,  
                    spacing = spacing, align ="left")
            img = Image.open( settings.STATIC_ROOT + 'app_logo.jpeg', 'r').resize(( 200 , 30))
            canvas_share.paste(img, (100, 740))
            draw_share.text((140, 780), 'https://accessone.mu', fill ="#b98a5c", font = font,  
            spacing = spacing)
            fname_share = f'qr_code_share-{self.code}'+'.png'
            buffer = BytesIO()
            canvas_share.save(buffer, 'PNG') 
            
            
            self.qr_code_share.save(fname_share, File(buffer), save=False)
            canvas_share.close()

            super().save(*args, **kwargs)
        else:
            canvas_share = Image.new('RGB', (400, 910), 'white')
            draw_share = ImageDraw.Draw(canvas_share)
            img1 = Image.open(settings.MEDIA_ROOT + str(self.residence_area.company_logo), 'r').resize(( 250 , 50))
            canvas_share.paste(img1, (75, 20))
            canvas_share.paste(qrcode_img_share, (0, 70))
            font = ImageFont.truetype(os.path.join(Path(__file__).resolve().parent, 'arial.ttf'), 14)
    
            spacing = 10
            if self.residence_area.residence:
                text = 'Corporate : ' + self.residence_area.residence.name
            if self.residence_area:
                text = 'Company / Office: ' + self.residence_area.area_name
            if not self.user :
                text += '\nCompany Manager: ' + self.resident.name
                text += '\nCompany phone: ' + self.resident.phone
                text += '\nCompany email: ' + self.resident.email
            if not self.resident :
                text += '\nCompany Manager: ' + self.user.name
                text += '\nCompany phone: ' + self.user.phone
                text += '\nCompany email: ' + self.user.email
            
            text += '\nEmployee name: ' + self.name
            text += '\nEmployee email: ' + self.email
            text += '\nEmployee phone: ' + self.phone
            text += '\nVisitor type: ' + self.type.visitor_type
            text += '\nEmployee vehicle /s number: ' + self.vehicle_number
            print(self.timedatefrom)
            if self.timedatefrom and (not self.isPermanent) :
                text += '\nDate from: ' + str((self.timedatefrom).replace(tzinfo=tz.gettz('GMT+4')).strftime('%d/%m/%Y'))
            if self.timedateto and (not self.isPermanent):
                text += '\nDate to: ' + str((self.timedateto).replace(tzinfo=tz.gettz('GMT+4')).strftime('%d/%m/%Y'))
            if self.time_from and  self.time_to and (not self.isPermanent):
                text += '\nTime interval: from ' + getTime(self.time_from) + ' to ' + getTime(self.time_to)
            text += '\nPass Recurrance: ' + splitat(self.recurrance_str_human)

            # text += '\nDate from: ' + str((self.timedatefrom - timedelta(minutes=10)).strftime('%d %Y %H:%m'))
            # text += '\nDate to: ' + str((self.timedateto - timedelta(minutes=10)).strftime('%d %Y %H:%m'))
            
            # drawing text size 
            draw_share.text((30, 490), text, fill ="black", font = font,  
                    spacing = spacing, align ="left")

            img = Image.open( settings.STATIC_ROOT + 'app_logo.jpeg', 'r').resize(( 200 , 30))
            # print("img path:",self.residence_area.company_logo)
            # print("img path:",self.residence_area.company_logo)
            # img1 = Image.open(settings.MEDIA_ROOT + str(self.residence_area.company_logo), 'r').resize(( 250 , 30))

            canvas_share.paste(img, (100, 840))
            draw_share.text((140, 880), 'https://accessone.mu', fill ="#b98a5c", font = font,  
            spacing = spacing)
            # canvas_share.paste(img1, (100, 780))
            fname_share = f'qr_code_share-{self.code}'+'.png'
            buffer = BytesIO()
            canvas_share.save(buffer, 'PNG') 
            
            
            self.qr_code_share.save(fname_share, File(buffer), save=False)
            canvas_share.close()

            super().save(*args, **kwargs)
class Inouts(models.Model):
    inoutpass = models.ForeignKey(Visitor, null=True, related_name='inouts_status', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, null=True, related_name='inouts_status', on_delete=models.CASCADE)
    checkin_date = models.DateTimeField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    checkin_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='inouts_agent_checkin', on_delete=models.CASCADE)
    checkout_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='inouts_agent_checkout', on_delete=models.CASCADE)
    override = models.BooleanField(default=False)
    overrides_note = models.CharField(max_length=250, default='',null=True, blank=True)

    def __str__(self):
        return '-'
    class Meta:
        verbose_name = 'Inout'
        verbose_name_plural = 'Inouts'