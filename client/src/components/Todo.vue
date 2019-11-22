<template>
    <div class="todo" :class="{finished: finished}" :style="{color: priorityColor}">
        <a-radio @click="FinishTodo" :class="{finished_p: finished}"></a-radio>
        <!--        todos内容-->
        <div class="todo-title">
            <span @dblclick="edit=true" v-if="edit===false">{{ title }}</span>
            <div v-if="edit === true">

                <a-input
                        v-model="title"
                        @blur="updateVal"
                        @keyup.enter="updateVal"
                />


                <a-button style="margin: 8px 12px 0 0" size="small" @click="UpdateTodo">保存</a-button>
                <a-button size="small" @click="edit=false">取消</a-button>

            </div>

            <div v-if="expired_time">
                <a-date-picker
                        :format="time_now_f"
                        @change="choiceTimeChange">
                    <span class="expired"
                          :class="{finished: finished, outer_expired: is_expired}">{{expired_time}}</span>
                </a-date-picker>
            </div>

        </div>

        <!--        编辑删除按钮-->
        <div style="flex: 1; text-align: right;">

            <a-icon :class="{finished_p: finished}" style="margin: 0 12px 0 0" type="edit" theme="twoTone"
                    :disabled="disabled"
                    @click="edit=true"/>
            <a-icon type="delete" theme="twoTone" :disabled="disabled" @click="deleteTodo"/>

            <!--            优先级和时间-->
            <a-dropdown :class="{finished_p: finished}" placement="bottomCenter">
                <a class="ant-dropdown-link" href="#">
                    <a-icon style="margin: 0 0 0 12px" :disabled="disabled" type="smile"/>
                </a>
                <a-menu slot="overlay">
                    <a-menu-item>
                        <a @click="changePriority(1)" style="color: #ff3d38">I 优先级</a>
                    </a-menu-item>
                    <a-menu-item>
                        <a @click="changePriority(2)" style="color: #ffaa1a">II 优先级</a>
                    </a-menu-item>
                    <a-menu-item>
                        <a @click="changePriority(3)" style="color: #ffaa1a">III 优先级</a>
                    </a-menu-item>
                    <a-menu-divider/>
                    <a-menu-item>
                        <a-date-picker
                                :format="time_now_f"
                                @change="choiceTimeChange">
                            <span class="expired">{{expired_time?expired_time:"截止时间"}}</span>
                        </a-date-picker>
                    </a-menu-item>
                </a-menu>
            </a-dropdown>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import moment from 'moment'

    export default {
        name: "todo",
        props: ['id', 'title', 'finished', 'priority', 'expired'],
        inject: ['reload'],
        data() {
            return {
                edit: false,
                priorityColor: '#000',
                disabled: false,
                expired_time: this.expired,
                is_expired: false,
                time_now_f: "YYYY-MM-DD",
            }
        },
        methods: {
            choiceTimeChange(date, dateString) {
                this.is_expired = false;
                this.expired_time = dateString;
                this.UpdateExpiredTodo();
                // 判断截止时间是否过期
                if (moment(this.expired_time).isBefore()) {
                    this.is_expired = true
                }
                console.log("截止时间: ", this.expired_time);

            },
            updateVal() {
                this.edit = false;
                this.UpdateTodo();
            },

            changePriority(priority) {
                if (priority === 1) {
                    this.UpdatePriorityTodo(priority);
                    this.priorityColor = '#ff3d38'
                } else if (priority === 2) {
                    this.UpdatePriorityTodo(priority);
                    this.priorityColor = '#ffaa1a'
                } else if (priority === 3) {
                    this.UpdatePriorityTodo(priority);
                    this.priorityColor = '#49a9ff'
                } else {
                    this.priorityColor = '#000'
                }
            },

            deleteTodo() {
                axios.delete('/api/api/v1/todos/a/' + this.id + '/')
                    .then((res) => {
                        this.reload();
                        this.$notify({
                            group: 'foo',
                            type: 'info',
                            text: '删除成功'
                        });
                    }).catch((error) => {
                    console.error(error)
                });
            },

            UpdateTodo() {
                let todos = new FormData();
                todos.append('title', this.title);
                axios.put('/api/api/v1/todos/a/' + this.id + '/', todos)
                    .then((res) => {
                        this.$notify({
                            group: 'foo',
                            type: 'info',
                            text: '更新成功！'
                        });
                    }).catch((error) => {
                    console.error(error)
                });
            },

            UpdatePriorityTodo(priority) {
                let todos = new FormData();
                todos.append('title', this.title);
                todos.append('priority', priority);
                axios.put('/api/api/v1/todos/a/' + this.id + '/', todos)
                    .then((res) => {
                        this.$notify({
                            group: 'foo',
                            type: 'info',
                            text: '优先级变为' + priority
                        });
                    }).catch((error) => {
                    console.error(error)
                });
            },

            UpdateExpiredTodo() {
                let todos = new FormData();
                todos.append('title', this.title);
                todos.append('expired', this.expired_time);
                axios.put('/api/api/v1/todos/a/' + this.id + '/', todos)
                    .then((res) => {
                        this.$notify({
                            group: 'foo',
                            type: 'info',
                            text: '截止时间' + this.expired_time
                        });
                    }).catch((error) => {
                    console.error(error)
                });
            },

            FinishTodo() {
                let todos = new FormData();
                todos.append('title', this.title);
                todos.append("finished", true);
                todos.append('priority', 4);
                this.priorityColor = '#000';
                //TODO: 按钮不可点击
                this.disabled = true;
                axios.put('/api/api/v1/todos/a/' + this.id + '/', todos)
                    .then((res) => {
                        this.reload();
                        this.$notify({
                            group: 'foo',
                            type: 'info',
                            text: '好棒耶！完成任务啦！'
                        });
                    }).catch((error) => {
                    console.error(error)
                });
            },
        },
        mounted() {
            if (this.priority === 1) {
                this.priorityColor = '#ff3d38'
            } else if (this.priority === 2) {
                this.priorityColor = '#ffaa1a'
            } else if (this.priority === 3) {
                this.priorityColor = '#49a9ff'
            } else {
                this.priorityColor = '#000'
            }

            // 判断截止时间是否过期
            if (moment(this.expired_time).isBefore()) {
                this.is_expired = true
            }
        }

    }
</script>

<style scoped lang="less">
    .todo {
        margin: 8px auto;
        padding: 12px 8px;
        text-align: left;
        -moz-box-shadow: 0px 0px 2px #847070;
        -webkit-box-shadow: 0px 0px 2px #847070;
        box-shadow: 0px 0px 2px #847070;
        border-radius: 4px;
        display: flex;
        align-items: center;
    }

    .finished {
        text-decoration: line-through;
        background: #eeeeee;
        color: #4f4f4f;
    }

    .finished_p {
        pointer-events: none;
    }

    .expired {
        font-size: 8px;
        color: #aaaaaa;
    }

    .outer_expired {
        font-size: 8px;
        color: #ff3d38;
    }
</style>