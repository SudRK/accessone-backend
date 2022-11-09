from .models import *
from .serializers import *
from django.dispatch import receiver
from channels.layers import get_channel_layer 
from django.db.models.signals import post_save,pre_save, post_delete
from asgiref.sync import async_to_sync
import json

@receiver(post_save,sender=AppUser)
def at_staff_save(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    serialiseddata = AppUserSerializer(instance)
    data ={'action': 'create' if created else 'update',
        'data' : serialiseddata.data,
        'type': 'appuser'}
    async_to_sync(channel_layer.group_send)(
        'AccessOne_Group' ,{
            'type': 'status',  #it's a event handler
            'value': json.dumps(data)
        }
    )
    
@receiver(post_delete,sender=AppUser)
def at_staff_save(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    serialiseddata = AppUserSerializer(instance)
    data ={'action': 'delete',
        'type': 'appuser'}

    async_to_sync(channel_layer.group_send)(
        'AccessOne_Group' ,{
            'type': 'status',  #it's a event handler
            'value': json.dumps(data)
        }
    )

    
    

# @receiver(post_delete,sender=Company_staff)
# def at_staff_delete(sender, instance, created, **kwargs):
#     staff(sender, instance, created, **kwargs)
    
# def staff(sender, instance, created, **kwargs):
#     channel_layer = get_channel_layer()
#     data={}
#     staffs=Company_staff.objects.filter(company__id=instance.company.id,is_active=True).values("user_id")
#     data["staffs"]=len(staffs)
#     async_to_sync(channel_layer.group_send)(
#         'dashboard_%s' % instance.company.id,{
#             'type': 'status_message',  #it's a event handler
#             'value': json.dumps(data)
#         }
#     )
#     user=User.objects.filter(id__in=staffs).all()
#     user_serializer=UserSerializer(user,many=True)
#     async_to_sync(channel_layer.group_send)(
#         'staff_%s' % instance.company.id,{
#             'type': 'status_message',
#             'value': json.dumps(user_serializer.data)
#         }
#     )