<template>
    <div class="home">
        <div class="login">
            <div style="flex: 1; text-align: right">欢迎{{user}}
                <a-icon type="logout" @click="logout"/>
            </div>
        </div>
        <a-row>
            <a-col :xs="1" :sm="3" :md="6" :lg="7" :xl="8"></a-col>
            <a-col :xs="22" :sm="18" :md="12" :lg="10" :xl="8">
                <div class="todo-image">
                    <img alt="Vue logo" src="../assets/todo.png">
                    <h3>小土豆</h3>
                </div>
                <p>明日复明日，明日何其多。——《明日歌》</p>


                <!--添加todo-->
                <a-input v-focus placeholder="添加一条todo" v-model="title" @pressEnter="addTodo"/>

                <div class="choiceTodo">
                    <div>
                        <a-date-picker size="small" type="primary" style="width: 110px; margin-right: 12px"
                                       placeholder="截止时间"
                                       :format="time_now_f"
                                       @change="choiceTimeChange"/>
                    </div>
                    <div>
                        <a-select defaultValue="优先级" size="small" @change="priorityChange">
                            <a-icon slot="suffixIcon" type="flag"/>
                            <a-select-option value="1">I</a-select-option>
                            <a-select-option value="2">II</a-select-option>
                            <a-select-option value="3">III</a-select-option>
                        </a-select>
                    </div>
                </div>


                <div class="main">
                    <div class="sort">
                        <a-dropdown placement="bottomRight">
                            <a-menu slot="overlay">
                                <a-menu-item key="2" @click="sortFunc('p')">
                                    <a-icon type="flag"/>
                                    优先级
                                </a-menu-item>
                                <a-menu-item key="3" @click="sortFunc('e')">
                                    <a-icon type="schedule"/>
                                    截止时间
                                </a-menu-item>
                            </a-menu>
                            <a-button style="margin-left: 8px"> 排序
                                <a-icon type="down"/>
                            </a-button>
                        </a-dropdown>
                    </div>

                </div>

                <div v-for="todo in todos">

                    <todo :title="todo.title"
                          :id="todo.id"
                          :finished="todo.finished"
                          :priority="todo.priority"
                          :expired="todo.expired"></todo>


                </div>
                <a-pagination :current="current" :total="total"
                              :defaultPageSize="5"
                              @change="pageSizeChange"/>
                <div style="text-align: left">已完成TODO</div>
                <div v-for="todo in todosf">
                    <todo :title="todo.title"
                          :id="todo.id"
                          :finished="todo.finished"
                          :priority="todo.priority"
                          :expired="todo.expired"></todo>

                </div>
            </a-col>
            <a-col :xs="1" :sm="3" :md="6" :lg="7" :xl="8"></a-col>
        </a-row>

    </div>
</template>

<script>
    // @ is an alias to /src
    import todo from '@/components/Todo.vue'
    import axios from 'axios'
    import moment from "moment";

    export default {
        name: 'home',
        components: {
            todo
        },
        data() {
            return {
                title: "",
                total: 0,
                finished_total: 0,
                current: 1,
                todos: "",
                todosf: "",
                visible: false,
                time_now_f: "YYYY-MM-DD",
                // 截止时间
                expired_time: null,
                // 优先级
                priority: 4,
                // 排序方式
                sort: 'd',
                user: this.$route.query.username
            }
        },
        inject: ['reload'],
        methods: {
            moment,
            // 登出
            logout() {
                localStorage.removeItem("token");
                // * 跳转回登录页面
                this.$router.push({name: 'login'});

            },
            sortFunc(sort) {
                this.sort = sort;
                let mysort = "";
                if (this.sort === 'p') {
                    mysort = "优先级"
                } else if (this.sort === "e") {
                    mysort = "截止时间"
                }

                this.getPageTodo(sort, this.current);
                this.$notify({
                    group: 'foo',
                    type: 'success',
                    text: '按' + mysort + '排序'
                });
            },
            choiceTimeChange(date, dateString) {
                this.expired_time = dateString;
                console.log("截止时间: ", this.expired_time);

            },

            priorityChange(value) {
                this.priority = value;
                console.info("优先级： ", this.priority)
            },

            pageSizeChange(page) {
                this.current = page;
                this.getPageTodo(this.sort, page);
                console.info("page:", page)
            },

            getAllTodo() {
                axios.get('/api/api/v1/todos/d/')
                    .then((res) => {
                        this.todos = res.data.results;
                        this.total = res.data.count;
                        console.info("todo总量: ", this.total);
                    }).catch((error) => {
                    console.error(error)
                });
            },

            getAllFinishedTodo() {
                axios.get('/api/api/v1/todos/f/')
                    .then((res) => {
                        this.todosf = res.data.results;
                        this.finished_total = res.data.count;
                        console.info("finished todo总量: ", this.finished_total);
                    }).catch((error) => {
                    console.error(error)
                });
            },

            getPageTodo(sort, page) {
                this.todos = "";
                axios.get('/api/api/v1/todos/' + sort + '/?page=' + page)
                    .then((res) => {
                        this.todos = res.data.results;
                    }).catch((error) => {
                    console.error(error)
                });
            },

            addTodo() {

                axios.post('/api/api/v1/todos/a/', {
                    'title': this.title,
                    'priority': this.priority,
                    'expired': this.expired_time
                })
                    .then((res) => {
                        console.info(res);
                        this.reload();
                        this.$notify({
                            group: 'foo',
                            type: 'success',
                            text: '添加成功'
                        });
                    }).catch((error) => {
                    console.error(error)
                });
            },

        },
        mounted() {
            this.getAllTodo();
            this.getAllFinishedTodo();
            console.info("finished: ", this.total - this.finished_total);
        },

    };

</script>

<style lang="less" scoped>
    .main {
        display: flex;
        align-items: center;
        padding: 6px 0 0 0;

        .sort {
            /*width: 48px;*/
            flex: 1;
            text-align: right;
        }
    }

    .login {
        display: flex;
        align-items: center;
        margin: 0 24px 0 0;

    }

    .choiceTodo {
        display: flex;
        align-items: flex-start;
        justify-content: right;
        margin: 8px 0;
    }

    .todo-image {
        display: flex;
        align-items: center;
        justify-content: center;
    }


</style>
