from rest_framework.schemas.openapi import AutoSchema


class IssueListUpdateSchema(AutoSchema):
    """
    Customization of schema
    """
    def get_operation(self, path, method):
        operation = super(IssueListUpdateSchema, self).get_operation(path, method)
        request_body = {
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                            'minimum': 1,
                            'nullable': False
                        },
                        'ordering': {
                            'type': 'integer',
                            'minimum': 1,
                            'maximum': 32767,
                            'nullable': True,
                        }
                    },
                    'required': [
                        'id'
                    ]
                },
            }
        }

        operation.update({
            'operationId': 'UpdateIssueOrdering',
        })

        operation['requestBody']['content']['application/json'] = request_body
        operation['requestBody']['content']['application/x-www-form-urlencoded'] = request_body
        operation['requestBody']['content']['multipart/form-data'] = request_body

        return operation
