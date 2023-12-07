<template>
	<div id="histogram"></div>
</template>

<script>
	import axios from 'axios'
	import * as echarts from "echarts";
	import sichuanmap from "@/assets/json/sichuan.json";
	export default{
		name:"histogram",
		data() {
			return{
			}		
		},
		mounted() {
			let histogram=echarts.init(document.getElementById("histogram"));//实例化对象
			let option = {
			  tooltip: {
			    backgroundColor: "rgb(196, 255, 249)",
			    trigger: "item",
				},
			  title:{
				text:"四川省各等级旅游景点数",
			    x:'center',
				y:'top',
				textAlign:'left',
				textStyle:{
				fontSize:13
				}	
			  },
			  xAxis: {
			    type: 'category',
			    data:['1A','2A','3A','4A','5A']
				// data: ['成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市','遂宁市','内江市','乐山市','南充市','眉山市','宜宾市','广安市','达州市','雅安市','巴中市','资阳市','阿坝州','甘孜州','凉山州']
			  },
			  yAxis: {
			    type: 'value'
			  },
			  series: [
			    {
			      data: ['2','92','385','323','17'],
			      type: 'bar',
			      showBackground: true,
			      backgroundStyle: {
			        color: 'rgba(180, 180, 180, 0.2)'
			      },
				  layoutSize: "30%",
			    }
			  ]
			};
			histogram.setOption(option)
		}
	}
	
	
</script>

<style>
	#histogram{
		width: 280px;
		height: 280px;
	}
</style>