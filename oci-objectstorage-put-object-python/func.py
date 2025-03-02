# Copyright (c) 2019, Oracle and/or its affiliates.  All rights reserved.
import io
import os
import json
import sys
from fdk import response

import oci.object_storage

def handler(ctx, data: io.BytesIO=None):
    signer = oci.auth.signers.get_resource_principals_signer()
    try:
        body = json.loads(data.getvalue())
        bucketName = body["bucketName"]
        fileName = body["objectName"]
        content = body["content"]
    except Exception as e:
        error = """
                Input a JSON object in the format: '{"bucketName": "<bucket name>",
                "content": "<content>", "objectName": "<object name>"}'
                """
        raise Exception(error)
    resp = put_object(signer, bucketName, objectName, content)
    return response.Response(
        ctx,
        response_data=json.dumps(resp),
        headers={"Content-Type": "application/json"}
    )

def put_object(signer, bucketName, objectName, content):
    client = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    try:
        object = client.put_object(os.environ.get("OCI_NAMESPACE"), bucketName, objectName, json.dumps(content))
        output = "Success: Put object '" + objectName + "' in bucket '" + bucketName + "'"
    except Exception as e:
        output = "Failed: " + str(e.message)
    response = { "state": output }
    return response
