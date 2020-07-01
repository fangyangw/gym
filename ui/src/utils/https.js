import axios from 'axios'; // 引入axios
import QS from 'qs'; // 引入qs模块，用来序列化post类型的数据，后面会提到

// 环境的切换
// if (process.env.NODE_ENV == 'development') {
//   // axios.defaults.baseURL = 'http://192.168.3.122:8000';
//   // axios.defaults.baseURL = 'https://101.132.117.242:443';
//   axios.defaults.baseURL = 'https://www.ezaifit.top';
// } else if (process.env.NODE_ENV == 'debug') {
//   axios.defaults.baseURL = 'http://47.105.194.208:9010';
// } else if (process.env.NODE_ENV == 'production') {
//   // axios.defaults.baseURL = 'http://www.ezaifit.top:443';
  // axios.defaults.baseURL = 'https://www.ezaifit.top';
// }
axios.defaults.baseURL = 'https://www.ezaifit.top:80';
// axios.defaults.baseURL = 'http://127.0.0.1:8000';
// axios.defaults.baseURL = 'http://47.105.194.208:9010';
axios.defaults.timeout = 60000;
axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';

export function get(url, params) {
  return new Promise((resolve, reject) => {
    axios.get(url, {
      params: params
    }).then(res => {
      resolve(res.data);
    }).catch(err => {
      reject(err.data)
    })
  });
}

/**
 * post方法，对应post请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
export function post(url, params) {
  return new Promise((resolve, reject) => {
    axios.post(url, QS.stringify(params))
      .then(res => {
        resolve(res.data);
      })
      .catch(err => {
        reject(err.data)
      })
  });
}
