"""
微信公众号和商户平台信息配置文件
"""

# ----------------------------------------------微信公众号---------------------------------------------- #
# 公众号appid
APPID = 'wx6e7157cd6dfbb4ec'
# 公众号AppSecret
APPSECRET = 'f62dcf502f8379c94323e774e877c714'

# ----------------------------------------------微信商户平台---------------------------------------------- #
# 商户id
MCH_ID = '1591387851'

API_KEY = 'api秘钥'
# 微信下单url
ufdoder_url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

# 微信支付结果回调接口，改为服务器上处理结果的回调方法路径
NOTIFY_URL = "https://www.ezaifit.top:80/notify/"
SIGN_KEY = "LfbrUlO9SwQOqNYhje9Xh71i0IK4eKjn"
UNIFIED_ORDER_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
ORDER_QUERY_URL = 'https://api.mch.weixin.qq.com/pay/orderquery'

# 微信会员到期提醒
notice_template_id = "-bUzUActf9mtviSiE3FHSfWSOPgWF9Sk9Ji3bMcq5ZY"
notice_url = "https://www.ezaifit.top/User"
# 你的服务器ip
create_ip = ""

# ----------------------------------------------回调页面---------------------------------------------- #
# 用户授权获取code后的回调页面，如果需要实现验证登录就必须填写
REDIRECT_URI = 'http://www.show.netcome.net/index'
PC_LOGIN_REDIRECT_URI = 'http://www.show.netcome.net/index'

defaults = {
    # 微信内置浏览器获取code微信接口
    'wechat_browser_code': 'https://open.weixin.qq.com/connect/oauth2/authorize',
    # 微信内置浏览器获取access_token微信接口
    'app_access_token': 'https://api.weixin.qq.com/cgi-bin/token',
    'wechat_browser_access_token': 'https://api.weixin.qq.com/sns/oauth2/access_token',
    # 微信内置浏览器获取用户信息微信接口
    'app_user_info': 'https://api.weixin.qq.com/cgi-bin/user/info',
    'wechat_browser_user_info': 'https://api.weixin.qq.com/sns/userinfo',
    # pc获取登录二维码接口
    'pc_QR_code': 'https://open.weixin.qq.com/connect/qrconnect',

    # 微信通知用戶
    'notice_user_url': 'https://api.weixin.qq.com/cgi-bin/message/template/send',
    # pc获取登录二维码接口
    # 'pc_QR_code': 'https://api.weixin.qq.com/sns/userinfo',
}

SCOPE = 'snsapi_userinfo'
PC_LOGIN_SCOPE = 'snsapi_login'
STATE = ''
LANG = 'zh_CN'
