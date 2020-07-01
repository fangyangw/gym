// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import 'normalize.css/normalize.css'
// import axios from 'axios'

// import Vue from 'vue';
import Vant from 'vant';
import moment from "vue-moment"
import 'vant/lib/index.css';
Vue.use(Vant)
Vue.use(moment)
Vue.config.productionTip = false

router.beforeEach ((to, from, next) => {
  var u = navigator.userAgent;
  var isiOS = !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/); //ios终端
  console.log("=======isiOS========")
  console.log(isiOS)
  if (isiOS && to.path !== location.pathname) {
    // 此处不可使用location.replace
    console.log("=======fullPath========")
    console.log(to.fullPath)
    location.assign(to.fullPath)
  } else {
    next()
  }
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

