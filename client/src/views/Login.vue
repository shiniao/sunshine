<template>
    <a-row>
        <a-col :xs="1" :sm="3" :md="6" :lg="7" :xl="8"></a-col>
        <a-col :xs="22" :sm="18" :md="12" :lg="10" :xl="8">
            <div class="todo-image">
                <img alt="Vue logo" src="../assets/todo.png">
                <h3>小土豆</h3>
            </div>
            <p>明日复明日，明日何其多。——《明日歌》</p>

            <a-form id="components-form-demo-normal-login" :form="form" class="login-form" @submit="handleSubmit">
                <a-form-item>
                    <a-input
                            v-decorator="['username',{ rules: [{ required: true, message: 'Please input your username!' }] },]"
                            placeholder="Username"
                            v-model="username">
                        <a-icon slot="prefix" type="user" style="color: rgba(0,0,0,.25)"/>
                    </a-input>
                </a-form-item>
                <a-form-item>
                    <a-input
                            v-decorator="[
          'password',
          { rules: [{ required: true, message: 'Please input your Password!' }] },
        ]"
                            type="password"
                            placeholder="Password"
                            v-model="password"
                    >
                        <a-icon slot="prefix" type="lock" style="color: rgba(0,0,0,.25)"/>
                    </a-input>
                </a-form-item>
                <a-form-item>
                    <a-checkbox
                            v-decorator="['remember',
            {
            valuePropName: 'checked',
            initialValue: true,
          },
        ]"
                    >
                        Remember me
                    </a-checkbox>
                    <a class="login-form-forgot" href="">
                        Forgot password
                    </a>
                    <a-button type="primary" html-type="submit" class="login-form-button" @click="login">
                        Log in
                    </a-button>
                </a-form-item>
            </a-form>
        </a-col>
        <a-col :xs="1" :sm="3" :md="6" :lg="7" :xl="8"></a-col>
    </a-row>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "login",
        data() {
            return {
                username: '',
                password: ''
            }
        },
        components: {},
        beforeCreate() {
            this.form = this.$form.createForm(this, {name: 'normal_login'});
        },
        methods: {
            handleSubmit(e) {
                let forms = null;
                e.preventDefault();
                this.form.validateFields((err, values) => {
                    if (!err) {
                        forms = values;
                        console.log('Received values of form: ', values);
                    }
                });
            },

            login() {

                axios.post('/api/token/', {
                    username: this.username,
                    password: this.password
                })
                    .then((res) => {
                        console.info(res)
                        // * 存储token
                        localStorage.setItem('token', res.data.token);
                        console.info("login successful");
                        // * 跳转回登录前页面
                        this.$router.push({
                            path: this.$route.query.redirect || '/',
                            query: {username: this.username}
                        })
                        // console.info(this.$route.query.redirect )

                    }).catch((error) => {
                    console.error(error)
                });
            }
        },
    }
</script>


<style scoped lang="less">
    #components-form-demo-normal-login {
        .login-form {
            max-width: 300px;
        }

        .login-form-forgot {
            float: right;
        }

        .login-form-button {
            width: 100%;
        }
    }

    .todo-image {
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
