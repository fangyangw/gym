<template>
  <div class="user-phone-warp">
    <!-- 手机号 -->
    <div class="phone-input">
      <span>手机号:</span>
      <inputgroup
        type="number"
        placeholder="手机号"
        v-model="phone"
        :btnTitle="btnTitle"
        :disabled="disabled"
        :error="errors.phone"
        @btnClick="getVerifyCode"
      />
    </div>
    <!-- 输入验证码 -->
    <div class="phone-input">
      <span>验证码:</span>
      <inputgroup
        type="number"
        v-model="verifyCode"
        placeholder="验证码"
        :error="errors.code"
      />
    </div>
    <!-- 登录按钮 -->

    <div class="binding-phone" @click="save_phone" :disabled="isClick">
      绑定手机号
    </div>
  </div>
</template>

<script>
import inputgroup from "@/components/InputGroup";
import {
  get_user_info_details,
  send_verification,
  save_phone
} from "@/api/index";

export default {
  components: {
    inputgroup: inputgroup
  },
  data() {
    return {
      phone: "", //手机号
      verifyCode: "", //验证码
      btnTitle: "获取验证码",
      disabled: false, //是否可点击
      errors: {} //验证提示信息
    };
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
    recommend_id() {
      return window.localStorage.getItem("recommend_id");
    },
    //手机号和验证码都不能为空
    isClick() {
      if (!this.phone || !this.verifyCode) {
        return true;
      } else {
        return false;
      }
    }
  },
  methods: {
    getVerifyCode() {
      if (this.validatePhone()) {
        //发送网络请求
        send_verification({
          open_id: this.openid,
          phone_number: this.phone
        }).then(res => {
          this.validateBtn();
          console.log(res);
          if (res.code != 0) {
            this.$dialog.alert({
              message: res.message
            });
          } else {
            this.$dialog.info({
              message: "发送成功"
            });
          }
        });
      }
    },
    validatePhone() {
      //判断输入的手机号是否合法
      if (!this.phone) {
        this.errors = {
          phone: "手机号码不能为空"
        };
        // return false
      } else if (!/^1[3456789]\d{9}$/.test(this.phone)) {
        this.errors = {
          phone: "请输入正确的手机号"
        };
        // return false
      } else {
        this.errors = {};
        return true;
      }
    },
    validateBtn() {
      //倒计时
      let time = 60;
      let timer = setInterval(() => {
        if (time == 0) {
          clearInterval(timer);
          this.disabled = false;
          this.btnTitle = "获取验证码";
        } else {
          this.btnTitle = time + "秒后重试";
          this.disabled = true;
          time--;
        }
      }, 1000);
    },

    save_phone() {
      this.errors = {};
      save_phone({
        open_id: this.openid,
        phone_number: this.phone,
        verification_code: this.verifyCode,
        recommend_id: this.recommend_id
      }).then(res => {
        console.log(res);
        if (res.code != 0) {
          this.$dialog.alert({
            message: res.message
          });
        } else {
          window.location.href = "https://www.ezaifit.top/User";
        }
      });
    },
    get_user_info_details() {
      get_user_info_details({
        OPENID: this.openid
      }).then(res => {
        console.log(res);
        if (res.code == 200) {
          this.userinfo = res.data[0];
          this.total_card = res.total_card;
          this.total_class = res.total_class;
        }
      });
    }
  }
};
</script>

<style lang="stylus">
.user-phone-warp
  margin-top 30px;
  .phone-input
    margin 10px 10px 0px 20px;
    display flex;
    font-size 15px;
    align-items left;
    span
      margin-right 10px;
      margin-top 2px;
  .binding-phone
      width 90%;
      height 35px;
      border-radius 8px;
      background-color #3478d2;
      margin-top: 20px;
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
