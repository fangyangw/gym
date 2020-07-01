<template>
  <div class="details-class-wrap">
     <div class="class-info-wrap">
         <i class="title">EZFIT</i>
         <p class="info">{{this.course.NAME}}/{{this.course.PRICE}}元</p>
         <p class="remark">易/在/24H/健/身</p>
         <p class="remark">{{this.course.DISCOUNTS}}</p>
     </div>
     <!-- 课程信息 -->
     <div class="class-details-wrap">
         <div class="info-wrap">
             <p class="title">开课门店</p>
             <p class="info">{{this.course.STORE_NAME}}</p>
         </div>
         <div class="info-wrap">
             <p class="title">课程名称</p>
             <p class="info">{{this.course.NAME}}</p>
         </div>
         <div class="info-wrap">
             <p class="title">课程类型</p>
             <p class="info">{{this.course.TYPE}}</p>
         </div>
         <div class="info-wrap">
             <p class="title">任课老师</p>
             <p class="info">{{this.course.COACH_NAME}}</p>
         </div>
         <div class="info-wrap">
             <p class="title">时长</p>
             <p class="info">{{this.course.DURATION}}</p>
         </div>
         <div class="info-wrap">
             <p class="title">售价</p>
             <p class="info">￥{{this.course.PRICE}}</p>
         </div>
         <div class="class-remark-wrap">
             <p class="title">课程简介:</p>
             <p class="info">{{this.course.SYNOPSIS}}</p>
         </div>
         <div class="class-remark-wrap">
             <p class="title">教练:</p>
             <img :src="this.course.COACH_PHOTO" alt="" style="width:100%; height:100%">
         </div>
     </div>
     <!-- 购买 -->
     <div class="buy-button-wrap">
         <div class="surplus">剩余:{{this.course.REMAIN_QUANTITY}}</div>
         <div class="button" @click="buy_class()">立即购买</div>
     </div>
  </div>
</template>

<script>
import {
    get_course
  } from "@/api/index"
export default {
  name: 'ClassDetail',
  data(){
    return {
      course: {}
    }
  },
  mounted(){
    this.get_course(this.$route.query.class_id)
  },
  methods:{
    buy_class(){
      this.$router.push({
        path: `/ClassOrder/?classid=${this.course.CID}`,
      })
    },
    get_course(course_id){
      get_course({course_id: course_id}).then(res => {
        if(res.code == 200){
          this.course = res.data[0]
          this.course.COACH_PHOTO = 'https://www.ezaifit.top:80/' + this.course.COACH_PHOTO
        }
      })
    }
  }
}
</script>
<style lang="stylus">
.details-class-wrap{
    height 100%;
    background-color white;
    .class-info-wrap{
        width 100%;
        height 181px;
        background-image url('../assets/classdetails.png');
        background-repeat no-repeat;
        background-size 100% 100%;
        box-sizing border-box;
        font-size 18px;
        color white;
        padding-left 25px;
        padding-top 25px;
        .title{
            color red;
            font-weight bold;
            letter-spacing 2px;
        }
        .info{
            color red;
            font-weight bold;
            letter-spacing 2px;
            padding-top 35px;
            padding-bottom 15px;
        }
        .remark{
            font-size 9px;
            padding-top 10px;

        }
    }
    .class-details-wrap{
        background-color white;
        width 100%;
        height 100%;
        border-top-right-radius 30px;
        border-top-left-radius 30px;
        margin-top -15px;
        position relative;
        box-sizing border-box;
        padding 35px 30px;
        .info-wrap{
            display flex;
            justify-content space-between;
            width 100%;
            font-size 15px;
            color #8d9194;
            letter-spacing 2px;
            padding-bottom 20px;
        }
        .class-remark-wrap{
            padding-top 40px;
            font-size 15px;
            .title{
                color #8d9194;
            }
            .info{
                padding-top 20px;
            }
        }
    }
    .buy-button-wrap{
        width 100%;
        height 50px;
        // border-radius 8px;
        border-top 2px solid $index_background_color;
        background-color #fefefe;
        color white;
        font-size 15px;
        display flex;
        justify-content space-between;
        align-items center;
        position fixed;
        bottom 0;
        left 0;
        z-index 1000;
        letter-spacing 2px;
        padding-left 15px;
        box-sizing border-box;
        .surplus{
            color black;
            font-size 15px;
            letter-spacing 2px;
        }
        .button{
            background-color #3478d2;
            border-radius 12px;
            height 100%;
            width 40%;
            display flex;
            justify-content center;
            align-items center;
            font-size 12.5px;
            // color
        }
    }
}
</style>
