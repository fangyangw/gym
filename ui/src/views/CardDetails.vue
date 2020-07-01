<template>
  <div class="details-card-wrap">
      <div class="show-card-wrap">
        <cards :data=cardDetails></cards>
      </div>
      <div class="card-info-wrap">
        <p class="card-name-wrap">
          <span>卡名称</span>
          <span>{{ cardDetails.TYPE }}</span>
        </p>
        <p class="card-time-wrap">
          <span>有效期</span>
          <span>{{ cardDetails.INDATE }}</span>
        </p>
        <p class="card-price-wrap">
          <span>售价</span>
          <span>￥{{ cardDetails.PRICE }}</span>
        </p>
      </div>
      <!-- 购卡协议 -->
      <agreement :is_renewal=RENEWAL ></agreement>
      <!-- 购买按钮 -->
      <div class="checkbox-warp">
        <van-checkbox v-model="checked"  shape="square">我已经阅读并同意上述协议</van-checkbox>
      </div>
      <div style="height: 100px;">
      </div>
      <div class="buy-wrap" @click="buy(cardDetails.CID)">确认购买</div>
  </div>
</template>

<script>
import {
    get_card,
    getsalelist
  } from "@/api/index"
import cards from "@/components/cards"
import agreement from "@/components/agreement"
import { Checkbox} from 'vant';
import { Toast } from 'vant';
export default {
  components:{
    cards,
    agreement
  },
  data(){
    return{
      cardDetails:{},
      checked: true,
      RENEWAL: false
    }
  },
  mounted(){
    this.get_card()
  },
  computed:{
    cardid(){
      return this.$route.query.cardid
    }
  },
  methods:{
    buy(id){
      if (!this.checked) {
        Toast('请阅读并同意上述协议');
      } else {
        this.$router.push({
          path: `/OrderDetails/?cardid=${id}`,
        })
      }
    },
    get_card(){
      get_card().then(res => {
        if(res.code == 200){
          // this.cardDetails = res.data
          res.data.forEach(item => {
            if(item.CID == this.cardid){
              this.cardDetails = item
              this.RENEWAL = this.cardDetails.TYPE === "连续包月卡"
            }
          })
        }
      })
    }
  }
}
</script>

<style lang="stylus">
.details-card-wrap
  p
    padding 0;
    margin 0;
  .show-card-wrap
    box-sizing border-box;
    padding 14px;
  .card-info-wrap
    width 100%;
    background-color white;
    font-size 13px;
    padding 14px 0;
    box-shadow 0 2px 12px 0 rgba(0,0,0,.1);
    .card-time-wrap
      padding-top 14px;
      padding-bottom 14px;
    p
      display flex;
      justify-content space-between;
      align-items center;
      box-sizing border-box;
      padding 0 14px;
      // font-weight bold;
      & span:nth-child(1){
        // font-size 29px;
        // font-weight 600;
      }
  .buy-wrap
    width 100%;
    height 50px;
    border-radius 8px;
    background-color #3478d2;
    color white;
    font-size 15px;
    display flex;
    justify-content center;
    align-items center;
    position fixed;
    bottom 0;
    left 0;
    z-index 1000;
    letter-spacing 2px;
  .checkbox-warp
    font-size 16px
    background-color #ffffff
    padding 0px 10px 20px 10px 
</style>
