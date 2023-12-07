<template>
		<el-container>
			<el-header class="homeheader">
				<el-row :gutter="20">
					<el-col :span="2"><img src='../assets/logo/logo.png' class="logo" alt="系统管理" /></el-col>
					<el-col :span="20"><img src="../assets/logo/logo4.png"></el-col>
					<el-col :span="2">
						<el-dropdown>
							<span style="display: flex;align-items: center;vertical-align: middle;;"><el-icon size="25"><User /></el-icon>游客</span>
							<template #dropdown>
								<el-dropdown-menu>
									<el-dropdown-item @click="loginvisiable=true">登陆</el-dropdown-item>
									<el-dropdown-item @click="registervisiable=true">注册</el-dropdown-item>
									<el-dropdown-item @click="aboutvisiable=true">关于</el-dropdown-item>
								</el-dropdown-menu>
							</template>
						</el-dropdown>
					</el-col>
				</el-row>
			</el-header>
			<el-container >
				<el-header class="mainheader" >
					<homemain></homemain>
				</el-header>
				<el-container class="zhuti" >
					<el-header style="height: 400px; padding-left: 0;padding-right: 0;">	
					   <carousel></carousel>
					</el-header>
					<el-main>
						<router-view name="homemain"></router-view>
					</el-main>
				</el-container>
			</el-container>
			<el-footer>
				<mfoot></mfoot>
			</el-footer>
		</el-container>
		<el-dialog title="登陆" v-model="loginvisiable" style="width: 600px;height: 400px;border-radius: 15px;background: linear-gradient(220.55deg, #DDE4FF 0%, #8DA2EE 100%);" draggable>
			<login @locancel="getlocancel" @gore="onre"></login>
		</el-dialog>
		<el-dialog title="注册" v-model="registervisiable" style="width: 600px;height: 500px;border-radius: 15px;background: linear-gradient(220.55deg, #DDE4FF 0%, #8DA2EE 100%);" draggable>
			<register @recancel="getrecancel" @golo="onlo"></register>
		</el-dialog>
		<el-dialog title="关于" v-model="aboutvisiable" width="900px" draggable>
			<h2>系统介绍</h2>
			<p>
				本旅游资源服务系统是一个全面性的在线旅游服务平台，旨在为游者和旅游业者提供便捷、高效、全面的服务。
				该系统提供了丰富的旅游资源和服务，使游者能够轻松地获取旅游地信息、进行攻略查询、游玩体验分享与查询等。
			</p>
			<p>
				该系统的主要功能包括景点定位、景点信息查询、行政区旅行社查询、路径分析、旅游攻略分享与查询、天气查询、人流量实时监控等。
				游者可以通过该系统浏览各地的旅游景点信息，了解景点的特色和历史背景，还可以根据自己的喜好和需求规划旅游路线。
				此外，游者还可以分享自己的旅游攻略和经验，与其他游者交流互动，提高旅游的趣味性和参与度。
			</p>
			<p>
				对于旅游业者而言，该系统提供了一个高效的推广平台。他们可以在该系统上发布自己的旅游产品和服务，
				包括旅游线路、酒店住宿、交通接送、导游服务等，
				将自己的旅游产品推荐给更多的目标客户，提升市场曝光度和销售量。
			</p>
			<p>
				该系统还提供了一些其他的功能和服务，如评价和反馈等。
				评价和反馈可以让游者和旅游业者对旅游产品和服务进行评价和反馈，帮助其他游者更好地选择旅游产品和服务。
			</p>
			<p>
				总之，本系统是一个为游者和旅游业者提供便捷、高效、全面服务的在线平台。
				它将帮助游者更好地了解和规划旅游行程，同时也为旅游业者提供了一个更广阔的市场空间，促进了旅游业的健康发展。
				该系统的丰富功能和服务，将为游者和旅游业者提供更全面、优质、高效的旅游服务和支持。
			</p>
			<p>欢迎大家使用！有不足之处欢迎大家批评指正！</p>
		</el-dialog>
</template>
<script>
	import carousel from '../components/home/carousel.vue'
	import homemain from '../components/home/home-main.vue'
	import mfoot from '../components/footer.vue'
	import login from '../components/login.vue'
	import register from '../components/register.vue'

	export default {
		name: 'home',
		data() {
			return {
				loginvisiable: false,//登录框的显隐性
				registervisiable: false,//注册框的显隐性
				aboutvisiable: false//关于框的显隐性
			}
		},
		components: {
			homemain,
			mfoot,
			login,
			register,
			carousel,
		},
		methods: {
			//取消登录
			getlocancel(data) {
				this.loginvisiable = data
			},
			//取消注册
			getrecancel(data) {
				this.registervisiable = data
			},
			//用来控制注册框的显隐性
			onre(data) {
				this.registervisiable = !this.registervisiable
				this.loginvisiable = !this.loginvisiable
			},
			//用来控制登录框的显隐性
			onlo(data) {
				this.registervisiable = !this.registervisiable
				this.loginvisiable = !this.loginvisiable
			},
		}
	};
</script>
<style scoped>
	.homeheader {
		height: 100px;
	}

	.el-row {
		text-align: center;
		align-items: center;
		vertical-align: middle;

	}

	.mainheader {
		height: 65px;
		background:linear-gradient(to right,#30cfd0 0%,#330867 100%);
	}
	.el-aside {
		width: 200px;
		height: 700px;
		padding: 0;
	}
	.zhuti{
		background: linear-gradient(  to right, #C5EDF5 0%, #4A879A 100%);	/* 220.55deg */	
		box-shadow: 0 5px 20px 0 rgba(0, 0, 12, 0.3);
	}

	.el-main {
		height: auto;
		min-height: 700px;
		/* color: white; */
		background: url("../assets/background/Earth - Phone.png") ;
		/* height: 700px; */
		/* border: 2px solid pink; */
		/* box-shadow: 0 2px 12px 0 rgba(0, 0, 12, 0.3); ; */
		/* background-color: #ece7d7; */
	}

	.el-footer {
		text-align: center;
		height: 100px;
	}

	h2 {
		text-align: center;
	}

	p {
		text-indent: 2em;
		font-family: Zhuo !important;
		line-height: 30px;
	}
</style>