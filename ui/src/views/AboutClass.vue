<template>
  <div class="about-class-wrap">
    <son-class v-for="(item,index) in courses" :course_detail=item :is_buy=true></son-class>
  </div>
</template>

<script>
import sonclass from "@/components/class";
import {
  get_user_info,
  get_user_info_details,
  get_course
} from "@/api/index"
export default {
  name: 'AboutClass',
  data(){
    return {
      user: {},
      courses: []
    }
  },
  components:{
    'son-class':sonclass
  },
  mounted(){
    this.get_course()
    if(this.openid){
      if(!this.$route.query.status){
        this.check_user_status()
      }
    }
  },
  computed:{
    openid(){
      return window.localStorage.getItem("openid")
    }
  },
  methods:{
    check_user_status(){
      get_user_info_details({
        "OPENID":this.openid
      }).then(res => {
        console.log("check user status", res)
        if(res.code == 200){
          this.user = res.data[0]
          if((this.user.PICTURE && this.user.PICTURE + '' != 0) && (this.user.PHONE && this.user.PHONE + ''!= "0") && res.subscribe == 1){

          }else{
            window.location.href = "https:///www.ezaifit.top/CheckUserRecommend"
          }
        }
      })
    },
    get_course(){
      get_course().then(res => {
        if(res.code == 200){
          this.courses = res.data
        }
      })
    }
  }
}
</script>

<style lang="stylus">
.about-class-wrap
  width 100%;
  box-sizing border-box;
  // padding 40px 0;
  padding 10px 0;
  display flex;
  flex-wrap wrap;
  margin-bottom 550px
  // justify-content space-around;
  // align-content space-around;
</style>
