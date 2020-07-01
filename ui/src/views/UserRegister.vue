<template>
  <div class="user-register-wrap">
    <div class="user-info-wrap">
      <div class="qr-wrap">
        <div id="qrcode" class="qr-code"></div>
      </div>
      <span style="font-size: 15px; position: relative; align-items:center; top: 40px;">扫描上面的二维码加入易在24h运动<br/>让自己变得更健康更强壮吧</span>
    </div>
    <div class="user-info-wrap">
       <p>邀请我的人：</p>
       <p>我邀请的人：</p>
    </div>
  </div>
</template>

<script>
import { get_user_info_details } from "@/api/index";
import QRCode from 'qrcodejs2';
export default {
  data(){
    return{
      link: 'https:///www.ezaifit.top',
      userinfo:{},
      total_class: 0,
      total_card: 0
    }
  },
  components:{
    // "van-popup":Popup
  },
  mounted(){
    if(this.openid){
      //this.get_user_info_details()
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
            text:  this.link + '?recommand_id=' + this.openid,   // 二维码内容
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
        }
      })
    }
  }
}
</script>
<style lang="stylus">
.user-register-wrap
  height 100%;
  background-color white;
  div
    box-sizing border-box;
  .user-info-wrap
      background-color $index_background_color;
      padding-top 17px;
      position relative;
    .qr-wrap
      width: 100%;
      margin-left: 30%;
      padding-top: 20px;
      .qr-code
        width: 124px;
        display flex;
</style>
