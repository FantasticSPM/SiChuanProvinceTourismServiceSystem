<template>
	<el-container>
		<el-header>
			<span style="display: flex;align-items:center;;"><img src="@/assets/logo/account.png"/>账户中心</span>
		</el-header>
		<el-container class="informationBody">
			<el-aside>
				<el-menu>
					<el-menu-item >基础信息</el-menu-item>
				</el-menu>
			</el-aside>
			<el-main>
				<div class="Information">
					<el-form  label-width="80px">
						<el-form-item label="用户名" >
							<el-input v-model="Info.usename" prefix-icon="Edit" clearable></el-input>
						</el-form-item>
						<el-form-item label="密码" >
							<el-input type="password" v-model="Info.password" prefix-icon="Edit" clearable></el-input>
						</el-form-item>
						<el-form-item label="性别" >
							<el-select v-model="Info.sex" style="width: 400px !important;">
								<el-option value="男">男</el-option>
								<el-option value="女">女</el-option>
							</el-select>
 						</el-form-item>
						<el-form-item label="年龄">
							<el-input v-model="Info.age" prefix-icon="Edit" clearable></el-input>
						</el-form-item>
						<el-button type="primary" round @click="update">修改</el-button>
					</el-form>
				</div>
			</el-main>
		</el-container>
	</el-container>
</template>

<script>
	import {
		ElMessage
	} from 'element-plus'
	export default{
		name:'information',
		data() {
			return{
				username:"",
				Info:"",
				registDate:"",
				joinDay:"",
				nowDate:null,
				nowtimer:""
			}
		},
		methods:{
			timeTranslate(time){//时间戳转换函数
				let year=time.getFullYear();
				let month=time.getMonth()+1;
				let day=time.getDate();
				return year+"-"+month+"-"+day
			},
			gettime(){
				this.nowDate=new Date().toLocaleString();
			},
			update(){
				if(this.Info.usename===JSON.parse(localStorage.getItem('Info')).usename
				&&this.Info.password===JSON.parse(localStorage.getItem('Info')).password
				&&this.Info.sex===JSON.parse(localStorage.getItem('Info')).sex
				&&this.Info.age===JSON.parse(localStorage.getItem('Info')).age)
				//判断信息是否有变动
				{
					ElMessage("请输入修改信息！")
					return
				}
				this.$axios.post(this.$store.state.Url+':8000/user/update/',JSON.stringify({
					username:this.username,
					information:this.Info
				})).then(res=>{
					//返回值为更新后的信息
					let updataInformation=res.data[0].fields
					//更新本地仓库个人信息
					localStorage.setItem('Info', JSON.stringify({
						usename: updataInformation.username,
						password: "qhixns8xgcb8dcbj8hcb5",
						age: updataInformation.age,
						sex: updataInformation.sex,
					}))
					ElMessage("修改成功！")
					setTimeout(function(){
						location.reload()
					},1000)//延迟一秒刷新页面
					
				})
			}
		},

		mounted() {
			this.username=JSON.parse(localStorage.getItem('Info')).usename;
			this.Info=JSON.parse(localStorage.getItem('Info'));

		}
	}
</script>

<style scoped>
	.el-header{
		display: flex;
		align-items: center;
		border-bottom: 1px solid #e6e6e6;
	}
	.el-aside{
		border-right: 1px solid #e6e6e6;
	}
	.el-menu{
		border: 0 !important;
	}
    .el-input{
		width: 400px;
	}
	:deep() .el-select{
		width: 400px !important;
	}
	.Information{
		width: 500px;
	}
	.informationBody{
		height: 500px;
		background: url('@/assets/background/information.png');
	}
	
</style>