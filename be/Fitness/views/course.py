# 课程信息
from rest_framework.views import APIView
from rest_framework.response import Response
from Fitness import models
from Fitness.utils import serializer


class CourseList(APIView):
    """
    课程列表
    """

    def get(self, request):
        res = {
            'code': 200,
            'data': [],
            'msg': 'Success'
        }
        course_set = models.Course.objects.all()
        course_ser = serializer.CourseSerializer(course_set, many=True)
        res['data'] = course_ser.data
        return Response(res)


class CourseDetail(APIView):
    """
    课程详情
    """

    def get(self, request):
        cid = request.GET.get("course_id")
        course_set = models.Course.objects.all()
        if cid:
            course_set = models.Course.objects.filter(CID=int(cid))
        res = {
            'code': 200,
            'data': [],
            'msg': 'Success'
        }
        course_detail_ser = serializer.CourseSerializer(course_set, many=True)
        res['data'] = course_detail_ser.data
        return Response(res)

    def post(self, request):
        res = {
            'code': 200,
            'data': [],
            'msg': 'Success'
        }
        cid = request.data.get('CID')
        if cid:
            course_detail_set = models.Course.objects.filter(CID=cid)
            course_detail_ser = serializer.CourseSerializer(course_detail_set, many=True)
            res['data'] = course_detail_ser.data
            return Response(res)
