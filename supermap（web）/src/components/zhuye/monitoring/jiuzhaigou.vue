<template>
	<el-container v-if="dataChecked!=''" class="monitorBody">
		<el-header style="height: 200px; text-align: center;">
			<p style="font-size: 40px;font-family: OPPO;">九寨沟旅游流量监控</p>
			<div><span class="NUM">购票人数：{{dataChecked.购票人数}} </span><span class="NUM"
					style="margin-left: 30px;margin-right: 30px;">已入园：{{dataChecked.已入园}}
				</span><span class="NUM">待入园：{{dataChecked.待入园}} </span></div>

		</el-header>
		<el-container>
			<el-aside style="width: 900px;">
				<div id="Summary" class="item" style=" width: 700px;height: 350px;margin: 0 auto;">
				</div>
				<div id="Location" class="item" style=" width: 700px;height: 400px;margin: 0 auto;margin-top: 20px;">
				</div>
			</el-aside>
			<el-main style="padding-top: 0;">
				<div style="width: 450px;height: 250px;" class="item">
					<div>
						<table>
							<th>票型</th>
							<th>售票人数</th>
							<th>检票人数</th>
							<tr>
								<td>全价套票</td>
								<td>{{sell.全价套票}}</td>
								<td>{{ticketsChecked.全价套票}}</td>
							</tr>
							<tr>
								<td>感恩赠票</td>
								<td>{{sell.感恩赠票}}</td>
								<td>{{ticketsChecked.感恩赠票}}</td>
							</tr>
							<tr>
								<td>学生优惠套票</td>
								<td>{{sell.学生优惠套票}}</td>
								<td>{{ticketsChecked.学生优惠套票}}</td>
							</tr>
							<tr>
								<td>儿童免票</td>
								<td>{{sell.儿童免票}}</td>
								<td>{{ticketsChecked.儿童免票}}</td>
							</tr>
							<tr>
								<td>感恩补充票赠票</td>
								<td>{{sell.感恩补充票赠票}}</td>
								<td>{{ticketsChecked.感恩补充票赠票}}</td>
							</tr>
							<!-- <tr><td>（60岁以上老人）免门票套票</td><td>{{sell.60岁以上老人）免门票套票}}</td></tr> -->
							<tr>
								<td>军人免门票套票</td>
								<td>{{sell.军人免门票套票}}</td>
								<td>{{ticketsChecked.军人免门票套票}}</td>
							</tr>
							<tr>
								<td>残疾人免门票套票</td>
								<td>{{sell.残疾人免门票套票}}</td>
								<td>{{ticketsChecked.残疾人免门票套票}}</td>
							</tr>
							<tr>
								<td>阿坝人活动门票</td>
								<td>{{sell.阿坝人活动门票}}</td>
								<td>{{ticketsChecked.阿坝人活动门票}}</td>
							</tr>
							<!-- <tr><td>（60岁以上）老人免门票</td><td>{{sell.（60岁以上）老人免门票}}</td></tr> -->
						</table>
					</div>
				</div>
				<div class="item" id="Age" style="width: 450px;height: 250px;"></div>
				<div class="item" id="Tourist" style="width: 450px;height: 250px;"></div>
			</el-main>
		</el-container>
	</el-container>
	<Loading v-else="dataChecked!=''"></Loading>
</template>

