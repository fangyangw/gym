<template>
  <div class="check-user-wrap">
    <div class="user-info-wrap">
      <div class="qr-wrap">
        <div class="img-warp">
          <img src="@/assets/qrcode.png">
        </div>

      </div>
      <div class="qr-title">
        <span style="color: red;font-size: 16px;">完成任务领取送1天会员</span>, 请按如下步骤进行操作:
      </div>
    </div>
    <div class="user-info-wrap">
      <div>
        <p style="border-top : 1px solid #aaa;">1、长按上面二维码, 关注公众号<input type="checkbox" disabled v-model="subscribe"></p>
      </div>
      <div @click="go('/User/Phone')">
        <p>2、绑定手机号码<input type="checkbox" disabled v-model="check_phone"></p>
      </div>
      <div @click="go('/User/UploadPhoto')">
        <p>3、上传人脸识别头像<input type="checkbox" disabled v-model="check_photo"></p>
      </div>
    </div>
    <div class="tips-info-wrap">
    </div>
    <div class="a-wrap">
      <router-link to="/AboutClass?status=ok">下次再说 </router-link>
    </div>
  </div>
</template>

<script>
import { get_user_info_details } from "@/api/index";
export default {
  data(){
    return{
      link: 'https:///www.ezaifit.top',
      userinfo:{},
      total_class: 0,
      total_card: 0,
      subscribe: false,
      check_photo: false,
      check_phone: false
    }
  },
  components:{
    // "van-popup":Popup
  },
  mounted(){
    if(this.openid){
      this.get_user_info_details()
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
    go(url){
      this.$router.push({
          path: url,
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
          this.check_photo = (this.userinfo.PICTURE && this.userinfo.PICTURE + '' != "0") ? true:false
          this.check_phone = (this.userinfo.PHONE && this.userinfo.PHONE + '' != "0") ? true:false
          this.subscribe = (res.subscribe == 1) ? true:false
        }
      })
    }
  }
}
</script>
<style lang="stylus">
.check-user-wrap
  height 100%;
  background-color white;
  div
    box-sizing border-box;
  .tips-info-wrap
    font-size 14px;
    margin 10px 17px
  .user-info-wrap
      background-color $index_background_color;
      padding-top 17px;
      padding-left 0px;
      position relative;
      font-size 14px;
    p
      display flex;
      justify-content space-between;
      padding 8px 17px;
      font-weight bolder;
      border-bottom : 1px solid #aaa;
    .qr-title
      display flex;
      justify-content center;
      font-size 16px;
      font-weight bolder;
    .qr-wrap
      width: 100%;
      display flex;
      justify-content center;
      .img-warp
        height 50%;
        width 50%;
        img
          height 100%;
          width 100%;
    .a-wrap
      display flex
      justify-content center
      font-size 16px
      font-weight bolder
      margin-top 20px
</style>
