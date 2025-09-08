from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api import utils as api_utils


class AddTask(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        View to add tasks
        """
        params = request.data
        return api_utils.add_task(params, request)


class ShowTaskList(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        View to show all tasks
        """
        params = request.data
        return api_utils.show_tasks(params, request)


class RemoveTask(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        View to remove task
        """
        params = request.data
        return api_utils.remove_task(params, request)
