<template>
  <div class="user-index-wrap">
    <div class="user-info-wrap">
      <div class="user-name">{{ username }}</div>
      <!-- <div class="user-iphone">
        <img src="@/assets/iphone.png" alt="">
        <span>13013818600</span>
      </div>-->
      <div class="user-card-info">
        <div @click="go('/YiBiRecord')">
          <span v-if="userinfo.YIBI != null">{{ userinfo.YIBI }}</span>
          <span v-else>0</span>
          <span>易币</span>
        </div>
        <div @click="go('/MyClass')">
          <span v-if="userinfo.COURSE_ID != null">
            {{
            userinfo.COURSE_ID
            }}
          </span>
          <span v-else>{{ total_class }}</span>
          <span>课时</span>
        </div>
        <div @click="go('/MyCard')">
          <span v-if="userinfo.CARD_ID != null">{{ userinfo.CARD_ID }}</span>
          <span v-else>{{ total_card }}</span>
          <span>卡片</span>
        </div>
      </div>
      <!-- 头像 -->
      <img class="touxiang" :src="userimage" alt />
      <!-- 会员卡日期 -->
      <div class="mb-card-wrap">
        <div class="card">
          <div class="left">
            <div>
              <i>VIP</i>
              <span>剩余天数</span>
              <span>{{ this.remain_day }}天</span>
            </div>
            <div>会员号: {{ userinfo.MID }}</div>
          </div>
          <div class="right">
            <div class="xuyue" @click="go('/BuyingCards')">立即续约</div>
          </div>
        </div>
      </div>
    </div>
    <div class="function-wrap">
      <div class="function-item" @click="go('/User/UploadPhoto')">
        <img src="@/assets/ren.png" alt />
        <span>门禁入场照片</span>
      </div>
      <div class="function-item" @click="exchangeYiBi()">
        <img src="@/assets/qianbao.png" alt />
        <span>易币兑换</span>
      </div>
      <!-- <div class="function-item">
        <img src="@/assets/suo.png" alt="">
        <span>支付密码</span>
      </div>-->
      <div class="function-item" @click="go('/User/UserRecommend')">
        <img src="@/assets/share.png" alt />
        <span>我的分享</span>
      </div>
      <div class="function-item">
        <img class="erji-img" src="@/assets/erji.png" alt />
        <a href="tel:19941850923">
          <span style="color: black;">联系客服</span>
        </a>
      </div>
      <div class="function-item" @click="go('/User/Phone')">
        <img src="@/assets/iphone.png" alt />
        <span>{{ this.user_phone }}</span>
      </div>
      <div class="function-item" @click="navgation()">
        <img src="@/assets/feiji.png" alt />
        <span>导航到店</span>
      </div>
    </div>
    <!-- <van-popup v-model="show">内容</van-popup> -->
  </div>
</template>

<script>
import { get_app_sign, get_user_info_details } from "@/api/index";
import wx from "weixin-js-sdk";
import moment from "vue-moment";

