<template>
	<el-container>
		<el-header class="weatheryHeader">
			<div>天气状况查询</div>
			<el-input v-model="cityname" style="width: 100%;" placeholder="晴带雨伞,饱带饥粮,不要忘记关注天气哟!"
				@keydown.enter="weatherSearch()">
				<template #append>
					<el-button @click="weatherSearch()">
						<el-icon>
							<Search />
						</el-icon>
					</el-button>
				</template>
			</el-input>
		</el-header>
		<el-main class="weatherBody">
			<!-- :style="{'background':result.situation=='晴朗'?'url('+require('@/assets/background/sunny.png')+')':'url('+require('@/assets/background/cloudy.png')+')'}" -->
				<div v-for="(item,index) in todayWeatherCondition" :key="index" class="WeatherItem">
					<div class="todayWeatherItem" style="height: 300px;">
						<div :id="'humidity'+index" style="width: 310px;height: 300px;float: left;"></div>
						<div style="float: left;width: 630px;height: 100%;background-repeat: no-repeat;background-size: cover;color: white;"
							:style="{'background':item.weather=='晴' ?'url('+require('@/assets/gif/qing.gif')+')'
							:item.weather.indexOf('云')!=-1 ?'url('+require('@/assets/gif/yun.gif')+')'
							:item.weather.indexOf('风')!=-1 ?'url('+require('@/assets/gif/feng.gif')+')'
							:item.weather.indexOf('雨')!=-1 &&item.weather.indexOf('雪')==-1?'url('+require('@/assets/gif/yu.gif')+')'
							:item.weather.indexOf('霾')!=-1 ?'url('+require('@/assets/gif/wumai.gif')+')'
							:item.weather.indexOf('雪')!=-1 ?'url('+require('@/assets/gif/xue.gif')+')'
							:item.weather.indexOf('阴')!=-1 ?'url('+require('@/assets/gif/yin.gif')+')'
							:''}">
							<span style="font-size: 30px;">{{item.province}}{{item.city}}今日天气</span>
							<span style="font-style: italic;">数据更新于{{item.reporttime}}</span>
							<div style="margin-top: 20px;">
								<span style="font-size: 50px;">{{item.temperature_float}}℃</span>
								<span>{{item.weather}}</span>
							</div>
							<div>{{item.winddirection}}{{item.windpower}}级</div>
							<div>空气湿度{{item.humidity_float}}%</div>
						</div>
						<div :id="'temperature'+index" style="width: 400px;height: 300px;float: right;"></div>
					</div>
					<div class="forecastWeatherItem">
						<div style="font-size: 25px;text-align: center;">{{forecastWeatherCondition[index].city}}未来几天天气状况</div>
						<el-table :data="forecastWeatherCondition[index].casts" style="width: 1300px;margin: 0 auto;">
							<el-table-column prop="date" label="日期" width="150" align="center" />
							<el-table-column prop="week" label="星期" align="center" />
							<el-table-column prop="dayweather" label="白天天气" align="center" />
							<el-table-column prop="nightweather" label="晚上天气" align="center" />
							<el-table-column prop="daytemp" label="白天温度" align="center" />
							<el-table-column prop="nighttemp" label="晚上温度" align="center" />
							<el-table-column prop="daywind" label="白天风向" align="center" />
							<el-table-column prop="nightwind" label="晚上风向" align="center" />
							<el-table-column prop="daypower" label="白天风力" align="center" />
							<el-table-column prop="nightpower" label="晚上风力" align="center" />
						</el-table>
						<div :id="'forecast'+index" style="width: 600px;height: 350px;margin: 0 auto;"></div>
					</div>
				</div>					
			<el-empty description="当前无天气状况,请输入城市名查询" v-show="forecastWeatherCondition==''" />
		</el-main>
	</el-container>
</template>

