from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer, SensorsSerializer


class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorsSerializer

    def post(self, request):
        Sensor(**request.data).save()
        return Response({'status': 'OK'})


class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def patch(self, request, pk):
        Sensor.objects.filter(id=pk).update(**request.data)
        return Response({'status': 'OK'})


class MeasurementsView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request):
        data = request.data
        if 'sensor_id' not in data and 'sensor' in data:
            data['sensor_id'] = data['sensor']
            del data['sensor']
        Measurement(**data).save()
        return Response({'status': 'OK'})
