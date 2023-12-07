import {
	createRouter,
	createWebHashHistory
} from 'vue-router';
import {
	ElMessage
} from 'element-plus'
// import home from '../views/home.vue'

const routes = [{
		path: '/',
		name: 'home',
		redirect: '/index',
		components: {
			out: () => import('../views/home.vue')
		},
		children: [
			{
				path: 'index',
				name: 'homeIndex',
				components: {
					homemain: () => import('@/components/home/index/index.vue')
				}
			},
			{
				path: 'summarize',
				name: 'summarize',
				components: {
					homemain: () => import('@/components/home/summarize/summarize.vue')
				}
			},
			{
				path: 'resource',
				name: 'resource',
				components: {
					homemain: () => import('@/components/home/resource/resource.vue')
				}
			},
			{
				path: 'trip',
				name: 'trip',
				components: {
					homemain: () => import('@/components/home/trip/trip.vue')
				}
			}
		]
	},
	{
		path: '/zhuye',
		name: 'zhuye',
		redirect: '/zhuye/index',
		meta: {
			isAuth: true
		},
		components: {
			out: () => import('../views/zhuye.vue')
		},
		children: [{
				path: 'index',
				name: 'zhuyeIndex',
				components: {
					main: () => import('@/components/zhuye/map.vue')
				}
			},
			{
				path: 'weatherInformation',
				name: 'weatherInformation',
				components: {
					main: () => import('@/components/zhuye/resource/weatherInformation.vue')
				}
			},
			{
				path: 'interestInformation',
				name: 'interestInformation',
				components: {
					main: () => import('@/components/zhuye/resource/interestInformation.vue')
				}
			},
			{
				path: 'man-time',
				name: 'man-time',
				components: {
					main: () => import('@/components/zhuye/monitoring/man-time.vue')
				}
			},
			{
				path: 'jiuzhaigou',
				name: 'jiuzhaigou',
				components: {
					main: () => import('@/components/zhuye/monitoring/jiuzhaigou.vue')
				}
			},
			{
				path: 'usershare',
				name: 'usershare',
				redirect: '/zhuye/usershare/hot',
				components: {
					main: () => import('@/components/zhuye/Interaction/usershare.vue')
				},
				children: [{
						path: 'hot',
						name: 'hot',
						components: {
							share: () => import('@/components/zhuye/Interaction/usershare/hot.vue')
						},
					},
					{
						path: 'mine',
						name: 'mine',
						components: {
							share: () => import('@/components/zhuye/Interaction/usershare/mine.vue')
						}
					},
				]
			},
			{
				path: 'feedback',
				name: 'feedback',
				components: {
					main: () => import('@/components/zhuye/Interaction/feedback.vue')
				}
			}
		],
	},
	{
		path: '/information',
		name: 'information',
		meta:{
			isAuth:true
		},
		components: {
			out: () => import('@/components/zhuye/details/information.vue')
		}
	},
]

const router = createRouter({
	history: createWebHashHistory(process.env.BASE_URL),
	routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
	if (to.meta.isAuth) { // 判断该路由是否需要登录权限
	    if(Date.now()<localStorage.getItem('time')){//判断localStorage中的time是否过期
			next()	//没过期放行
		}else{//localStorage过期
			ElMessage("抱歉，身份信息已过期，请重新登陆！")
			localStorage.removeItem('userName');
			localStorage.removeItem('time');
			next("/")
		}
		
	}else{
		next()
	}
});

export default router