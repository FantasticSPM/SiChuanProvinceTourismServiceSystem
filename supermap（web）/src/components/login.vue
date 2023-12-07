<template>
	<div class="login">
		<el-progress :percentage=percentage :indeterminate="true" v-show="isdisable"> <el-button
				text>{{title}}</el-button></el-progress>
		<img src="../assets/logo/loginfont.png" style="width: 60px;margin-top: 20px;" />
		<el-form :inline="true" label-width="60px" class="form">
			<el-form-item label="用户名">
				<el-input prefix-icon="User" v-model="loginInfo.usename" placeholder="请输入用户名" required />
			</el-form-item>
			<el-form-item label="密码">
				<el-input prefix-icon="Lock" v-model="loginInfo.password" @keydown.enter="sure" placeholder="请输入密码"
				 show-password required />
			</el-form-item>
			<el-form-item style="margin-top: 20px;">
				<el-button type="primary" round @click="sure">确定</el-button>
				<el-button type="primary" round style="margin-left: 170px;" @click="cancel">取消</el-button>
			</el-form-item>
		</el-form>
		<router-link to="" @click="goregister">注册账号</router-link>|
		<router-link to="" @click="tip">修改密码</router-link>
	</div>
</template>

<script>
	import {
		ElMessage
	} from 'element-plus'

	export default {
		name: 'login',
		components: {

		},
		data() {
			return {
				//账户密码
				loginInfo: {
					usename: "",
					password: "",
				},
				loginvisiable: false,//登陆框显隐性
				percentage: 0,//进度条
				isdisable: false,//进度条显隐性
				title: "",//加载信息
				}
		},
		methods: {
			sure() {
				if (this.loginInfo.usename == "" || this.loginInfo.password == "") {//确保用户名和密码不为空
					ElMessage("请输入完整信息")
				} else {
					//登录请求
					this.$axios.post(this.$store.state.Url+':8000/user/login/', JSON.stringify({
						username: this.loginInfo.usename,
						password: this.loginInfo.password
					}), {//加载进程
						onDownloadProgress: (progressEvent) => {
							let progressBar = Math.round(progressEvent.loaded / progressEvent.total * 100)
							if (progressBar == 100) {
								this.percentage = progressBar;
								this.title = "加载完成!"
							} else {
								this.percentage = progressBar;
								this.isdisable = true
								this.title = "正在加载,请耐心等待!"
							}
						}
					}).then(res => {
						// console.log(res.data.info)
						if(this.percentage==100){
							if (res.data.state == 2002) {
								let loginData = res.data.responseFromeDatabase
								const time = Date.now() + 60 * 60 *
								1000; //向localStorage中添加一个time，用于判断登陆信息是否过期,设置的为60min
								localStorage.setItem('Info', JSON.stringify({//向浏览器本地仓库存储个人信息
									usename: loginData.username,
									password: "qhixns8xgcb8dcbj8hcb5",//设置假密码
									age: loginData.age,
									sex: loginData.sex,
									registTime: loginData.date_joined,

								}))
								localStorage.setItem('time', time)
								this.$router.push('/zhuye')//登录跳转
								let appellation = loginData.sex == '男' ? '先生' : '女士'
								ElMessage("亲爱的【" + this.loginInfo.usename + "】" + appellation + "!您好，欢迎您进入本系统！")
							} else if (res.data.state == 1111) {
								ElMessage("用户名或密码错误");
								//用户名或密码错误时清空输入框
								this.loginInfo.usename = "";
								this.loginInfo.password = ""
							}
						}

					})
				}

			},
			cancel() {//取消登录
				this.$emit("locancel", this.loginvisiable)
			},
			goregister() {//跳转注册页面
				this.$emit("gore")
			},
			tip() {
				ElMessage('请先登录再修改密码！！！')
			}
		},

	}
</script>


<style scoped>
	.login {
		width: 550px;
		height: 300px;
		margin: 0 auto;
		text-align: center;
		margin-top: -30px;
	}

	.form {
		margin-top: 30px;
		margin-bottom: 20px;
	}

	.el-input {
		width: 350px;
		background-color: transparent;
	}
</style>