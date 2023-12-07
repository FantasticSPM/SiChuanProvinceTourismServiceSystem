<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <el-row :gutter="20">
                    <el-col :span="2">
                        <img src="../assets/logo/logo.png" class="logo" alt="系统管理" />
                    </el-col>
                    <el-col :span="20" class="biaoti">
                        <img src="../assets/logo/logo4.png" alt="" />
                    </el-col>
                    <el-col :span="2">
                        <el-dropdown>
                            <span style="display: flex;justify-content: center;align-items: center;"><el-icon size="25"><avatar></avatar></el-icon>{{Info.usename==""?"游客":Info.usename}}</span>
                            <template #dropdown>
                                <el-dropdown-menu>
                                    <el-dropdown-item @click="information">个人信息</el-dropdown-item>
                                    <el-dropdown-item divided @click="exit">退出登录</el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                    </el-col>
                </el-row>
				<!--  backgroundColor="#545c64" -->
            </el-header>
            <el-container>
			   <el-header class="menuOption">
                   <el-menu mode="horizontal" router text-color="black"  active-text-color="#94cfeb" style="background:transparent;"  >
					   <el-menu-item index="/zhuye/index" class="menuTitle"><el-icon><House /></el-icon>首页</el-menu-item>					   
					   <el-sub-menu index="1" class="menuTitle">
					       <template #title >                               
					           <span ><el-icon><search></search></el-icon>旅游资源信息管理</span>
					       </template>
					       <el-menu-item index="/zhuye/interestInformation"><el-icon><Reading /></el-icon>景点信息</el-menu-item>
					       <el-menu-item index="/zhuye/weatherInformation"><el-icon><Sunrise /></el-icon>天气状况</el-menu-item>
					   </el-sub-menu>
					   <el-sub-menu index="2" class="menuTitle">
					   		 <template #title >
					   			 <span><el-icon><chat-round></chat-round></el-icon>互动区</span>
					   		</template>
					   		 <el-menu-item index="/zhuye/usershare"><el-icon><ChatLineSquare /></el-icon>旅游体验分享</el-menu-item>
					   		 <el-menu-item index="/zhuye/feedback"><el-icon><warn-triangle-filled></warn-triangle-filled></el-icon>系统反馈</el-menu-item>
					   </el-sub-menu>
					   <el-sub-menu index="3" class="menuTitle">
					       <template #title>                               
					           <span><el-icon><View /></el-icon>人流量监控</span>
					       </template>
					       <el-menu-item index="/zhuye/man-time"><el-icon><Position /></el-icon>四川省旅游数据统计</el-menu-item>
					       <el-menu-item index="/zhuye/jiuzhaigou"><el-icon><Aim /></el-icon>九寨沟每日旅游人次实时监控</el-menu-item>
					   </el-sub-menu>
					   <!-- <el-sub-menu index="4">
					       <template #title>                                
					           <span><el-icon><tickets></tickets></el-icon>分析</span>
					       </template>
					       <el-menu-item index="4-1">二级菜单</el-menu-item>
					       <el-menu-item index="4-2">二级菜单</el-menu-item>
					   </el-sub-menu>
					   <el-sub-menu index="5">
					       <template #title>                               
					           <span><el-icon><more-filled></more-filled></el-icon>拓展</span>
					       </template>
					       <el-menu-item index="5-1">二级菜单</el-menu-item>
					       <el-menu-item index="5-2">二级菜单</el-menu-item>
					   </el-sub-menu> -->
				   </el-menu>
			   </el-header>
                <el-main>					
                    <router-view name="main"></router-view>
                </el-main>
            </el-container>
            <el-footer>
                <mfoot></mfoot>
            </el-footer>
        </el-container>
    </div>
</template>

<script>
    import mfoot from '@/components/footer.vue';
    export default {
        name: 'zhuye',
		data() {
			return{
				Info:""
			}
		},
        components: {
            mfoot,
        },
        methods: {
			//跳转到个人信息框
            information() {
                this.$router.push('/information');
            },
           //退出登录
            exit() {
				let m=confirm("您确定退出吗?")
				if(m){
					localStorage.removeItem('Info')
					localStorage.removeItem('time')
					location.reload()
				}
            },
        },
		mounted() {
			//从浏览器本地仓库取出个人信息
			this.Info=JSON.parse(localStorage.getItem('Info'))
		}
    };
</script>

<style scoped>
	.el-row {
		align-items: center;
		vertical-align: middle;
	}

	.el-header {
		/* background-color: aqua; */
		text-align: center;
		height: 100px;
	}

	.logo {
		width: 70px;
	}

	.biaoti {
		font-family: "华文行楷";
		font-size: 80px;
	}

/* 	.el-aside {
		width: 200px;
		height: 700px;
		align-items: center;
		vertical-align: middle;
		background-color: antiquewhite; 
	} */
	.menuTitle{
		width: 250px;
	}
	.el-menu-item {
		font-family: Biao !important;
		font-size: 20px;
	}
	.el-sub-menu span{
		margin: 0 auto;
		font-family: Biao !important;
		font-size: 20px;
	}
	.el-main {
		/* background-color: aquamarine; */
		padding: 0;
		/* border: 4px solid #e6e6e6; */
		border-radius: 3px;
		height: auto;
		min-height: 700px;
		box-shadow: 0 2px 12px 0 rgba(0, 0, 12, 0.3); 
	}
	.menuOption{
		height: 120px;
		border: 1px solid #e6e6e6;
		background: url('@/assets/background/zhuye.png') 0 0 no-repeat, linear-gradient(45deg, #1cbbb4,#0a94e1);;
		box-shadow: 0 2px 12px 0 rgba(0, 0, 12, 0.3)
	}

	.el-footer {
		/* background-color: aliceblue; */
		text-align: center;
		height: 100px;
	}
</style>
