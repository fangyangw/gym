<template>
  <div class="buy-cards-wrap">
    <cards v-for="(item,index) in cardlist" :key='index' :data=item :is_buy=true></cards>
  </div>
</template>

<script>
  import cards from "@/components/cards"
  import {
    get_card,
    getsalelist,
    get_user_info_details,
  } from "@/api/index"
  export default {
    data(){
      return{
        cardlist:[]
      }
    },
    components: {
      cards
    },
    mounted(){
      this.get_card()
      if(this.openid){
        if(!this.$route.query.status){
          // this.check_user_status()
        }
      }
    },
    computed:{
      openid(){
        return window.localStorage.getItem("openid")
      }
    },  
    methods: {
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
      toDetails(id) {
        console.log("1111111111")
        this.$router.push({
          name: 'DetailsCard',
          params: {
            cardid: '123445789'
          }
        })
      },
      get_card(){
        get_card().then(res => {
          console.log(res, '-=-')
          if(res.code == 200){
            this.cardlist = res.data
          }
        })
      }
    }
  }

</script>

<style lang="stylus">
  // .cards-wrap
  .buy-cards-wrap
    padding 14px;
    margin-bottom 550px
    p
        padding 0;
        margin 0;

</style>
