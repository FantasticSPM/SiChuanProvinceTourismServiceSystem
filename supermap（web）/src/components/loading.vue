<template>
	<!-- 加载组件 -->
	<div class="contea">
		<div class="title">正在加载中</div>	
		<div class="conters"></div>
	</div>
</template>

<script>
	export default{
		name:'Loading'
	}
</script>

<style scoped>
	.title{
		width: 400px;
		margin: 0 auto;
		margin-top: 200px;
		font-size: 20px;
		font-family: OPPO;
		text-align: center;
	
	}
	.contea{
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 100vh;
		background-color:#f0f9ff; 
		animation: changeback 1s linear infinite;
	}
	.conters{
		position: absolute;
		width: 150px;
		height: 150px;
		background:linear-gradient( to top,#f0f9ff 40%,#51eeee);
		border-radius: 50%;
		animation: xuh 1s linear infinite;
	}
	.conters:before{
		content: '';
		position: absolute;
		width: 130px;
		height: 130px;
		bottom: 0;
		background:#f0f9ff;
		border-radius: 50%;
		
	}
	.conters::after{
		content: '';
		position: absolute;
		width: 40px;
		height: 40px;
		border-radius: 50%;
		top: 50px;
		right: -8px;
		background: #51eeee;
		box-shadow: 0 0 5px #51eeee,0 0 25px;
	}
	@keyframes xuh {
		to{
			transform: rotate(360deg);
		}
	}
  
</style>