<script>
	import {
		ElMessage
	} from 'element-plus';
	import * as echarts from "echarts";
	export default {
		name: "weatherInformation",
		data() {
			return {
				cityname: "",
				todayWeatherCondition: "",
				forecastWeatherCondition: '',
			}
		},
		methods: {
			weatherSearch() {
				if (this.cityname == "") {
					return
				}
				let todayUrl =
					`https://restapi.amap.com/v3/weather/weatherInfo?city=${this.cityname}&extensions=base&key=abc5e5e5bdc3b7a3aadaf16a56957602`;
				let forecastUrl =
					`https://restapi.amap.com/v3/weather/weatherInfo?city=${this.cityname}&extensions=all&key=abc5e5e5bdc3b7a3aadaf16a56957602`;
                //并发请求，避免数据产生时差
				this.$axios.all([
					this.$axios.get(todayUrl).then(res => res.data),
					this.$axios.get(forecastUrl).then(res => res.data)
				]).then(
					this.$axios.spread((val1, val2) => {
						if (val1.lives[0] != '' && val1.lives[0] != undefined) {
							let num=val1.lives.length//结果个数
							ElMessage("查询成功，为您找到【"+num+"】条结果！")
							this.todayWeatherCondition = val1.lives
							this.forecastWeatherCondition = val2.forecasts
							for (let item in val1.lives) {
								//确保DOM已挂载
								this.$nextTick(() => {
									let Temperature = 'temperature' + item//动态ID
									let Humidity = 'humidity' + item//动态ID
									let Forecast = 'forecast' + item//动态ID
									let chartDom1 = document.getElementById(Temperature);//今日温度
									let chartDom2 = document.getElementById(Humidity);//今日湿度
									let chartDom3 = document.getElementById(Forecast);//未来几天温度
									let myChart1 = echarts.init(chartDom1);
									let myChart2 = echarts.init(chartDom2);
									let myChart3 = echarts.init(chartDom3);
									let option1, option2,option3;
									let WeatherDate = val2.forecasts[item].casts.map(i => {
										return i.date
									}); //遍历未来几天日期，放在一个数组里面
									let WeatherDaytemp = val2.forecasts[item].casts.map(i => {
										return i.daytemp_float
									}) //未来几天白天温度
									let WeatherNighttemp = val2.forecasts[item].casts.map(i => {
										return i.nighttemp_float
									}) //未来几天晚上温度
									option1 = {
										tooltip: {
											trigger: 'item',
										},
										series: [{
												type: 'gauge',
												center: ['50%', '60%'],
												startAngle: 200,
												endAngle: -20,
												min: 0,
												max: 45,
												splitNumber: 9,
												itemStyle: {
													color: '#FFAB91'
												},
												progress: {
													show: true,
													width: 20
												},
												pointer: {
													show: false
												},
												axisLine: {
													lineStyle: {
														width: 20
													}
												},
												axisTick: {
													distance: -45,
													splitNumber: 5,
													lineStyle: {
														width: 2,
														color: '#999'
													}
												},
												splitLine: {
													distance: -52,
													length: 14,
													lineStyle: {
														width: 3,
														color: '#999'
													}
												},
												axisLabel: {
													distance: -20,
													color: '#999',
													fontSize: 20
												},
												anchor: {
													show: false
												},
												title: {
													show: false
												},
												detail: {
													valueAnimation: true,
													width: '60%',
													lineHeight: 40,
													borderRadius: 8,
													offsetCenter: [0, '-15%'],
													fontSize: 40,
													fontWeight: 'bolder',
													formatter: '{value} °C',
													color: 'inherit'
												},
												data: [{
													value: val1.lives[item].temperature
												}]
											},
											{
												type: 'gauge',
												center: ['50%', '60%'],
												startAngle: 200,
												endAngle: -20,
												min: 0,
												max: 60,
												itemStyle: {
													color: '#FD7347'
												},
												progress: {
													show: true,
													width: 8
												},
												pointer: {
													show: false
												},
												axisLine: {
													show: false
												},
												axisTick: {
													show: false
												},
												splitLine: {
													show: false
												},
												axisLabel: {
													show: false
												},
												detail: {
													show: false
												},
												// data: [{
												// 	value: 20
												// }]
											}
										]
									};
									option2 = {
										tooltip: {
											formatter: '{a} <br/>{b} : {c}%'
										},
										series: [{
											name: '空气湿度',
											type: 'gauge',
											progress: {
												show: true
											},
											detail: {
												valueAnimation: true,
												formatter: '{value}%'
											},
											data: [{
												value: val1.lives[item].humidity,
											}]
										}]
									};
									option3 = {
										title: {
											text: val2.forecasts[item].city + "未来几天温度",
											x: 'left',
											y: 'top',
											textAlign: 'left',
											textStyle: {
												fontSize: 13
											}
										},
										tooltip: {
											backgroundColor: "rgb(196, 255, 249)",
											formatter: '{a} <br/>{b} : {c}°C'
										},
										legend: {
											data: ['白天温度', '晚上温度']
										},
										xAxis: {
											type: 'category',
											data: WeatherDate
										},
										yAxis: {
											type: 'value',
											axisLabel: {
												formatter: '{value} °C'
											}
										},
										series: [{
												name: '晚上温度',
												type: 'line',
												data: WeatherNighttemp,
												markLine: {
													symbol: 'none',
													data: [{
														type: 'average',
														name: '夜间平均气温'
													}]
												}
											},
											{
												name: '白天温度',
												type: 'line',
												// stack: 'Total',
												data: WeatherDaytemp,
												lineStyle:{
													color:'#0d9adb'
												},
												itemStyle:{
													normal:{
														color:'#0d9adb'
													},
												},
												markLine: {
													symbol: 'none',
													lineStyle:{
														color:'#0d9adb'
													},
													data: [{
														type: 'average',
														name: '白天平均气温'
													}]
												}
											}
										]
									};
									option1 && myChart1.setOption(option1);
									option2 && myChart2.setOption(option2);									
									option3 && myChart3.setOption(option3);
								})
							}
						} else {
							ElMessage('请输入准确的城市名！')
						}
					}))
			},
		}
	}
</script>

<style scoped>
	.weatheryHeader {
		font-family: You;
		font-size: 40px;
		height: 110px;
		text-align: center;
		/* border: 2px solid #e6e6e6; */
		/* box-shadow: 0 2px 8px 0 rgba(0, 0, 12, 0.3); */
		background: url('@/assets/background/weather.png');
		color: white;
	}

	.weatherBody {
		/* height: 590px; */
		text-align: center;
		/* border: 2px solid #e6e6e6; */
		box-shadow: 0 2px 8px 0 rgba(0, 0, 12, 0.3);
		background: linear-gradient(to right, #d9d8fb 0%, #18b3bf);
	}
	
	.WeatherItem{
		margin-bottom: 20px;
	}

	.todayWeatherItem {
		box-shadow: 0 2px 12px 0 rgba(0, 0, 12, 0.3);
		border-radius: 3px;
	}

	.forecastWeatherItem {
		margin-top: 5px;
		box-shadow: 0 2px 12px 0 rgba(0, 0, 12, 0.3);
		border-radius: 3px;
	}

	.el-empty {
		height: 590px;
	}

	:deep() .el-table,
	:deep() .el-table__expanded-cell {
		background-color: transparent;
	}

	:deep() .el-table th,
	:deep() .el-table tr,
	:deep() .el-table td {
		background-color: transparent;
	}
</style>