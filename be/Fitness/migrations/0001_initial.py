# Generated by Django 2.1.4 on 2020-05-09 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('CID', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='卡ID')),
                ('NAME', models.CharField(blank=True, max_length=100, null=True, verbose_name='卡名称')),
                ('TYPE', models.CharField(blank=True, max_length=100, null=True, verbose_name='卡类型')),
                ('REMARK', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('INDATE', models.CharField(blank=True, max_length=255, null=True, verbose_name='有效期')),
                ('PRICE', models.CharField(blank=True, max_length=100, null=True, verbose_name='售价')),
                ('DAYS', models.CharField(blank=True, max_length=100, null=True, verbose_name='天数')),
                ('REMAIN_QUANTITY', models.CharField(blank=True, max_length=100, null=True, verbose_name='剩余数量')),
            ],
            options={
                'verbose_name': '03_card_table',
                'verbose_name_plural': '03_card_table',
                'db_table': '03_card_table',
            },
        ),
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('CID', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='门店ID')),
                ('NAME', models.CharField(blank=True, max_length=100, null=True, verbose_name='姓名')),
            ],
            options={
                'verbose_name': '05_coach_table',
                'verbose_name_plural': '05_coach_table',
                'db_table': '05_coach_table',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('CID', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='课程ID')),
                ('NAME', models.CharField(blank=True, max_length=100, null=True, verbose_name='课程名称')),
                ('TYPE', models.CharField(blank=True, max_length=100, null=True, verbose_name='课程类型')),
                ('DISCOUNTS', models.CharField(blank=True, max_length=100, null=True, verbose_name='优惠信息')),
                ('DURATION', models.CharField(blank=True, max_length=100, null=True, verbose_name='持续时长')),
                ('PRICE', models.CharField(blank=True, max_length=100, null=True, verbose_name='售价')),
                ('SYNOPSIS', models.CharField(blank=True, max_length=100, null=True, verbose_name='简介')),
                ('REMAIN_QUANTITY', models.CharField(blank=True, max_length=100, null=True, verbose_name='剩余数量')),
                ('BACKGROUND', models.ImageField(blank=True, null=True, upload_to='background/', verbose_name='背景图')),
                ('COACH_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Fitness.Coach', verbose_name='教练ID')),
            ],
            options={
                'verbose_name': '02_course_table',
                'verbose_name_plural': '02_course_table',
                'db_table': '02_course_table',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('MID', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='会员ID')),
                ('PASSWORD', models.CharField(blank=True, max_length=255, null=True, verbose_name='支付密码')),
                ('NICK', models.CharField(blank=True, max_length=100, null=True, verbose_name='昵称')),
                ('PHOTO', models.ImageField(blank=True, null=True, upload_to='phone/', verbose_name='头像')),
                ('PHONE', models.CharField(blank=True, max_length=100, null=True, verbose_name='手机号')),
                ('PICTURE', models.ImageField(blank=True, null=True, upload_to='picture/', verbose_name='人脸照片')),
                ('YIBI', models.CharField(blank=True, max_length=100, null=True, verbose_name='我的易币')),
                ('SHARE', models.CharField(blank=True, max_length=100, null=True, verbose_name='我的分享')),
                ('REGISTER_DATE', models.DateField(auto_now_add=True, verbose_name='注册时间')),
                ('REMAIN_TIME', models.CharField(blank=True, max_length=100, null=True, verbose_name='会员剩余时间')),
                ('CARD_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Fitness.Card', verbose_name='卡ID')),
                ('COURSE_ID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Fitness.Course', verbose_name='课程ID')),
            ],
            options={
                'verbose_name': '01_member_table',
                'verbose_name_plural': '01_member_table',
                'db_table': '01_member_table',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('SID', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='门店ID')),
                ('NAME', models.CharField(blank=True, max_length=100, null=True, verbose_name='门店名称')),
                ('ADDRESS', models.CharField(blank=True, max_length=100, null=True, verbose_name='门店地址')),
            ],
            options={
                'verbose_name': '04_store_table',
                'verbose_name_plural': '04_store_table',
                'db_table': '04_store_table',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='STORE_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Fitness.Store', verbose_name='门店ID'),
        ),
        migrations.AddField(
            model_name='coach',
            name='STORE_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Fitness.Store', verbose_name='门店ID'),
        ),
        migrations.AddField(
            model_name='card',
            name='STORE_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Fitness.Store', verbose_name='门店ID'),
        ),
    ]