<script>
	import * as echarts from 'echarts';
	import Loading from '@/components/loading.vue'
	export default {
		name: 'jiuzhaigou',
		components: {
			Loading
		},
		data() {
			return {
				sell: [],
				ticketsChecked: [],
				dataChecked: [],
				showCard: false,
				visible: true,
				percentage: 0
			}
		},
		methods: {
			demo() {
				this.$axios.all([
					this.$axios.get(this.$store.state.Url + ':8000/strategy/liuliang/').then(res => res.data),
					this.$axios.get(this.$store.state.Url + ':8000/strategy/monitor/').then(res => res.data)
				]).then(
					this.$axios.spread((val1, val2) => {
						this.dataChecked = val2.检票数据
						this.sell = val2.售票人数
						this.ticketsChecked = val2.检票人数
						this.$nextTick(() => {
							this.total(val1)
							this.locationChart(val2.今日客源地前十)
							this.Chart(val2.各年龄)
							this.Chart(val2.游客类型)
						})
					})
				)
			},
			total(item) {
				let Date = []
				let Num = []
				for (let i in item) {
					Date.push(i);
					// res.data[i]=parseInt(res.data[i])
					Num.push(item[i]);
				}
				Date = Date.slice(0, 15)
				Date.reverse();
				Num = Num.slice(0, 15)
				Num.reverse();
				let chartDom = document.getElementById('Summary');
				let myChart = echarts.init(chartDom);
				let option
				option = {
					title: {
						text: "九寨沟单日接待游客人数",
						subtext: '（数据来源于九寨沟官网,每日实时更新）',
						x: 'center',
						y: 'top',
						textAlign: 'left',
						textStyle: {
							fontSize: 20
						}
					},
					tooltip: {
						trigger: 'axis',
						backgroundColor: "rgb(196, 255, 249)",
						// formatter: '{a} <br/>{b} : {c}'
					},
					xAxis: {
						type: 'category',
						axisLabel: {
							show: true,
							interval: 0,
							// formatter:function(value){
							// 	return value.split('').join('\n')
							// },
							rotate: 40
						},
						data: Date
					},
					yAxis: {
						type: 'value'
					},
					series: [{
						name: '旅游人次',
						type: 'line',
						// stack: 'Total',
						data: Num,
						markLine: {
							symbol: 'none',
							data: [{
								type: 'average',
								name: '平均',
							}, ]
						},
						markPoint: {
							data: [{
									type: 'max',
									name: '峰值'
								},
								{
									type: 'min',
									name: '低谷'
								},
							]
						},
					}]
				};
				option && myChart.setOption(option);
			},
			locationChart(item) {
				let topProvince = []
				let topPeople = []
				for (let i in item) {
					topProvince.push(i);
					// res.data[i]=parseInt(res.data[i])
					topPeople.push(parseFloat(item[i]));
				}
				let chartDom = document.getElementById('Location');
				let myChart = echarts.init(chartDom);
				let option;
				option = {
					color: ['#00A3E0', '#FFA100', '#ffc0cb', '#CCCCCC', '#BBFFAA', '#749f83', '#ca8622', '#dfdb20',
						'#adbe25', '#ceb2ad'
					],
					title: {
						text: "今日客源地前十",
						x: 'center',
						y: 'top',
						textStyle: {
							fontSize: 20
						}
					},
					tooltip: {
						trigger: 'axis',
						backgroundColor: "rgb(196, 255, 249)",
						// formatter: '{a} <br/>{b} : {c}'
					},
					xAxis: {
						type: 'category',
						data: topProvince
					},
					yAxis: {
						type: 'value'
					},
					series: [{
						data: topPeople,
						type: 'bar',
						markLine: {
							symbol: 'none',
							data: [{
								type: 'average',
								name: '平均',
							}, ]
						},
						showBackground: true,
						backgroundStyle: {
							color: 'rgba(180, 180, 180, 0.2)'
						},
						itemStyle: {
								color: function(params) {
									let colorList = ['#00A3E0', '#FFA100', '#ffc0cb', '#CCCCCC', '#BBFFAA',
										'#749f83', '#ca8622', '#dfdb20', '#adbe25', '#ceb2ad'
									]
									return colorList[params.dataIndex]
								}
						}
					}]
				};
				option && myChart.setOption(option);
			},

			Chart(item) {
				let j = []
				for (let i in item) {
					let m = {}
					m.value = parseFloat(item[i].substr(0, item[i].length - 1))
					m.name = i
					j.push(m)
				}
				let ID, Text
				if (item.hasOwnProperty('0-6岁')) {
					ID = 'Age'
					Text = '各年龄分布'
				} else {
					ID = 'Tourist'
					Text = '今日团散比'
				}
				let chartDom = document.getElementById(ID);
				let myChart = echarts.init(chartDom);
				let option;
				option = {
					title: {
						text: Text,
						left: 'center'
					},
					tooltip: {
						trigger: 'item'
					},
					legend: {
						orient: 'vertical',
						left: 'left'
					},
					series: [{
						type: 'pie',
						radius: ['30%', '60%'],
						center: ['60%', '60%'],
						data: j,
						emphasis: {
							itemStyle: {
								shadowBlur: 10,
								shadowOffsetX: 0,
								shadowColor: 'rgba(0, 0, 0, 0.5)'
							}
						}
					}]
				};
				option && myChart.setOption(option);
			}

		},
		beforeMount() {
			// let m=setInterval(this.demo,10000)
		},
		created() {
			// this.demo

		},
		mounted() {
			this.demo()
		},

	}
</script>

<style scoped>
	table {
		width: 400px;
	}

	th {
		text-align: center;
	}

	td {
		text-align: center;
	}
	.monitorBody{
		background: url('@/assets/background/monitor.png') 0 0 no-repeat, #f0f9ff;
	}

	.item {
		border-radius: 20px;
		background-color: #e9f1fc;
		box-shadow: 5px 5px 10px #5bcccb;
		margin-bottom: 10px;
	}

	.NUM {
		font-size: 25px;
	}
</style>