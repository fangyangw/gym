<template>
  <div id="app">
    <router-view />
    <div class="nav-wrap">
      <span class="nav_right_border" :style="{'color': RouterName == 'AboutClass' ? 'red' : 'black'}"
        @click="go('/AboutClass?status=ok')">约课</span>
      <span class="nav_right_border" :style="{'color': RouterName == 'BuyingCards' ? 'red' : 'black'}"
        @click="go('/BuyingCards')">购卡</span>
      <span :style="{'color': RouterName == 'User' ? 'red' : 'black'}" @click="go('/User')">我的</span>
      <!-- <span :style="{'color': RouterName == 'User' ? 'red' : 'black'}" @click="wechat">我的</span> -->
    </div>
  </div>
</template>

<script>
import {
  get_user_info,
  get_user_info_details
} from "@/api/index"
  export default {
    name: 'App',
    data() {
      return {
        appid: "wx6e7157cd6dfbb4ec",
        redirect_uri: "https:///www.ezaifit.top/CheckUserRecommend",
        user: {}
      }
    },
    mounted() {
      this.rem()
      if(this.$route.query.recommend_id){
        window.localStorage.setItem("recommend_id", this.$route.query.recommend_id)
      }
      if(!this.IsLogin){
        console.log(this.$route.query.code, '---')
        if(this.$route.query.code){
          console.log("32222222222")
          this.get_user_info(this.$route.query.code)
        }else{
          console.log("111111111")
          this.wechat()
        }
      }else{
        this.get_user_info(this.$route.query.code)
      }
    },
    computed: {
      RouterName() {
        return this.$route.name
      },
      username(){
        return window.localStorage.getItem('username')
      },
      userimage(){
        return window.localStorage.getItem('userimage')
      },
      openid(){
        return window.localStorage.getItem('openid')
      },
      IsLogin(){
        if(this.username && this.userimage && this.openid){
          return true
        }else{
          return false
        }
      }
    },
    methods: {
      go(url) {
        if(!this.IsLogin){
          if(this.$route.query.code){
            this.get_user_info(this.$route.query.code)
          }else{
            this.wechat()
          }
        }
        this.$router.push(url)
      },
      wechat() {
        window.location.href =
          `https://open.weixin.qq.com/connect/oauth2/authorize?appid=${this.appid}&redirect_uri=${this.redirect_uri}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect`
      },
      rem() {
        // console.log(this.$route.name)
        let htmlWidth = document.documentElement.clientWidth ||
          document.body.clientWidth;
        console.log(htmlWidth);
        //获取htmlDom
        let htmlDom = document.getElementsByTagName('html')[0];
        //设置html的font-size
        htmlDom.style.fontSize = htmlWidth / 10 + 'px';

        window.addEventListener('resize', (e) => {
          let htmlWidth = document.documentElement.clientWidth ||
            document.body.clientWidth;
          console.log(htmlWidth);
          //获取htmlDom
          let htmlDom = document.getElementsByTagName('html')[0];
          //设置html的font-size
          htmlDom.style.fontSize = htmlWidth / 10 + 'px';
        })
      },
      get_user_info(code){
        get_user_info({
          "code":code,
          "open_id": this.openid
        }).then(res => {
          if(res.code == 200){
            window.localStorage.setItem("username",res.data.nickname)
            if(res.data.headimgurl){
              window.localStorage.setItem("userimage",res.data.headimgurl)
            }else{
              window.localStorage.setItem("userimage", "../assets/touxiang.png")
            }
            window.localStorage.setItem("openid",res.data.openid)
          }
        })
      }
    }
  }

</script>
<style lang="stylus">
  html,body
    width 100%;
    height 100%;
    background-color: $index_background_color;
    p
      padding 0;
      margin 0;
  #app
      background-color: $index_background_color;
      width 100%;
      height 100%;
      font-family 'Microsoft YaHei;'
      -webkit-font-smoothing antialiased;
      -moz-osx-font-smoothing grayscale;
      .nav-wrap
        font-size 15px;
        background-color #fefefe;
        width 100%;
        height 36px;
        box-sizing border-box;
        padding 12px 0;
        text-align center;
        position fixed;
        bottom 0;
        left 0;
        box-shadow 0 2px 12px 0 rgba(0, 0, 0, .1);
        span
          display inline-block;
          box-sizing border-box;
          width 32%;
          font-weight normal;

</style>
