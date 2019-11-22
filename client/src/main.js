import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css'
import axios from 'axios'
import Notifications from 'vue-notification'

Vue.config.productionTip = false

Vue.use(Antd)
Vue.use(Notifications)

new Vue({
    router,
    render: h => h(App)
}).$mount('#app')

// * http request 拦截器
axios.interceptors.request.use(
    config => {
        // * 判断是否存在token，如果存在的话，则每个http header都加上token
        if (localStorage.token) {
            config.headers["Authorization"] = `Bearer ${localStorage.token}`;
        }
        return config;
    },
    err => {
        return Promise.reject(err);
    });

// * http response 拦截器
// todo: 错误处理
axios.interceptors.response.use(
    response => {
        return response
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 403:
                    // 跳转到登录界面
                    router.replace({
                        path: '/login',
                        query: {redirect: router.currentRoute.fullPath}
                    });
            }
        }
        return Promise.reject(error.response.data);
    });

Vue.prototype.$http = axios;
// * 公共汽车
Vue.prototype.bus = new Vue();

// * v-focus
Vue.directive('focus',{
    inserted(el){
        el.focus()
    }
})
