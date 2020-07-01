import requests
import json
import logging
import base64
import datetime

host = "http://322v8358j2.qicp.vip"
register_user_url = "/Face/SetUserInfo"
delete_user_url = "/Face/DeleteUser"
set_face_url = "/Face/SetUserFacePhoto"
delete_face_url = "/Face/DeleteUserFacePhoto"
set_verify_url = "/Face/SetUserVerifyPhoto"
delete_verify_url = "/Face/DeleteUserVerifyPhoto"
get_all_user_url = "/Face/GetAllUserInfo"
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DoorControl")


def get_all_user():
    url = host + get_all_user_url
    payload = {}
    response = call_api("GET", url, json.dumps(payload), "call get all user")
    if response and response.get("status") == 200:
        return True, response.get("data")
    else:
        return False, response.get("data")


def delete_verify_face(user_id):
    url = host + delete_verify_url + "/" + str(user_id)
    payload = {}
    response = call_api("GET", url, json.dumps(payload), "call delete verify face")
    if response and response.get("status") == 200:
        return True, ""
    else:
        return False, response.get("data")


def set_verify_face(user_id, photo):
    url = host + set_verify_url
    payload = {
        "userID": user_id,
        "photo": photo
    }
    response = call_api("POST", url, json.dumps(payload), "call set verify face")
    if response and response.get("SetUserVerifyPhotoResult", {}).get("status") == 200:
        return True, ""
    else:
        return False, response.get("data")


def delete_face(user_id):
    url = host + delete_face_url + "/" + str(user_id)
    payload = {}
    response = call_api("GET", url, json.dumps(payload), "call delete face")
    if response and response.get("status") == 200:
        return True, ""
    else:
        return False, response.get("data")


def set_face(user_id, photo):
    url = host + set_face_url
    payload = {
        "userID": user_id,
        "photo": photo
    }
    response = call_api("POST", url, json.dumps(payload), "call set face")
    if response and response.get("SetUserFacePhotoResult", {}).get("status") == 200:
        return True, ""
    else:
        return False, response.get("data")


def register_user(user_id, username, password, privilege=0):
    url = "%s%s" % (host, register_user_url)
    payload = {
        "userID": user_id
    }
    if username:
        payload["name"] = username
    if password is not None:
        payload["password"] = password
    if privilege is not None:
        payload["privilege"] = privilege
    response = call_api("POST", url, json.dumps(payload), "call register user")
    if response and response.get("status") == 200:
        return True, ""
    else:
        return False, response.get("data")


def delete_user(user_id):
    url = host + delete_user_url + "/" + str(user_id)
    payload = {}
    response = call_api("GET", url, json.dumps(payload), "call delete user")
    if response and response.get("status") == 200:
        return True, ""
    else:
        return False, response.get("data")


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
        logger.info("API url: %s, userid: %s" %(url, json.loads(payload).get("userID")))

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


def check_and_register(member):
    user_id = str(member.MID)
    status, data = register_user(user_id, member.NICK, member.PASSWORD)
    final_status = False
    if not status:
        print("Warning: cann't register user.")
    if member.PHOTO:
        r = requests.request("GET", member.PHOTO)
        if r.status_code == 200:
            with open("tmp.jpg", 'wb') as fh:
                fh.write(r.content)
            with open("tmp.jpg", 'rb') as fh:
                image = fh.read()
                image_base64 = str(base64.b64encode(image), encoding='utf-8')
                status, data = set_face(user_id, "data:image/jpg;base64,%s" % image_base64)
    if member.PICTURE:
        with member.PICTURE.open("rb") as fh:
            image = fh.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')
            status, data = set_verify_face(user_id, "data:image/jpg;base64,%s" % image_base64)
            if status is True:
                member.register_door_control_status = True
                member.save()
            else:
                print("Error: set verify face %s" % data)
            final_status = status
    else:
        print("Error: there is no user verify picture")
    return final_status, ""


def check_member_in_vip_date(remain_time, now=None):
    pass
    # if now is None:
    #     now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    # if remain_time and remain_time != 0 and remain_time != '0':
    #     try:
    #         remain_datetime = datetime.datetime.strptime(remain_time, "%Y-%m-%d %H:%M:%S")
    #         if now < remain_datetime:
    #             return True
    #     except Exception as e:
    #         print("check in vip date error, %s" % str(e))
    # return False
