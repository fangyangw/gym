<template>
  <div  v-if="is_buy" class="cards-wrap" @click="toDetails(data.CID)">
      <!-- <div class=""></div> -->
      <div class="logo-and-title">
          <i class="logo">EZFIT</i>
          <span class="title">易/在/24H/健/身</span>
      </div>
      <div class="card-info">
          <span>{{  data.NAME }}</span>
      </div>
      <div class="card-remark">
          <span>{{data.TYPE}},{{ data.INDATE }}</span>
      </div>
      <div class="card-xufei">
<!--           <span>到期自动续费</span> -->
      </div>
  </div>
  <div v-else class="cards-wrap">
      <!-- <div class=""></div> -->
      <div class="logo-and-title">
          <i class="logo">EZFIT</i>
          <span class="title">易/在/24H/健/身</span>
      </div>
      <div class="card-info">
          <span>{{  data.NAME }}</span>
      </div>
      <div class="card-remark">
          <span>{{data.TYPE}},{{ data.INDATE }}</span>
      </div>
      <div class="card-xufei">
          <!-- <span>到期自动续费</span> -->
      </div>
  </div>
</template>

<script>
export default {
    name:"cards",
    props:{
        data:{
            type:Object
        },
        is_buy: Boolean,
    },
    methods:{
        toDetails(id) {
         this.$router.push({
          path: `/DetailsCard/?cardid=${id}`,
        })
      }
    }
}
</script>

<style lang="stylus">
.cards-wrap
    width 100%;
    height 150px;
    border-radius 12px;
    background-image url('../assets/VIP.png');
    background-repeat no-repeat;
    background-size 100% 100%;
    box-sizing border-box;
    padding 14px;
    padding-left 29px;
    color white;
    .logo-and-title
        display flex;
        justify-content space-between;
        align-items flex-end;
        .logo
            font-size 18px;
            color red;
            letter-spacing 3px;
            font-weight bold;
        .title
            color white;
            font-size 12px;
    .card-info
        color white;
        font-size 20px;
        padding-top 14px;
        font-weight bold;
        letter-spacing 2px;
    .card-remark
        font-size 12px;
        padding-top 10px;
    .card-xufei
        font-size 11px;
        padding-top 16px;

</style>