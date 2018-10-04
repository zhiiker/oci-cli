# coding: utf-8
# Copyright (c) 2016, 2018, Oracle and/or its affiliates. All rights reserved.

import oci
from oci_cli.cli_clients import CLIENT_MAP
from oci_cli.cli_clients import MODULE_TO_TYPE_MAPPINGS
from oci.file_storage import FileStorageClient

MODULE_TO_TYPE_MAPPINGS["file_storage"] = oci.file_storage.models.file_storage_type_mapping
CLIENT_MAP["file_storage"] = FileStorageClient