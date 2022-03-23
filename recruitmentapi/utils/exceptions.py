from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.data.get('detail'):
            response.data['status_code'] = response.status_code
            response.data['message'] = response.data['detail']
            response.data.pop('detail')
        else:
            if response.data.get('non_field_errors') or response.data.get('message'):
                response.data['status_code'] = response.status_code
            else:
                field_errors = {}
                for key in response.data:
                    field_errors[key] = response.data[key]
                response.data = {'status_code': response.status_code,
                                 'field_errors': field_errors}
        return response
