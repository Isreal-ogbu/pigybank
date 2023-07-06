from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from django.db import transaction


def error_handler(e):
    msg = ''
    if hasattr(e, 'detail'):
        if isinstance(e.detail, dict):
            for q in e.detail.items():
                msg += f"{q[0]}: {q[1][0]} "
                break
        elif isinstance(e.detail, list):
            for q in e.detail:
                msg += f"{q} "
                break
        else:
            msg = str(e.detail)
    elif hasattr(e, 'message'):
        if isinstance(e.message, dict):
            for q in e.message.items():
                msg += f"{q[0]}: {q[1][0]} "
                break
        elif isinstance(e.message, list):
            for q in e.message:
                msg += f"{q} "
                break
        elif isinstance(e.message, str):
            msg = e.message
        else:
            msg = str(e)
    else:
        msg = str(e)
    return msg


class ResponseInfo(object):
    def __init__(self, **args):
        self.response = {
            "status": args.get('status', 'success'),
            "data": args.get('data', []),
            "message": args.get('message', 'Success')
        }
        self.status_code = status.HTTP_200_OK


class ResponseModelViewSet(ModelViewSet):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        self.status_code = ResponseInfo().status_code
        super().__init__(**kwargs)

    def get_queryset(self):
        q = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return q
            else:
                return q
        else:
            return q

    def list(self, request, *args, **kwargs):
        print("ok")
        try:
            response_data = super().list(request, *args, **kwargs)
            self.response_format["data"] = response_data.data
            self.status_code = response_data.status_code
            if not response_data.data:
                self.response_format["message"] = "List empty"

        except Exception as e:
            self.response_format['status'] = 'Failed'
            self.response_format['message'] = error_handler(e)
            self.status_code = status.HTTP_400_BAD_REQUEST
        return Response(self.response_format, status=self.status_code)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            response_data = super().create(request, *args, **kwargs)
            self.response_format["data"] = response_data.data
            self.status_code = response_data.status_code
        except Exception as e:
            self.response_format["status"] = 'Failed'
            self.response_format['message'] = error_handler(e)
            self.status_code = status.HTTP_400_BAD_REQUEST
        return Response(self.response_format, status=self.status_code)

    def retrieve(self, request, *args, **kwargs):
        try:
            response_data = super().retrieve(request, *args, **kwargs)
            self.response_format["data"] = response_data.data
            self.status_code = response_data.status_code
            if not response_data.data:
                self.response_format["message"] = "Empty"
        except Exception as e:
            self.response_format['status'] = 'Failed'
            self.response_format['message'] = error_handler(e)
            self.status_code = status.HTTP_400_BAD_REQUEST
        return Response(self.response_format, status=self.status_code)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            kwargs['partial'] = True
            response_data = super().update(request, *args, **kwargs)
            self.response_format["data"] = response_data.data
            self.status_code = response_data.status_code
        except Exception as e:
            self.response_format['status'] = 'Failed'
            self.response_format['message'] = error_handler(e)
            self.status_code = status.HTTP_400_BAD_REQUEST
        return Response(self.response_format, status=self.status_code)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        try:
            obj = vars(self.get_object())
            obj.pop('_state', None)
            obj.pop('password', None)
            obj.pop('is_staff', None)
            obj.pop('is_superuser', None)
            obj.pop('secret', None)
            response_data = super().destroy(request, *args, **kwargs)
            self.response_format["data"] = obj
            self.status_code = response_data.status_code
        except Exception as e:
            msg = error_handler(e)
            if "protected" in str(e):
                msg = "This record cannot be deleted, because it has been referenced"
            self.response_format['message'] = msg
            self.response_format['status'] = 'Failed'
            self.status_code = status.HTTP_400_BAD_REQUEST
        return Response(self.response_format, status=self.status_code)


class ResponseAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        self.status_code = ResponseInfo().status_code
        super().__init__(**kwargs)