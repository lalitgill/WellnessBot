import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from decouple import config
subscription_key = config('AzureOcrKey', cast=str)
endpoint = config('AzureOcrEndpoint', cast=str)
class AzureOcrHelper:
    def azure_ocr(self, file_path):
        computervision_client = ComputerVisionClient(endpoint,
                                                     CognitiveServicesCredentials(subscription_key))

        with open(file_path, "rb") as image_stream:
            read_response = computervision_client.read_in_stream(image_stream, raw=True)

        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        extracted_text = ""
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    extracted_text += line.text + " "

        return extracted_text