<template>
	<div>
	<el-menu mode="horizontal" text-color="black"  active-text-color="#000000" style="background:transparent" router>
		<el-menu-item index="/index">首页</el-menu-item>
		<el-menu-item index="/summarize">四川文旅概况</el-menu-item>
		<el-menu-item index="/resource">四川省旅游资源</el-menu-item>
		<el-menu-item index="/trip">四川省旅游景点推荐</el-menu-item>		
	</el-menu>
	</div>
</template>

<script>
	export default{
		name:"home-main",
		
	}
</script>

<style scoped>
	.el-menu{
		width: 950px;
		margin: 0 auto;
	}
	.el-menu-item{
		width: 220px;
		margin: 0 auto; 
		/* border: 3px solid #e6e6e6; */
		font-size: 22px;
		color: white;
		font-family: Biao !important;	
		/* background-color: black; */
	}
</style>