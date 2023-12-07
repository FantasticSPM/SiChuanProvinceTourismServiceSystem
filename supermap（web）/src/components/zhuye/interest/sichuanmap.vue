<template>
	<div id="sichuan"></div>
</template>

<script>
	import * as echarts from "echarts";
	import sichuanmap from "@/assets/json/sichuan.json";
	export default {
		name: 'sichuanmap',
		data() {
			return {
			}
		},
		mounted() {
			// console.log(sichuanmap);
			let myChart = echarts.init(document.getElementById("sichuan")); //初始化echarts示例
			echarts.registerMap("四川", sichuanmap); //注册地图数据
			let data = [];
			data = sichuanmap.features.map((item) => {
				return {
					name: item.properties.name,
					fiveAnum: item.properties.fiveAnum,
					fourAnum: item.properties.fourAnum,
					threeAnum: item.properties.threeAnum,
				}
			}) //取出json中所需要的数据
			let option = {
				title: {
					text: "四川省各市州A级旅游景点数",
					x: 'center',
					y: 'top',
					// textAlign:'left',
					textStyle: {
						fontSize: 13
					}
				},
				tooltip: {
					backgroundColor: "rgba(0,0,0,0)",
					trigger: "item",
					formatter: function(item) {
						let tipHtml =
							`<div style="background:#fff;border-radius:10px;padding-top:10px;box-shadow:0 0 10px #666">
					    <div style="text-align:center;color:#494949;padding:8px 6px">
		                     <table border='0' cellspacing='0' cellpadding='0' style="text-align: center;border-spacing: 0 7px;">
							 <caption style="color:#fff;height:20px;border-radius:6px;font-size:12px;line-height:20px;background-color:#5861a2;text-align:center;margin:0 2px;">${ item.data.name}</caption>
		                     <tr style="border:1px soild #5861a2;background-color: #edeff2;">
		                         <th>5A</th>
		                     	 <td>${item.data.fiveAnum}</td>
		                     </tr>
		                     <tr style="border:1px soild #5861a2;">
		                         <th>4A</th>
		                     	 <td>${item.data.fourAnum}</td>
		                     </tr>
		                     <tr style="border:1px soild #5861a2;background-color: #edeff2;">
		                         <th>3A</th>
		                     	 <td>${item.data.threeAnum}</td>
		                     </tr> 
					    </div>
		
				    </div>`;
						return tipHtml;
					},
				},
				series: [{
					name: "四川省各市州A级旅游景点数",
					type: "map",
					map: "四川", // 自定义扩展图表类型
					aspectScale: 1,
					zoom: 1, //缩放
					showLegendSymbol: true,
					// label: {
					//   show: true,
					//   color: "#fff",
					//   fontSize: 5,
					// },
					itemStyle: {
						areaColor: "#0E95F1",
						borderColor: "#e9e9e9",
						borderWidth: 1,
						shadowColor: "#0E95F1",
						shadowBlur: 20,
					},
					emphasis: {
						label: {
							show: true,
							color: "#000000",
							fontSize: 10,
						},
						itemStyle: {
							areaColor: "#FFD181",
							borderColor: "#fff",
							borderWidth: 1,
						},
					},
					layoutCenter: ["50%", "50%"],
					layoutSize: "100%",
					// markPoint: {
					//   symbol: "none",
					// },
					data: data,
				}],
			};
			myChart.setOption(option);
			showTips("成都市");
			// 默认鼠标移出canvas后显示成都的tooltip信息
			myChart.on("globalout", () => {
				setTimeout(() => {
					showTips("成都市");
				}, 3000);
			});

			function showTips(name) {
				data.forEach((item, i) => {
					if (item.name.includes(name)) {
						myChart.dispatchAction({
							type: "showTip",
							seriesIndex: 0,
							dataIndex: i,
						});
						myChart.dispatchAction({
							type: "Select",
							seriesIndex: 0,
							dataIndex: i,
						});
					}
				});
			}
			myChart.setOption(option);
		},

	}
</script>

<style scoped>
	#sichuan {
		width: 230px;
		height: 250px;
	}
</style>