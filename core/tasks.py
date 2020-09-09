import json
import os

import boto3
import requests
from background_task import background
from boto3.session import Session
from django.conf import settings

from Algo.document_parser import main
from .models import OutputFiles, HandwritingInputLogger
from .serializers import OutputFilesSerializer
s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY , aws_secret_access_key=settings.AWS_SECRET)


# start after 1 sec
@background(schedule=1)
def output_file_proccessor(id, file_name, player_id):
    output_file_name = os.path.join(settings.MEDIA_ROOT, id + ".pdf")
    pic_loc = settings.PICKLE_LOC
    url = 'https://dsc-handly.s3.ap-south-1.amazonaws.com/TEST.docx'
    input_loc = os.path.join(settings.MEDIA_ROOT, id+'.docx')
    s3.download_file('dsc-handly', id+'.docx' , input_loc)
    print(input_loc, pic_loc, output_file_name)
    status, resp = main(input_loc, output_file_name, pic_loc)
    print(resp)
    handwriter = HandwritingInputLogger.objects.filter(id=id)[0]
    handwriter.status = True
    if status:
        data = {
            'input_details': handwriter,
            'url': '/media/' + resp.split('/media/')[1]
        }
        output = OutputFiles(**data)
        output.save()
        handwriter.save()
        output = OutputFiles.objects.filter(input_details__id=id)
        serializer = OutputFilesSerializer(output, many=True)
        if player_id != '':
            send_push(player_id, '/media/' + resp.split('/media/')[1], True)
            print("done")
    else:
        handwriter.error_status = True
        handwriter.error_logger = resp
        handwriter.save()
        if player_id != '':
            send_push(player_id, '/media/' + resp.split('/media/')[1], False)
        # send push
    print(status, '/media/' + resp.split('/media/')[1])


def send_push(player_id, output, status):
    if status:
        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": settings.ONE_SIGNAL_AUTH_KEY
        }
        payload = {"app_id": settings.ONE_SIGNAL_ID,
                   "include_player_ids": [player_id],
                   "contents": {"en": "Handwritten Document Ready!"},
                   "data": {"status": "Success", "payload": output}
                   }
        print(payload)
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        print(req.status_code, req.reason)
    else:
        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": settings.ONE_SIGNAL_AUTH_KEY
        }
        payload = {"app_id": settings.ONE_SIGNAL_ID,
                   "include_player_ids": [player_id],
                   "contents": {"en": "Handwritten Document Failed!"},
                   "data": {"status": "Failed", "payload": output}
                   }
        print(payload)
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        print(req.status_code, req.reason)
