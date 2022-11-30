from enum import Enum
from os import stat

class SIZE_UNIT(Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_unit(size_in_bytes, unit):
    """Convert the size from bytes to other units like KB, MB or GB"""
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


def get_file_size(file_path, size_type=SIZE_UNIT.BYTES):
    """Get file in size in given unit like KB, MB or GB"""
    size = stat(file_path).st_size
    sizes = []
    sizes.append({"size": convert_unit(size, SIZE_UNIT.BYTES), "unit": "Bytes"})
    sizes.append({"size": convert_unit(size, SIZE_UNIT.KB), "unit": "KB"})
    sizes.append({"size": convert_unit(size, SIZE_UNIT.MB), "unit": "MB"})
    sizes.append({"size": convert_unit(size, SIZE_UNIT.GB), "unit": "GB"})
    size, unit = list(filter(lambda a: int(a["size"]) > 0, sizes))[-1].values()
    return size, unit


# Enum for each endpoint
class endpoints(Enum):
    base_url = "https://ai4mat.enea.it"
    get_token = f"{base_url}/auth/jwt/login"
    check_auth = f"{base_url}v1/health/checkauth"
    post_metadata = f"{base_url}/api/v1/project/add"
    post_project_file = f"{base_url}/api/v1/project/add/file/"
    post_property_file = f"{base_url}/api/v1/project/add/file_property/"
    get_query_db = f"{base_url}/api/v1/project/query/"
    get_user_projects_info = f"{base_url}/api/v1/user/projects/info"
    get_file = f"{base_url}/file"
    delete_project_file = f"{base_url}/api/v1/project/add/file/"
