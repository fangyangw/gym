<template>
  <div class="details-card-wrap">
      <div class="card-info-wrap">
        <p class="card-name-wrap">
          <span>商品名称</span>
          <span>{{ cardDetails.TYPE }}</span>
        </p>
        <p class="card-time-wrap">
          <span>数量</span>
          <span>1</span>
        </p>
        <p class="card-price-wrap">
          <span>待付金额</span>
          <span>￥{{ price }}</span>
        </p>
        <div class="buy-wrap-common buy-wrap-kibi" @click="buy_use_yibi">易币支付</div>
        <div class="buy-wrap-common" @click="buy">微信支付</div>
      </div>
  </div>
</template>


<script>
import {
    get_card,
    order_pay,
    yibi_order_pay
  } from "@/api/index"
import cards from "@/components/cards"
import { Toast } from 'vant';
import wx from "weixin-js-sdk"
export default {
  components:{
    cards
  },
  data(){
    return{
      cardDetails:{},
      price: 0
    }
  },
  mounted(){
    this.get_card()
  },
  computed:{
    cardid(){
      return this.$route.query.cardid
    },
    open_id(){
      return window.localStorage.getItem("openid")
    }
  },
  methods:{
    buy_use_yibi(){
      let data = {
        "busname": "card",
        "open_id": this.open_id,
        "good_id": this.cardid,
        "description": "pay for month card",
        "total_yibi": this.price
      }
      yibi_order_pay(data).then(res => {
        //成功状态下
        console.log(res)
        if (res.code == 200) {
          Toast.success('支付成功');
          setTimeout(()=>{   //设置延迟执行
            window.location.href = "https://www.ezaifit.top/User"
          },1000);
        }
        else {
          this.$dialog.alert({
            message: res.message,
          });
        }
      });
    },
    buy(){
       //请求后台接口获取数据 准备进行微信支付
      let data = {
        "busname": "card",
        "open_id": this.open_id,
        "good_id": this.cardid,
        "description": "pay for month card",
        "total_fee": parseFloat(this.price * 100)
      }
      order_pay(data).then(res => {
        //成功状态下
        console.log(res)
        if (res.code == 0) {
          // 存储微信支付数据data
          let data = res;
          console.log("即将跳转微信支付", data);

          //函数为分装过得  (就是调用微信支付)
          this.wexinPay(
            {
              appId: "wx6e7157cd6dfbb4ec",
              partnerId: data.partner_id,
              package: "prepay_id=" + data.prepay_id,
              nonceStr: data.nonce_str,
              signType: data.sign_type,
              timeStamp: data.timestamp + '',
              paySign: data.pay_sign
            },
            //成功回调函数
            res => {
              window.location.href = "https://www.ezaifit.top/User"
            },
            res => {
              this.$dialog.alert({
                message: "支付失败",
              });
            }
          );
        }
        else {
          this.$dialog.alert({
            message: res.message,
          });
        }
      });
    },
    wexinPay(data, cb, errorCb) {
        //获取后台传入的数据
        let appId = data.appId;
        let timestamp = data.timeStamp;
        let nonceStr = data.nonceStr;
        let signature = data.signature;
        let packages = data.package;
        let paySign = data.paySign;
        let partnerId = data.partnerId;
        let signType = data.signType;
        console.log('发起微信支付')
        //下面要发起微信支付了
        wx.config({
            debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
            appId: appId, // 必填，公众号的唯一标识
            timestamp: timestamp, // 必填，生成签名的时间戳
            nonceStr: nonceStr, // 必填，生成签名的随机串
            signature: signature, // 必填，签名，见附录1
            jsApiList: ['chooseWXPay'] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
        });
        wx.ready(function () {
            wx.chooseWXPay({
                appId: appId,
                timestamp: timestamp, // 支付签名时间戳，注意微信jssdk中的所有使用timestamp字段均为小写。但最新版的支付后台生成签名使用的timeStamp字段名需大写其中的S字符
                nonceStr: nonceStr, // 支付签名随机串，不长于 32 位
                package: packages, // 统一支付接口返回的prepay_id参数值，提交格式如：prepay_id=***）
                signType: signType, // 签名方式，默认为'SHA1'，使用新版支付需传入'MD5'
                paySign: paySign, // 支付签名
                success: function (res) {
                    // 支付成功后的回调函数
                    cb(res);
                },
                fail: function (res) {
                    //失败回调函数
                    errorCb(res);
                }
            });
        });
        wx.error(function (res) {
            // config信息验证失败会执行error函数，如签名过期导致验证失败，具体错误信息可以打开config的debug模式查看，也可以在返回的res参数中查看，对于SPA可以在这里更新签名。
            /*alert("config信息验证失败");*/
        });
    },
    get_card(){
      get_card({params:{
        open_id: this.open_id
      }}).then(res => {
        if(res.code == 200){
          // this.cardDetails = res.data
          res.data.forEach(item => {
            if(item.CID == this.cardid){
              this.cardDetails = item
              this.price = (item.discount_price) ? item.discount_price : item.PRICE
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
  .buy-wrap-common
    width 90%;
    height 45px;
    border-radius 8px;
    background-color #27A844;
    margin-top: 30px;
    margin-left: 17px;
    color white;
    font-size 15px;
    display flex;
    justify-content center;
    align-items center;
    left 0;
    z-index 1000;
    letter-spacing 2px;
  .buy-wrap-kibi
    background-color #DD3648;
</style>