export default {
  data() {
    return {
      show: false,
      userinfo: {},
      total_class: 0,
      total_card: 0,
      remain_day: 0
    };
  },
  components: {
    // "van-popup":Popup
  },
  mounted() {
    if (this.openid) {
      this.get_user_info_details();
    }
  },
  computed: {
    username() {
      return window.localStorage.getItem("username");
    },
    userimage() {
      return window.localStorage.getItem("userimage");
    },
    openid() {
      return window.localStorage.getItem("openid");
    },
    user_phone() {
      if (
        this.userinfo.PHONE &&
        this.userinfo.PHONE != 0 &&
        this.userinfo.PHONE != "0"
      ) {
        return this.userinfo.PHONE;
      } else {
        return "绑定手机号";
      }
    }
  },
  methods: {
    kehu() {
      this.$dialog.alert({
        message: "客服电话：18962513837"
      });
    },
    go(url) {
      console.log("test=======");
      this.$router.push({
        path: url
      });
    },
    navgation() {
      let that = this;
      get_app_sign({
        open_id: this.openid,
        location: window.location.href,
        open_location: "yes"
      }).then(
        res => {
          if (res.code == 0) {
            wx.config({
              debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
              appId: "wx6e7157cd6dfbb4ec", // 必填，公众号的唯一标识
              timestamp: res.timestamp, // 必填，生成签名的时间戳
              nonceStr: res.nonce_str, // 必填，生成签名的随机串
              signature: res.pay_sign, // 必填，签名，见附录1
              jsApiList: ['closeWindow','openLocation', 'getLocation']// 必填，需要使用的JS接口列表，所有JS接口列表见附录2
            });
            wx.getLocation({//
              type:'gcj02', // 默认为 wgs84 返回 gps 坐标，gcj02 返回可用于 wx.openLocation 的坐标
              success: function (res) {
                // alert("纬度:" + res.latitude + " 经度:" + res.longitude)
                console.log(res.latitude); console.log(res.longitude);
                wx.openLocation({
                  latitude: 31.214212, // res.latitude, 纬度，范围为-90~90，负数表示南纬
                  longitude: 120.58769, //res.longitude, 经度，范围为-180~180，负数表示西经
                  scale: 15, // 缩放比例
                  name:"易在24h健身馆",
                  address:"江苏省苏州市吴中区越湖路1111号18幢101室2楼",
                  success:function(r){
                    console.log(r)
                  }
                })
              }
            })

          } else {
            this.$dialog.alert({
              message: "打开导航失败"
            });
          }
        },
        res => {
          this.$dialog.alert({
            message: "打开导航失败"
          });
        }
      );
    },
    exchangeYiBi() {
      this.$dialog.alert({
        message: "请在约课和购卡页面直接购买！"
      });
    },
    get_user_info_details() {
      get_user_info_details({
        OPENID: this.openid
      }).then(res => {
        console.log(res);
        if (res.code == 200) {
          this.userinfo = res.data[0];
          //  "REMAIN_TIME": "2020-06-13 17:40:49"
          if (res.REMAIN_TIME && res.REMAIN_TIME + "" != "") {
            //let now = this.$moment()
            //let remain_time = this.$moment(res.REMAIN_TIME)
            //this.remain_day = (remain_time.diff(now, 'day') > 0) ? remain_time.diff(now, 'day') + 1 : 0
            this.remain_day = res.REMAIN_TIME;
          }
          this.total_card = res.total_card;
          this.total_class = res.total_class;
        }
      });
    }
  }
};
</script>
<style lang="stylus">
.user-index-wrap {
  height: 100%;
  background-color: white;

  div {
    box-sizing: border-box;
  }

  .user-info-wrap {
    background-color: $index_background_color;
    padding-top: 17px;
    position: relative;

    .user-name {
      padding-left: 45px;
      font-size: 24px;
      font-weight: bold;
    }

    .user-iphone {
      padding-left: 45px;
      color: #939799;
      font-size: 12px;
      display: flex;
      align-items: center;
      padding-top: 9px;

      img {
        width: 9px;
        height: 13px;
        margin-right: 5px;
      }
    }

    .user-card-info {
      display: flex;
      align-items: center;
      padding-left: 25px;
      padding-top: 25px;

      div {
        display: flex;
        flex-direction: column;
        font-size: 15px;
        color: #939799;
        text-align: center;
        margin-left: 20px;

        span:nth-child(1) {
          color: red;
          font-size: 24px;
          font-weight: bold;
          margin-left: 0;
          margin-bottom: 10px;
        }
      }
    }

    .touxiang {
      width: 90px;
      height: 90px;
      border-radius: 50%;
      position: absolute;
      top: 12.5px;
      right: 24px;
    }

    .mb-card-wrap {
      // text-align center;
      padding-top: 30px;
      display: flex;
      justify-content: center;

      .card {
        color: #ffffff;
        font-size: 12px;
        height: 94px;
        width: 90%;
        background-image: url('../assets/userbac.png');
        background-repeat: no-repeat;
        background-size: 100% 100%;
        box-sizing: border-box;
        border-radius: 15px;
        box-sizing: border-box;
        padding: 15px;
        display: flex;
        align-items: center;
        justify-content: space-between;

        .left {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          height: 100%;
          padding-left: 9px;

          div:nth-child(1) {
            i {
              color: red;
              font-size: 24px;
            }

            span {
              padding-left: 12px;
            }
          }

          div:nth-child(2) {
            padding-left: 10px;
            margin-bottom: 10px;
            // box-sizing border-box;
          }
        }

        .right {
          // height 100%;
          padding-right: 12.5px;

          .xuyue {
            box-sizing: border-box;
            color: white;
            background-color: red;
            border-radius: 12px;
            width: 79px;
            height: 24px;
            display: flex;
            justify-content: center;
            align-items: center;
          }
        }
      }
    }
  }

  .function-wrap {
    background-color: white;
    width: 100%;
    height: 150px;
    position: relative;
    margin-top: -15px;
    display: flex;
    flex-wrap: wrap;
    font-size: 15px;
    padding: 21.5px 14px;

    .function-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 33%;
      margin-top: 40px;

      // text-align center;
      img {
        width: 25px;
        height: 22.5px;
        margin-bottom: 10px;
      }

      .erji-img {
        width: 30px;
        height: 22px;
      }
    }
  }
}
</style>
