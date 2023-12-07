<template>
	<el-carousel height="400px" :interval="2000" type="card" style="background-color: transparent;">
	  <el-carousel-item >
	     <img src="@/assets/carousel/pandas.jpg" alt="">
	  </el-carousel-item>
	  <el-carousel-item>
	     <img src="@/assets/carousel/hotpot.jpg" alt="">
	  </el-carousel-item>
	  <el-carousel-item >
	     <img src="@/assets/carousel/jiuzhaigou.jpg" alt="">
	  </el-carousel-item>
	  <el-carousel-item >
	     <img src="@/assets/carousel/chuanOpera.jpg" alt="">
	  </el-carousel-item>
	  <el-carousel-item >
	     <img src="@/assets/carousel/pandas1.jpg" alt="">
	  </el-carousel-item>
	  <el-carousel-item >
	     <img src="@/assets/carousel/hotpot1.jpg" alt="">
	  </el-carousel-item>
	  <el-carousel-item >
	     <img src="@/assets/carousel/jiuzhaigou1.jpg" alt="">
	  </el-carousel-item>
	  <el-carousel-item >
	     <img src="@/assets/carousel/chuanOpera1.jpg" alt="">
	  </el-carousel-item>
	</el-carousel>
</template>

<script>
</script>

<style scoped>
	:deep() .el-carousel__indicators{
		left: unset;
		transform: unset;
		right: 2%;
	}
	:deep() .el-carousel__button{
		width: 10px;
		height: 10px;
		border: none;
		border-radius: 50%;
		background-color: rgba(0, 0, 0, 0.2);
	}
	:deep() .is-active .el-carousel__button{
		background: white;
	}
	:deep() .el-carousel__container{
		height: 100%;
	}
	:deep() .el-carousel__arrow{
		background: linear-gradient(to right, #65FDF0 0%, #65FDF0 100%);;
		color: black;
	}
</style>