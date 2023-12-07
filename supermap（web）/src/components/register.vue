<template>
	<div class="register">
		<img src="../assets/logo/register.png" style="width: 60px;margin-top: 20px;" />
		<el-form :inline="true" label-width="80px" class="form">
			<el-form-item label="用户名">
				<el-input prefix-icon="User" v-model="registInfo.usenames" placeholder="请输入用户名" />
			</el-form-item>
			<el-form-item label="年龄">
				<el-input type="" prefix-icon="Timer" v-model="registInfo.age" placeholder="请输入年龄" />
			</el-form-item>
			<el-form-item label="性别">
				<el-select v-model="registInfo.value" placeholder="请选择性别">
					<template #prefix>
						<span>
							<el-icon><Pointer /></el-icon>
						</span>
					</template>					
					<el-option value="男"><el-icon><Male /></el-icon>男</el-option>
					<el-option value="女"><el-icon><Female /></el-icon>女</el-option>
				</el-select>
			</el-form-item>
			<el-form-item label="密码">
				<el-input type="password" prefix-icon="Lock" v-model="registInfo.passwords" placeholder="请输入密码" show-password/>
			</el-form-item>
			<el-form-item label="再次密码">
				<el-input type="password" prefix-icon="Lock" v-model="registInfo.passwordss" @keydown.enter="register" placeholder="请再次输入密码" show-password/>
			</el-form-item>
			<el-form-item style="margin-top: 20px;">
				<el-button type="primary" round @click="register">确定</el-button>
				<el-button type="primary" round style="margin-left: 170px;" @click="cancel">取消</el-button>
			</el-form-item>
		</el-form>
		<router-link to="" @click="gologin">去登录</router-link>
	</div>
</template>

<script>
	import {
		ElMessage
	} from 'element-plus';
	import querystring from "querystring"
	document.cookie = "ioiopipoadiasdasdbasdbas"
	export default {
		name: 'register',
		data() {
			return {
				//注册信息
				registInfo:{
					usenames: "",
					age: "",
					value: "",
					passwords: "",
					passwordss: "",
				},
				//注册框的显隐性
				registervisiable: false,
			}
		},
		components: {

		},
		methods: {
			//取消注册
			cancel() {
				this.$emit("recancel", this.registervisiable)
			},
			//跳转登录
			gologin() {
				this.$emit('golo')
			},
			//提交注册
			register() {
				if (this.registInfo.usenames === '' || this.registInfo.passwords === '' || this.registInfo.passwordss === '') {
					ElMessage("请输入完整信息")
				} else if (this.registInfo.passwords != this.registInfo.passwordss) {
					ElMessage("请输入相同密码")
				} else {
					this.$axios.post(this.$store.state.Url+':8000/user/register/', JSON.stringify({
						username: this.registInfo.usenames,
						password: this.registInfo.passwords,
						user_xb: this.registInfo.value,
						user_age: this.registInfo.age
					})).then(res => {
						if (res.data.state==2001) {
							ElMessage("注册成功！" + "您的用户名是" + this.registInfo.usenames + ',密码是' + this.registInfo.passwords);
						} else if(res.data.info.substr(1,4)==1062){
							ElMessage("【"+this.registInfo.usenames+"】,该用户名已存在")			
						}else {
							ElMessage("注册失败，请稍后重试");
							console.log("注册失败,您的问题是:" + res.data.info);
						}
					}).catch(err => {
						console.log(err)
					})

				}
			}
		}
	}
</script>

<style scoped>
	.register {
		width: 500px;
		height: 420px;
		margin: 0 auto;
		margin-top: -70px;
		text-align: center;
		/* 		background-color: rgba(85, 255, 255, 0.8);
		border-radius: 10px; */

	}

	.form {
		margin-top: 30px;
		margin-bottom: 10px;
	}

	.el-input {
		width: 350px;
		/* background-color: transparent; */
	}
	.el-select{
		width: 350px;
	}
</style>