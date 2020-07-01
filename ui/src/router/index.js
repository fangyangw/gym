import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import AboutClass from '@/views/AboutClass'
import BuyingCards from '@/views/BuyingCards'
import User from '@/views/User'
import DetailsCard from '@/views/CardDetails'
import DetailsClass from '@/views/ClassDetails'
import OrderDetails from '@/views/OrderDetails'
import ClassOrder from '@/views/ClassOrder'
import UserRecommend from '@/views/UserRecommend'
import UserPhone from '@/views/UserPhone'
import UserUploadPhoto from '@/views/UserUploadPhoto'
import UserRegister from '@/views/UserRegister'
import CheckUserRecommend from '@/views/CheckUserRecommend'
import YiBiRecord from '@/views/YiBiRecord'
import MyClass from '@/views/MyClass'
import MyCard from '@/views/MyCard'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [{
      path: "/",
      redirect: "/AboutClass",
      component: AboutClass
    },
    {
      path: '/AboutClass',
      name: 'AboutClass',
      component: AboutClass
    },
    {
      path: '/BuyingCards',
      name: 'BuyingCards',
      component: BuyingCards
    },
    {
      path: '/User',
      name: 'User',
      component: User
    },
    {
      path: '/DetailsCard',
      name: 'DetailsCard',
      component: DetailsCard
    },
    {
      path: '/DetailsClass',
      name: 'DetailsClass',
      component: DetailsClass
    },
    {
      path: '/OrderDetails',
      name: 'OrderDetails',
      component: OrderDetails
    },
    {
      path: '/ClassOrder',
      name: 'ClassOrder',
      component: ClassOrder
    },
    {
      path: '/User/UserRecommend',
      name: 'UserRecommend',
      component: UserRecommend
    },
    {
      path: '/User/Phone',
      name: 'UserPhone',
      component: UserPhone
    },
    {
      path: '/User/UploadPhoto',
      name: 'UserUploadPhoto',
      component: UserUploadPhoto
    },
    {
      path: '/User/Register',
      name: 'UserRegister',
      component: UserRegister
    },
    {
      path: '/CheckUserRecommend',
      name: 'CheckUserRecommend',
      component: CheckUserRecommend
    },
    {
      path: '/YiBiRecord',
      name: 'YiBiRecord',
      component: YiBiRecord
    },
    {
      path: '/MyClass',
      name: 'MyClass',
      component: MyClass
    },
    {
      path: '/MyCard',
      name: 'MyCard',
      component: MyCard
    }
  ]
})
export default router
