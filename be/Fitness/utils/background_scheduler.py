import logging
import socket

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from Fit.settings import VIP_STATUS_COUNT_INTERVAL, ENABLE_SCHEDULER, NOTICE_DAY
from Fitness.models import Member
from Fitness.utils.door_control import delete_verify_face, check_member_in_vip_date, delete_user, check_and_register
from Fitness.views.wx_get import update_token
from Fitness.views.tools import get_user_remain_time, send_notification
import datetime
logger = logging.getLogger("django")


def check_user_vip_date():
    update_token()
    # flag = False
    # # 每2个小时进行check,再每天0-2点时进行会员卡进行计时
    # if (utc_now.hour + 8) > 0 and utc_now.hour + 8 < VIP_STATUS_COUNT_INTERVAL/(60*60):
    #     flag = True
    for member in Member.objects.all():
        try:
            remain_day, card = get_user_remain_time(member)
            try:
                if remain_day < 1:
                    if member.register_door_control_status is True:
                        print("%s , %s is out of vip date, but still have door control, remove it photo from door control." %(member.NICK, member.MID))
                        status, message = delete_user(member.MID)
                        if status is True:
                            member.register_door_control_status = False
                            member.save()
                        else:
                            print("Error: cat not remove it photo from door control")
                else:
                    if member.register_door_control_status is False:
                        print("%s , %s is in vip date, add it photo to door control." %(member.NICK, member.MID))
                        status, message = check_and_register(member)
                        if status is True:
                            member.register_door_control_status = True
                            member.save()
                        else:
                            print("Error: cat not add it photo from door control")
            except Exception as e:
                print("Error: check member vip date. %s" % str(e))
            if remain_day < NOTICE_DAY and member.notice_status is False:
                send_notification(member, card)
            if remain_day >= NOTICE_DAY and member.notice_status is True:
                member.notice_status = False
                member.save()

        except Exception as e:
            print("Error: notice member vip date. %s" % str(e))
        # else:
        #     if flag:
        #         member.REMAIN_TIME = str(int(member.REMAIN_TIME) - 1)
        #         member.save()


def init_scheduler():
    if ENABLE_SCHEDULER:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 47200))

            scheduler = BackgroundScheduler()
            scheduler.add_jobstore(DjangoJobStore(), "default")

            scheduler.add_job(check_user_vip_date, "interval",
                              id='apps.utils.background_scheduler.heartbeat',
                              seconds=VIP_STATUS_COUNT_INTERVAL)
            register_events(scheduler)
            scheduler.start()
        except socket.error:
            logger.info('!!!scheduler already started, DO NOTHING!!!')
