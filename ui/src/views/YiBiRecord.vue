<template>
  <div class="yibi-class-wrap">
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
    <van-list
        v-model="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
    >
        <van-cell v-for="item in yibi_orders" :key="item.id" :title="item.total_yibi" :value="item.update_time"/>
    </van-list>
    </van-pull-refresh>
  </div>
</template>

<script>
import { List } from 'vant';
import moment from "vue-moment"

import {
  get_user_info,
  get_user_info_details,
  get_yibi_order
} from "@/api/index"
export default {
  name: 'YiBiRecord',
  data(){
    return {
      user: {},
      yibi_orders: [],
      loading: false,
      finished: false,
      refreshing: false,
    }
  },
  components:{
  },
  mounted(){
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

        }
      })
    },
    onLoad() {
      get_yibi_order({
        "open_id": this.openid
      }).then(res => {
        if(res.code == 200){
          this.yibi_orders = []
          for(let i=0; i < res.data.length; i++){
            let operation = (res.data[i].payee == this.openid) ? "+" : "-"
            this.yibi_orders.push({
              "id": i+1,
              "total_yibi": "易币：" + operation + res.data[i].total_yibi,
              "update_time": this.dateFormat("YYYY-mm-dd HH:MM:SS", new Date(res.data[i].update_time))
            })
          }
          this.finished = true
        }
      })
    },
    onRefresh() {
      // 清空列表数据
      this.finished = false;

      // 重新加载数据
      // 将 loading 设置为 true，表示处于加载状态
      this.loading = true;
      this.onLoad();
    },
    dateFormat(fmt, date) {
      let ret;
      const opt = {
          "Y+": date.getFullYear().toString(),        // 年
          "m+": (date.getMonth() + 1).toString(),     // 月
          "d+": date.getDate().toString(),            // 日
          "H+": date.getHours().toString(),           // 时
          "M+": date.getMinutes().toString(),         // 分
          "S+": date.getSeconds().toString()          // 秒
          // 有其他格式化字符需求可以继续添加，必须转化成字符串
      };
      for (let k in opt) {
          ret = new RegExp("(" + k + ")").exec(fmt);
          if (ret) {
              fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
          };
      };
      return fmt;
  }
  }
}
</script>

<style lang="stylus">
.yibi-class-wrap
  width 100%;
</style>
