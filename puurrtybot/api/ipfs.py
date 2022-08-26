# https://docs.ipfs.tech/how-to/address-ipfs-on-web/

import requests
from requests.models import Response


NETWORK = """https://ipfs.io/ipfs"""
IPFS_STATUS_CODES = {
    #
    400: """Bad Request""",
    502: """Bad Gateway""",
    503: """Service Unavailable""",
    504: """Gateway Timeout"""}


def query(query_string: str) -> Response:
    """Query ipfs.io and check for valid response."""
    response = requests.get(f"""{NETWORK}{query_string}""")
    if response.status_code != 200:
        raise Exception( (response.status_code, IPFS_STATUS_CODES[response.status_code]) )
    return response


def get_image(cid: str) -> Response:
    """Get image from ipfs by cid (ipfs asset id)."""
    return query(f"""/{cid}""")