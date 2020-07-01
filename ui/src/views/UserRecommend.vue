<template>
  <div class="user-recommend-wrap">
    <div class="user-info-wrap">
      <div class="qr-wrap">
        <div id="qrcode" class="qr-code"></div>
      </div>
      <div class="title-wrap">
        <span style="font-size: 18px;">用户通过扫描您的分享码, 完成新用户注册3个步骤后, 即可获得10易币<br/></span>
      </div>
    </div>
    <div class="user-info-wrap">
       <p>邀请我的人：</p>
        <div class="user-logo" v-if="recommend_member">
         <div><img :src="recommend_member.PHOTO" class="head-image"  v-if="recommend_member.PHOTO"/></div>
         <div class="head-name">{{recommend_member.NICK}}</div>
        </div>
       <p>我邀请的人：</p>
        <div class="user-logo" v-for="(user, i) in shared_members">
         <div><img :src="user.PHOTO" class="head-image"/></div>
         <div class="head-name">{{user.NICK}}</div>
        </div>
    </div>
    <div class="tip-warp">
      <span>推荐人购卡或购买私教课，可获得金额10%的等额易币</span>
    </div>
  </div>
</template>

<script>
import { get_user_info_details } from "@/api/index";
import QRCode from 'qrcodejs2';
export default {
  data(){
    return{
      link: 'https:///www.ezaifit.top/CheckUserRecommend',
      userinfo:{},
      total_class: 0,
      total_card: 0,
      recommend_member: {},
      shared_members: []
    }
  },
  components:{
    // "van-popup":Popup
  },
  mounted(){
    if(this.openid){
      this.get_user_info_details()
      console.log("-=-=")
      this.$nextTick (function () {
        this.qrcode();
      })
    }
  },
  computed:{
    username(){
        return window.localStorage.getItem('username')
      },
      userimage(){
        return window.localStorage.getItem('userimage')
      },
      openid(){
        return window.localStorage.getItem('openid')
      },
  },
  methods:{
    qrcode () {
        let that = this;
        let qrcode = new QRCode('qrcode', {
            width: 135,
            height: 135,        // 高度
            text:  this.link + '?recommend_id=' + this.openid,   // 二维码内容
            background : "#ffffff", //二维码的后景色
            foreground : "#000000", //二维码的前景色
            // render: 'canvas' ,   // 设置渲染方式（有两种方式 table和canvas，默认是canvas）
            // background: '#f0f',   // 背景色
            // foreground: '#ff0'    // 前景色
        })
    },
    get_user_info_details(){
      get_user_info_details({
        "OPENID":this.openid
      }).then(res => {
        console.log(res)
        if(res.code == 200){
          this.userinfo = res.data[0]
          this.total_card = res.total_card
          this.total_class = res.total_class
          this.recommend_member = res.recommend_member
          this.shared_members = res.shared_members
        }
      })
    }
  }
}
</script>
<style lang="stylus">
  .user-recommend-wrap
    height 100%;
    background-color white;
    .user-info-wrap
        width 100%;
        background-color $index_background_color;
        padding-top 17px;
        padding-left 0px;
        position relative;
        font-size 14px;
      p
        padding 8px 17px;
        font-weight bolder;
        border-bottom : 1px solid #aaa;
      .qr-wrap
        margin-left: 30%;
        padding-top: 20px;
        .qr-code
          width: 124px;
          display flex;
          justify-content center
      .user-logo
        display flex;
        justify-content space-between;
        margin 10px 17px;
        height 30px;
      .title-wrap
        display flex
        justify-content center
        margin 20px 17px 0px 17px
      .head-image
        width 25px;
        height 25px;
        border-radius 50%;
      .head-name
        padding-top: 3px;
    .tip-warp
      margin 10px 17px
      font-size 14px
</style>
