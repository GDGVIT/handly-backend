from django.contrib import admin
from .models import (
    Collections,
    OutputFiles,
    HandwritingInputLogger,
    InputFile
)
# Register your models here.
admin.site.register(Collections)
admin.site.register(OutputFiles)
admin.site.register(HandwritingInputLogger)
admin.site.register(InputFile)