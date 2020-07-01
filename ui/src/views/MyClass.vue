<template>
  <div class="my-class-wrap">
    <div class="title-wrap">
        <div class="title-color-warp">
            <p>我的约课</p>
        </div>
    </div>
    <div v-if="my_courses.length == 0" class="no-data-wrap"><span>暂无数据..</span>.</div>
    <son-class v-else v-for="(item,index) in my_courses" :course_detail=item></son-class>
  </div>
</template>

<script>
import sonclass from "@/components/class";
import { Tag } from 'vant';
import {
  get_user_info,
  get_user_info_details,
  get_my_course
} from "@/api/index"
export default {
  name: 'MyClass',
  data(){
    return {
      user: {},
      my_courses: []
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
        }
      })
    },
    get_course(){
      get_my_course({
        'open_id': this.openid
      }).then(res => {
        if(res.code == 200){
          this.my_courses = res.data
        }
      })
    }
  }
}
</script>

<style lang="stylus">
.my-class-wrap
  width 100%;
  box-sizing border-box;
  padding 10px 0;
  .title-wrap
        font-size 20px;
        margin 10px;
        color #ffffff
    .title-color-warp
        background-color #f2826a
        padding 5px
  .no-data-wrap
    margin 20px 0px
    display flex
    justify-content center
    font-size 16px
</style>
