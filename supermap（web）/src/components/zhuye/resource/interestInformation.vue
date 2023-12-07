<template>
	<el-container>
		<el-header class="strategyHeader">
			<div>景点攻略查询</div>
			<el-input v-model="interestSearch" style="width: 100%;" placeholder="四川景点等你来探索!" @keydown.enter="Search()">
				<template #append>
					<el-button @click="Search()">
						<el-icon><Search /></el-icon>
					</el-button>
				</template>
			</el-input>
		</el-header>
		<el-container class="interestBody" v-for="(item,index) in interestInformation" :key="index" >
			<el-header style="height: 200px;">
				<p style="white-space: pre-wrap;font-size: 30px;text-align: center;">{{item.fields.pname}}</p>
				<p style="white-space: pre-wrap;text-align: center;">{{item.fields.level}}</p>
				<p style="white-space: pre-wrap;text-align: center;font-style: italic;">{{item.fields.location}}</p>
				<hr>
			</el-header>
			<el-container>
				<el-aside style="width: 520px;">
					<el-image
						style="width: 500px;height: 560px;margin-left: 10px;"
						fit="cover"
						:src="fileurl+item.fields.img_url[0]" 
						:preview-src-list="item.fields.img_url.map(v=>{
							return fileurl+v
						})">
					</el-image>
				<!-- 				</span>	 -->
				<!-- 				<el-carousel style="position: absolute;width: 500px;margin: auto;height: 300px;"
								:height="'100%'"
								:indicator-position="item.fields.img_url.length<=1?'none':''" 
								:arrow="item.fields.img_url.length<=1?'never':'always'">
								  <el-carousel-item v-for="(i,index) in item.fields.img_url" :key="index">
								    <el-image
								      style="width: 100%;height: 100%;"
								      :src="fileurl+i" 
								      :preview-src-list="[fileurl+i]">
								    </el-image>
								  </el-carousel-item>
								</el-carousel> -->
				</el-aside>							
				<el-main style="box-shadow: 2px 2px 8px 0 rgba(0, 0, 12, 0.3);white-space: pre-wrap;">
					{{item.fields.content}}
				</el-main>
			</el-container>
		</el-container>
		<el-empty description="当前无景点攻略,请输入景点查询" v-show="interestInformation==''"></el-empty>
	</el-container>	
</template>

<script>
	export default{
		name:"interestInformation",
		data(){
			return{
				interestSearch:"",
				interestInformation:"",
				fileurl:this.$store.state.Url+':8000/static/image/',//后端存放照片的路径
	
			}
		},
		mounted() {			

			
		},
		methods:{
			Search(){
				if (this.interestSearch==""){
					return
				}else{
					let fs=new FormData()
					fs.append("keywords",this.interestSearch)
					this.$axios.post(this.$store.state.Url+":8000/strategy/index/",fs,{Headers:{'Content-Type':'multipart/form-data'}})
					.then(res=>{
						this.interestInformation=res.data.data
						console.log(res.data.data.map(item=>item))
					})
				}
			}
		}
	}
</script>

<style scoped>
     .strategyHeader{
		font-family: You;
		font-size: 40px;
	    background: url('@/assets/background/strategy.png');
		height: 110px;
		text-align: center;
		/* box-shadow: 0 2px 8px 0 rgba(0, 0, 12, 0.3); */
     }
	 .el-empty{		
		 height: 590px;
		 background:linear-gradient(to right ,#d9d8fb 0%,#18b3bf);
	 }
	 .interestBody{
		/* border: 2px solid #e6e6e6; */
		/* border-radius: 20px; */
		box-shadow: 2px 2px 8px 0 rgba(0, 0, 12, 0.3); 
		background:linear-gradient(to right ,#d9d8fb 0%,#18b3bf);
	 }

</style>