<template>
  <div class="my-cards-wrap">
    <div class="title-wrap">
        <div class="title-color-warp">
            <p>我的会员卡</p>
        </div>
    </div>
    <div v-if="cardlist.length == 0" class="no-data-wrap"><span>暂无数据..</span>.</div>
    <cards v-else v-for="(item,index) in cardlist" :key='index' :data=item :is_buy=false></cards>
  </div>
</template>

<script>
  import cards from "@/components/cards"
  import {
    get_card,
    getsalelist,
    get_my_card
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
    computed:{
      openid(){
        return window.localStorage.getItem('openid')
      }
    },
    mounted(){
      this.get_card()
    },
    methods: {
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
        get_my_card({
          "open_id": this.openid
        }).then(res => {
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
  .my-cards-wrap
    padding 14px;
    p
        padding 0;
        margin 0;
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
