import { get, post } from '@/utils/https'
// import axios from 'axios';

export const get_user_info = p => get('/user_info/', p);

export const get_card = p => get('/card/', p);

export const get_user_info_details = p => get('/member/', p);

export const order_pay = p => post('/order/', p);

export const send_verification = p => post('/phone/send_verification/', p);

export const save_phone = p => post('/phone/save/', p);

export const get_app_sign = p => post('/app/sign/', p);


export const update_member_info = p => post('/member/', p);

export const get_user_image = p => get('/user/image/', p);

export const get_course = p => get('/course/detail/', p);

export const get_my_course = p => get('/user/course/', p);

export const get_my_card = p => get('/user/card/', p);

export const get_yibi_order = p => get('/yibi/order/', p);

export const yibi_order_pay = p => post('/yibi/buy/', p);
