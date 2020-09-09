from background_task import background
from Algo.document_parser import main
import urllib.request
import os
from django.conf import settings
from .models import OutputFiles, HandwritingInputLogger
import requests
import json
from .serializers import OutputFilesSerializer


# start after 1 sec
@background(schedule=1)
def output_file_proccessor(id, file_name, player_id):
    output_file_name = os.path.join(settings.MEDIA_ROOT, id + ".pdf")
    pic_loc = settings.PICKLE_LOC
    input_loc = os.path.join(settings.MEDIA_ROOT, file_name.split('/media/')[1])
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
