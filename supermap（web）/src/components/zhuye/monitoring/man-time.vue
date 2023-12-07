<template>
	<div class="Body">
		<div style="text-align: center;font-size: 40px;height: 100px;line-height: 100px;">四川省统计数据</div>
		<hr>
		<div style="height: 500px;">
			<div id="man-time" style="width: 700px;height: 400px;float: left;"></div>
			<div id="pay" style="width: 700px;height: 400px;float: left;"></div>
		</div>
		<div style="width: 850px; height: 400px;margin: 0 auto;">
			<div id="industry" style="width: 400px;height: 300px;float: left;"></div>
			<div id="tourism" style="width: 400px;height: 300px;float: left;"></div>
		</div>
	</div>

</template>

<script>
	import * as echarts from "echarts";
	export default{
		name:'man-time',
		methods:{
			manTime(){
				let chartDom1 = document.getElementById('man-time');
				let myChart1 = echarts.init(chartDom1);
				let option1;
				option1 = {
					title: {
						text: "2022年四川省各市州旅游人次",
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
						formatter: '{a} <br/>{b} : {c}万'
					},
					xAxis: {
						type: 'category',
						axisLabel:{
							show:true,
							interval:0,
							rotate:40
						},
						data: ['成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市','遂宁市','内江市','乐山市','南充市','眉山市','宜宾市','广安市','达州市','雅安市','巴中市','资阳市','阿坝州','甘孜州','凉山州']
					},
					yAxis: {
						type: 'value'
					},
					series: [{
							name: '旅游人次',
							type: 'line',
							// stack: 'Total',
							data:[20531.94,547.34,3014.78,5547.3,875,7415.6,5189.5,5831.5,6198.5,7308,6380,4293,7905.79,3000,2222.5,3284.88,3279.8,3629,4058.7,3500,4356.5],
						    markLine: {
						    	symbol:'none',
						        data: [
						    		{ 
						    			type: 'average', 
						    		    name: '平均' ,
						    		},
						    		]
						    },
						    markPoint: {
						        data: [
						            { type: 'max', name: '峰值' },
						            { type: 'min', name: '低谷' },
						        ]
						    },
						}
					]			
				};
				option1 && myChart1.setOption(option1);
			},
			
			pay(){
				let chartDom = document.getElementById('pay');
				let myChart = echarts.init(chartDom);
				let option;
				option = {
				  title: {
				    text: '入境外国人在四川逐年日均旅游花费',
				    subtext: '2008-2019',
				    left: 'center'
				  },
				    xAxis: {
				      type: 'category',
				      data: ['2008', '2009', '2010', '2011', '2012', '2013', '2014','2015','2016','2017','2018','2019']
				    },
				    yAxis: {
				      type: 'value'
				    },
					tooltip: {
						// trigger: 'axis',
						backgroundColor: "rgb(196, 255, 249)",
						// formatter: '{a} <br/>{b} : {c}万'
					},
					  series: [
					    {
						  name: '日均',
					      data: [173.390, 175.630, 175.450, 176.690, 176.630, 185.150, 185.590,192.940,193.320,202.080,193.818,195.310],
					      type: 'bar',
					      showBackground: true,
					      backgroundStyle: {
					        color: 'rgba(180, 180, 180, 0.2)'
					      },
						  itemStyle:{
							  normal:{
								  color:function(params){
									  let colorList=['#00A3E0','#FFA100','#ffc0cb','#CCCCCC','#BBFFAA','#749f83','#ca8622','#dfdb20','#adbe25','#ceb2ad','#DDcca2','BA25d5c']
									  return colorList[params.dataIndex]
								  }
							  }
						  }
					    }
					  ]
				};
				option && myChart.setOption(option);
			},
			industry(){
				let chartDom = document.getElementById('industry');
				let myChart = echarts.init(chartDom);
				let option;
				option = {
				  title: {
				    text: '四川省2022年一、二、三产业收入',
				    // subtext: '2008-2019',
				    left: 'center'
				  },
				  tooltip: {
				    trigger: 'item'
				  },
				  legend: {
				    orient: 'horizonal',
				    x: 'right',
					y:"bottom"
				  },
				  series: [
				    {
				      name: '产业占比',
				      type: 'pie',
					  radius:'60%',
				      itemStyle: {
				        borderRadius: 8
				      },
				      data: [
				        { value: 5958.729, name: '第一产业' },
				        { value: 21167.6754, name: '第二产业' },
				        { value: 29623.3956, name: '第三产业' },
				      ],
				      emphasis: {
				        itemStyle: {
				          shadowBlur: 10,
				          shadowOffsetX: 0,
				          shadowColor: 'rgba(0, 0, 0, 0.5)'
				        }
				      }
				    }
				  ]
				};
				option && myChart.setOption(option);
			},
			tourism(){
				let chartDom = document.getElementById('tourism');
				let myChart = echarts.init(chartDom);
				let option;
				option = {
				  title: {
				    text: '四川省2022年旅游与其他收入',
				    // subtext: '2008-2019',
				    left: 'center'
				  },
				  tooltip: {
				    trigger: 'item'
				  },
				  legend: {
				    orient: 'vertical',
				    x: 'right',
					y:"bottom"
				  },
				  series: [
				    {
				      name: '收入',
				      type: 'pie',
					  radius:'60%',
				      itemStyle: {
				        borderRadius: 8
				      },
				      data: [
				        { value: 3700, name: '旅游收入' },
				        { value: 7900, name: '其他收入' }
				      ],
				      emphasis: {
				        itemStyle: {
				          shadowBlur: 10,
				          shadowOffsetX: 0,
				          shadowColor: 'rgba(0, 0, 0, 0.5)'
				        }
				      }
				    }
				  ]
				};
				option && myChart.setOption(option);
			},
			
		},
		mounted() {
			this.manTime();
			this.pay();
			this.industry();
			this.tourism()
		}
	}
</script>

<style scoped>
	.Body{
		background:linear-gradient(220.55deg, #72EDF2 0%, #A7BFE8 100%) ;
	}
</style>