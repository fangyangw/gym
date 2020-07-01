import string
import random
import hashlib
import json
import requests
import logging

logger = logging.getLogger("CommonTools")


def nonce_str(size=32):
    charsets = string.ascii_uppercase + string.digits
    result = []
    for index in range(0, size):
        result.append(random.choice(charsets))
    return "".join(result)


def sign(payload, sign_key=None):
    lst = []
    for key, value in payload.items():
        lst.append("%s=%s" % (key, value))
    lst.sort()
    raw_str = "&".join(lst)
    if sign_key:
        raw_str += "&key=%s" % sign_key
    md5 = hashlib.md5()
    md5.update(raw_str.encode('utf8'))
    return md5.hexdigest().upper()


def sign_sha1(payload):
    lst = []
    for key, value in payload.items():
        lst.append("%s=%s" % (key, value))
    lst.sort()
    raw_str = "&".join(lst)
    return hashlib.sha1(raw_str.encode("utf-8")).hexdigest()


def call_api(method, url, payload={}, info=''):
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        if type(payload) is dict:
            payload = json.dumps(payload)
        payload = payload.encode("utf-8")
        logger.info("API url: %s" % url)

        response = requests.request(method, url, data=payload, headers=headers, timeout=(4, 6))
        logger.info("Response status_code: %s ,  text: %s" %(response.status_code, response.text))
        if response.status_code >= 300:
            logger.error("Url: " + url + "\n" + payload)
            msg = ('Call the ZLIMS (' + info
                        + ') API Failed.  status code '
                        + str(response.status_code)
                        + "\n" + response.text)
            logger.error(msg)
            return {}
        else:
            response.encoding = 'utf-8'
            return json.loads(response.text)
    except Exception as e:
        logger.error("Url: " + url + "\n" + str(payload))
        msg = 'Call (' + info + ') API Failed.' + str(e)
        logger.error(msg)
        return {}
