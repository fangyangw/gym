<template>
  <div class="user-upload-wrap">
    <div class="user-info-wrap">
      <div v-if="is_loading">
        <van-loading size="24px" vertical>加载中...</van-loading>
      </div>
      <img v-else class="user-photo" :src="photo" />
    </div>
    <div class="user-info-wrap">
      <buthaton class="upload-buthaton" @click="upload_photo()">
        <span v-if="have_upload">更改照片</span>
        <span v-else>上传照片</span>
      </buthaton>
    </div>
  </div>
</template>

<script>
import {
  get_user_info_details,
  get_app_sign,
  update_member_info,
  get_user_image
} from "@/api/index";
import wx from "weixin-js-sdk";
import { Loading } from 'vant';
export default {
  data() {
    return {
      link: "hthatps:///www.ezaifit.top",
      local_ids: "",
      error: "",
      have_upload: false,
      photo: null,
      show: false,
      is_loading: true,
    };
  },
  components: {
    // "van-popup":Popup
  },
  mounted() {
    if (this.openid) {
      this.get_user_info_details();
      this.get_photo();
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
    }
  },
  methods: {
    upload_photo() {
      let that = this;
      get_app_sign({
        open_id: this.openid,
        location: window.location.href
      }).then(
        res => {
          if (res.code == 0) {
            wx.config({
              debug: false, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
              appId: "wx6e7157cd6dfbb4ec", // 必填，公众号的唯一标识
              timestamp: res.timestamp, // 必填，生成签名的时间戳
              nonceStr: res.nonce_str, // 必填，生成签名的随机串
              signature: res.pay_sign, // 必填，签名，见附录1
              jsApiList: ["chooseImage", "uploadImage"] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
            });
            wx.chooseImage({
              count: 1, // 默认9
              sizeType: ["compressed"], // 可以指定是原图还是压缩图，默认二者都有
              sourceType: ["album", "camera"], // 可以指定来源是相册还是相机，默认二者都有
              success: function(res) {
                let local_id = res.localIds[0]; // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片
                wx.uploadImage({
                  localId: local_id, // 需要上传的图片的本地ID，由chooseImage接口获得
                  isShowProgressTips: 1, // 默认为1，显示进度提示
                  success: function(res1) {
                    update_member_info({
                      server_id: res1.serverId,
                      open_id: that.openid,
                      recommend_id: that.recommend_id
                    }).then(res => {
                      if (res.code == 500) {
                        that.$dialog.alert({
                          message: res.message
                        });
                      } else {
                        //重新刷新页面
                        window.location.reload();
                        // that.get_photo();
                      }
                    });
                  }
                });
              },
              error: function(res) {
                that.$dialog.alert({
                  message: res
                });
              }
            });
            wx.error(function(res) {
              that.error = res.errMsg;
              that.$dialog.alert({
                message: res.errMsg
              });
            });
          } else {
            this.$dialog.alert({
              message: "打开手机相机失败"
            });
          }
        },
        res => {
          this.$dialog.alert({
            message: "打开手机相机失败"
          });
        }
      );
    },
    get_photo() {
      get_user_image({
        open_id: this.openid
      }).then(res => {
        this.is_loading = false;
        if (res.code == 0) {
          this.have_upload = true;
          this.photo = res.data;
        } else {
          this.have_upload = false;
          this.photo = null;
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
.user-upload-wrap
  height 100%;
  background-color white;
  div
    box-sizing border-box;
  .user-info-wrap
    background-color $index_background_color;
    padding-top 17px;
    display flex
    justify-content center
    .upload-buthaton
      width 90%;
      height 35px;
      border-radius 8px;
      background-color #3478d2;
      margin-top: 20px;
      color white;
      font-size 15px;
      display flex;
      justify-content center;
      align-items center;
      left 0;
      z-index 1000;
      lethater-spacing 2px;
    .user-photo
      width 200px;
      height 250px;
</style>
