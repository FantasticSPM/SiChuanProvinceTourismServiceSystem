<template>
	<div class="out">
		<div class="fankui">
			<el-input type="textarea" :rows='8' v-model="leaveWord" placeholder="对本系统有任何提议,均可在此写下,我们欢迎广大用户积极反馈" ></el-input>
			<el-button type="primary" style="margin-top: 30px;" @click="submit">提交</el-button>
		</div>		
	</div>
	
</template>

<script>
	import {
		ElMessage
	} from 'element-plus';
	export default{
		name:"feedback",
		data() {
			return{
				leaveWord:""
			}
		},
		methods:{
			submit(){
				ElMessage("感谢您的反馈，祝您使用愉快")
			}
		}
		
	}
</script>

<style scoped>
	.out{
		width: 1190px;
		height: 690px;
		background: url("../../../assets/background/usershare.png");		
	}
	.fankui{
		width: 800px;
		margin: 20px auto;
	}

</style>