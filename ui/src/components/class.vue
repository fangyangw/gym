<template>
  <div v-if="is_buy" class="class-wrap" @click="goDetails()">
    <div class="img-wrap" v-bind:style="{backgroundImage:'url(' + getPicture() + ')'}">
      <div>
        <!-- <van-tag class="tga-wrap-left" mark type="primary" size="large">{{this.course_detail.TYPE}}</van-tag> -->
      </div>
      <div>
        <!-- <van-tag class="tga-wrap-right" type="success" size="large">{{this.course_detail.NAME}}</van-tag> -->
      </div>
    </div>
    <!-- <p class="price">{{this.course_detail.NAME}}</p> -->
    <div class="title-warp">
      <span class="title">{{this.course_detail.DURATION}}/课时</span>
      <!-- <span class="title" style="margin-top:5px;">{{this.course_detail.SYNOPSIS}}</span> -->
    </div>
  </div>
  <div v-else class="class-wrap">
    <div class="img-wrap" v-bind:style="{backgroundImage:'url(' + getPicture() + ')'}">
      <div>
        <!-- <van-tag class="tga-wrap-left" mark type="primary" size="large">{{this.course_detail.TYPE}}</van-tag> -->
      </div>
      <div>
        <!-- <van-tag class="tga-wrap-right" type="success" size="large">{{this.course_detail.NAME}}</van-tag> -->
      </div>
    </div>
    <!-- <p class="price">{{this.course_detail.NAME}}</p> -->
    <div class="title-warp">
      <span class="title">{{this.course_detail.DURATION}}/课时</span>
      <!-- <span class="title" style="margin-top:5px;">{{this.course_detail.SYNOPSIS}}</span> -->
    </div>
  </div>
</template>

<script>
  import { Tag } from 'vant';
  export default {
    name: "class",
    methods: {
      goDetails() {
        this.$router.push({
          path: `/DetailsClass/?class_id=${this.course_detail.CID}`
        })
      },
      getPicture(){
        return 'https://www.ezaifit.top:80/' + this.course_detail.BACKGROUND
      }
    },
    props: {
      course_detail: {
        type: Object,
        default: function() {
          return {CID: 1};
        }
      },
      is_buy: Boolean,
    }
  }

</script>

<style lang="stylus">
  .class-wrap
    width 100%;
    margin-left 10px;
    margin-right 10px;
    margin-bottom 10px;
    .img-wrap
      width 100%;
      height 155px;
      // border-radius 12px;

      background-repeat no-repeat;
      background-size 100% 100%;
      box-sizing border-box;
      display flex
      justify-content space-between
      .tga-wrap-right
        font-size 16px
      .tga-wrap-left
        font-size 16px
    .title-warp
      background-color #ffffff
      .title
        display block
        font-size 14px
        padding 5px 0px
</style>
