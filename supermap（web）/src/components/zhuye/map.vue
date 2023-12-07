<template>
	<el-container class="mapbody">
		<el-aside>
			<histogram class="illustration1"></histogram>
			<interest class="illustration2"></interest>
		</el-aside>
		<el-main>
			<div class="wrapper">
				<div class="layer">
					<el-dropdown>
						<span class="dropdown"><img src="@/assets/logo/layers.png" alt="">图层切换</span>
						<template #dropdown>
							<el-dropdown-menu>
								<el-dropdown-item @click="vec">标准地图</el-dropdown-item>
								<el-dropdown-item @click="img">影像地图</el-dropdown-item>
								<el-dropdown-item @click="ter">地形地图</el-dropdown-item>
							</el-dropdown-menu>
						</template>
					</el-dropdown>
				</div>
				<div class="interest">
					<el-dropdown>
						<span class="dropdown"><img src="@/assets/logo/景点.png">景点等级</span>
						<template #dropdown>
							<el-dropdown-menu>
								<el-dropdown-item @click="none">无</el-dropdown-item>
								<el-dropdown-item @click="AAA">3A</el-dropdown-item>
								<el-dropdown-item @click="AAAA">4A</el-dropdown-item>
								<el-dropdown-item @click="AAAAA">5A</el-dropdown-item>
								<el-dropdown-item @click="allA">ALL A</el-dropdown-item>
							</el-dropdown-menu>
						</template>
					</el-dropdown>
				</div>
				<div class="chaxun">
					位置搜索:
					<el-select v-model="inputsql" @keyup.enter="query(inputsql)" filterable @change="query(inputsql)" remote placeholder="请输入内容"
						remote-show-suffix :remote-method="query" no-data-text="没有查到结果" style="margin-bottom: 10px;">
						<el-option v-for="(item,index) in options1" :key="index" :value="item.feature.properties.NAME"
							:label="item.feature.properties.NAME">
							<span style="float: left">{{ item.feature.properties.NAME}}</span>
							<span
								style="float: right;color: var(--el-text-color-secondary);font-size: 10px;">{{item.feature.properties.所在市州}}{{item.feature.properties.所在区县 }}</span>
						</el-option>
					</el-select>
					<el-button @click="navigate"><img src="@/assets/logo/路线.png" /></el-button>
					<el-button type="primary" @click="query(inputsql)">
						<span style="vertical-align: middle"><el-icon style="vertical-align: middle">
								<Search />
							</el-icon>搜索</span>
					</el-button>
					<el-button type="primary" @click="clear">
						<span style="vertical-align: middle"><el-icon style="vertical-align: middle">
								<Search />
							</el-icon>清除</span>
					</el-button>
				</div>
				<div class="navigation" v-if="daohang">
					<el-container>
						<el-header style="display: flex;align-items: center;">
							<div style="position: absolute; right: 10px;">
								<el-col :span="2"><el-button style="background: transparent;border: 0;"><el-icon color="white"
											@click="daohang=false">
											<CloseBold />
										</el-icon></el-button></el-col>
							</div>
						</el-header>
						<el-main>
								 <div v-for="(valueItem,index) in form" :key="index">						
									 <el-select v-model="form[index]" filterable remote placeholder="请输入地点" remote-show-suffix
								reserve-keyword :remote-method="query" style="margin-bottom: 10px;" @change="addPoint(form[index],index)">
										 <el-option v-for="(item,index) in options2" :key="index"
										 	:value="item.feature.geometry.coordinates" :label="item.feature.properties.NAME">
										 	<span style="float: left">{{ item.feature.properties.NAME}}</span>
										 	<span
										 		style="float: right;color: var(--el-text-color-secondary);font-size: 10px;">{{item.feature.properties.所在市州}}{{item.feature.properties.所在区县 }}
											</span>
										</el-option>
									 </el-select>							  
								 </div>
								  <el-button  icon="Plus" @click="addSearch"></el-button>
								  <el-button style="float: right;" icon="Minus" @click="removeSearch"></el-button>
						</el-main>
						<el-footer>
							<el-button  icon="Position" @click="networkchaxun(form)">导航</el-button>
						</el-footer>
					</el-container>
				</div>
				<div id="map"></div>
			</div>
		</el-main>
	</el-container>

</template>

<script>
	import {useStore} from 'vuex'
	import {
		reactive
	} from '@vue/runtime-core';
	import {
		ElMessage
	} from 'element-plus';
	import {
		createElementBlock,
		onMounted,
		onunMounted,
		onUpdated,
		provide,
		ref,
		render
	} from 'vue'
	import interest from '@/components/zhuye/interest/sichuanmap.vue'
	import histogram from '@/components/zhuye/interest/histogram.vue'
	// import querytool from '@/components/zhuye/querytool.vue';
	export default {
		name: 'scMap',
		components: {
			interest,
			histogram
		},
		setup() {
			let store=useStore();
			let Url=store.state.Url
			const inputsql = ref('');//位置搜索框
			let daohang = ref(false);//导航栏的显隐
			const form=ref(['',''])
			// const form=ref([{jw:[]},{jw:[]}]);//导航输入框
			const options1 = ref("")//位置搜索框结果
			const options2 = ref("")//导航输入框结果
			const L = window.L;
			let resultlayer, dataresultlayer, webresultlayer;//相关结果图层
			let pointLayers=[]//点图层组
			let tianditu_vec_w = null; //天地图矢量图层
			let tianditu_cva_w = null; //天地图矢量图层注记	
			let tianditu_img_w = null; //天地图卫星图层
			let tianditu_ter_w = null; //天地图地形图层
			let AAAurl =
				Url+':8090/iserver/services/map-SiChuan/rest/maps/AAA%E6%97%85%E6%B8%B8%E6%99%AF%E5%8C%BA%40SiChuan';
			let AAAAurl =
				Url+':8090/iserver/services/map-SiChuan/rest/maps/AAAA%E6%97%85%E6%B8%B8%E6%99%AF%E5%8C%BA%40SiChuan';
			let AAAAAurl =
				Url+':8090/iserver/services/map-SiChuan/rest/maps/AAAAA%E6%97%85%E6%B8%B8%E6%99%AF%E5%8C%BA%40SiChuan';
			let allAurl =
				Url+':8090/iserver/services/map-SiChuan/rest/maps/A%E7%BA%A7%E6%97%85%E6%B8%B8%E6%99%AF%E5%8C%BA%40SiChuan';
			const mapurl =Url+':8090/iserver/services/map-SiChuan/rest/maps/SiChuan';
			const dataurl = Url+':8090/iserver/services/data-SiChuan/rest/data';
			const networkURL =
				Url+':8090/iserver/services/transportationAnalyst-SiChuan/rest/networkanalyst/Network@SiChuan';
			// provide('map',parent);
			// console.log(parent);
			let map, layers, interest_layers = reactive([]);

			onMounted(() => {

				layers = { //底图集
					tianditu_vec_w: new L.supermap.TiandituTileLayer({
						url: 'http://t0.tianditu.gov.cn/vec_c/wmts?tk=b2bd626091f9d4d1912dedcd8fb7648d',
						layerType: 'vec',
						noWrap: 'true',
					}), //天地图矢量图层
					tianditu_cva_w: new L.supermap.TiandituTileLayer({
						url: 'http://t0.tianditu.gov.cn/cva_c/wmts?tk=b2bd626091f9d4d1912dedcd8fb7648d',
						layerType: 'cva',
						noWrap: 'true',
					}), //天地图矢量图层注记
					tianditu_img_w: new L.supermap.TiandituTileLayer({
						url: 'http://t0.tianditu.gov.cn/img_c/wmts?tk=b2bd626091f9d4d1912dedcd8fb7648d',
						layerType: 'img',
						noWrap: 'true',
					}), //天地图卫星图层
					tianditu_ter_w: new L.supermap.TiandituTileLayer({
						url: 'http://t0.tianditu.gov.cn/ter_c/wmts?tk=b2bd626091f9d4d1912dedcd8fb7648d',
						layerType: 'ter',
						noWrap: 'true',
					}), //天地图地形图层
				};
				interest_layers = { //景点集
					AAA: new L.supermap.TiledMapLayer(AAAurl, {
						noWrap: true,
						attribution: false,
					}), //3A景点图层
					AAAA: new L.supermap.TiledMapLayer(AAAAurl, {
						noWrap: true,
						attribution: false,
					}), //4A景点图层
					AAAAA: new L.supermap.TiledMapLayer(AAAAAurl, {
						noWrap: true,
						attribution: false,
					}), //5A景点图层
					allA: new L.supermap.TiledMapLayer(allAurl, {
						noWrap: true,
						attribution: false,
					}), //所有A级景点图层
				};

				map = L.map('map', { //创建地图对象
					crs: L.CRS.EPSG4326,
					center: [30, 104],
					layers: [layers.tianditu_vec_w],
					maxZoom: 25,
					minZoom: 2,
					zoom: 6,
					attributionControl: false,
				});

				L.control.scale({ //比例尺控件
					maxWidth: 100,
					metric: true,
					imperial: false
				}).addTo(map)
				
				let bounds = L.latLngBounds(L.latLng(-90, -180), L.latLng(90, 180));
				map.setMaxBounds(bounds); //设置地图边界
				new L.supermap.TiledMapLayer(mapurl, { //四川省底图
					noWrap: true,
					attribution: false,
					opacity: 0.5,
				}).addTo(map);
				layers.tianditu_cva_w.setZIndex(1);//标注图层
				layers.tianditu_cva_w.addTo(map);
				// map.addLayer(pointLayers)
				// new L.supermap.TiledMapLayer(dataurl).addTo(map)
				// L.control.layers(layers).addTo(map)//leaflet自带的图层控制面板
				map.on('click',e=>{
					resultlayer && map.removeLayer(resultlayer);
					webresultlayer && map.removeLayer(webresultlayer);
					dataresultlayer && map.removeLayer(dataresultlayer);
				    for(let item in pointLayers){
					   pointLayers[item] && map.removeLayer(pointLayers[item]);
				    }
					let x=e.latlng.lng;//点击点的经度
					let y=e.latlng.lat//点击点的纬度
					let point=new L.circleMarker([y,x]);
					
					let geometryParam =  new L.supermap.GetFeaturesByGeometryParameters({
						geometry:point,
						datasetNames:["SiChuan:市"],
						spatialQueryMode:'INTERSECT'
					});
					
					 new L.supermap.FeatureService(dataurl).getFeaturesByGeometry(geometryParam,(serviceResult)=>{						
						 if(serviceResult.result.features.features[0]==undefined){//当获取到四川省以外经纬度，查询结果为空时，后面不执行
							 return
						 }						  
						 let postalCode=serviceResult.result.features.features[0].properties.邮政编码;
						 let city=serviceResult.result.features.features[0].properties.NAME
						 resultlayer=L.geoJSON(serviceResult.result.features).addTo(map);
				
						 let dataparam = new L.supermap.GetFeaturesBySQLParameters({ //数据查询
						    toIndex:1000,
						 	queryParameter: {
						 		attributeFilter: "邮政编码 ='"+postalCode+"'" 
						 	},
						 	datasetNames: ["SiChuan:旅行社"],
						 });
						  
						 L.supermap.featureService(dataurl).getFeaturesBySQL(dataparam, (serviceResult) => {
							 // console.log(serviceResult.result.features.features)													
				            let DS=serviceResult.result.features.features;
							let DataLength=serviceResult.result.features.features.length;//数据长度
							// let i=1;//初始页面
							// let eachPAGE=DS.slice(i*10,i*10+10);//每个页面的数据
							let num=10//每页的个数
							let pageNum=Math.ceil(DataLength/num)//总页数
							let tips=`
							<table width="1200" class="maptable" >
							     <caption>${city}旅行社信息</caption>
								 <thead style="background-color:#20C997";color:white>
							     <tr><th>旅行社中文名称</th>
								     <th>许可证编号</th>
									 <th>邮政编码</th>
									 <th>固定电话</th>
									 <th>传真号码</th>
									 <th>地址</th>								 
								</tr>
								</thead>
								<tbody id="iData">
				                    ${
										DS.slice(0,num).map(item=>{
											return `<tr>
											<td> ${item.properties.旅行社中文名称}</td>
											<td> ${item.properties.许可证编号}</td>
											<td> ${item.properties.邮政编码}</td>
											<td> ${item.properties.固定电话}</td>
											<td> ${item.properties.传真号码}</td>
											<td> ${item.properties.地址}</td>									
											</tr>`
										}).join('')
									}
								</tbody>
							</table>
							<div align="center">
							   <span id="iPage">
							       共${DataLength}条数据 分${pageNum}页 当前第1页
							   </span> 
							   <span id="ibarcon" >

							   </span>
							<div>  
							`; 	
							let boxDOM=document.createElement('div')
							boxDOM.innerHTML=tips
														
							let tempStr ="跳转至";
							tempStr +="<select id='iSelect' style='width:60px' >"; 
							for(var j=1;j<=pageNum;j++){
								tempStr +="<option  value='"+j+"' >第"+ j +"页</option>";
							}
							tempStr +="</select>";
							boxDOM.childNodes[3].childNodes[3].innerHTML = tempStr;
							
							resultlayer.bindPopup(boxDOM,{
								maxWidth:1200,
								autoPanPaddingTopLeft:[50,70],
								autoPanPaddingBottomRight:[50,60]
							}).openPopup();
						   
						   
							boxDOM.childNodes[3].childNodes[3].childNodes[1].onchange=function(){
								let index=document.getElementById("iSelect").selectedIndex//索引
								let pagenum=document.getElementById("iSelect").options[index].value//页码								
								let data=DS.slice((pagenum-1)*num,pagenum*num)//每页的数据
								let ob=data.map(item=>{
											return `<tr>
											<td> ${item.properties.旅行社中文名称}</td>
											<td> ${item.properties.许可证编号}</td>
											<td> ${item.properties.邮政编码}</td>
											<td> ${item.properties.固定电话}</td>
											<td> ${item.properties.传真号码}</td>
											<td> ${item.properties.地址}</td>									
											</tr>`
										})
								document.getElementById('iData').innerHTML=ob.join("")
								let page=`共${DataLength}条数据 分${pageNum}页 当前第${pagenum}页`
								document.getElementById('iPage').innerHTML=page
							}							
						 })						 
					 });
				})
			});

			function clear() { //清除查询结果
				resultlayer && map.removeLayer(resultlayer);
				webresultlayer && map.removeLayer(webresultlayer);
				dataresultlayer && map.removeLayer(dataresultlayer);
				for(let item in pointLayers){
					pointLayers[item] && map.removeLayer(pointLayers[item]);
				}
								
			};


			function query(place) { //地图查询函数		
				resultlayer && map.removeLayer(resultlayer);
				webresultlayer && map.removeLayer(webresultlayer);
				dataresultlayer && map.removeLayer(dataresultlayer);
				if (place === '') {
					return
				};
				// let mapparam1=new L.supermap.QueryBySQLParameters({//地图查询
				// 	queryParams:{
				// 		name:"市@SiChuan#1",
				// 		attributeFilter:"市名称 like'"+inputsql.value+"'"
				// 	}
				// });
				// L.supermap.queryService(url).queryBySQL(mapparam1,(serviceResult)=>{
				// 	resultlayer = L.geoJSON(serviceResult.result.recordsets[0].features)
				// 	resultlayer.addTo(map)
				// });
				let dataparam = new L.supermap.GetFeaturesBySQLParameters({ //数据查询
					queryParameter: {
						attributeFilter: "NAME like '%" + place + "%'" //模糊查询，查询结果是以输入框开头的名称
					},
					datasetNames: ["SiChuan:A级旅游景区","SiChuan:居民地地名"],
					//"SiChuan:水域","SiChuan:公路","SiChuan:铁路","SiChuan:市", "SiChuan:县","SiChuan:居民地地名", 
				});
				L.supermap.featureService(dataurl).getFeaturesBySQL(dataparam, (serviceResult) => {
					dataresultlayer = L.geoJSON(serviceResult.result.features);
					dataresultlayer.addTo(map);
					options1.value = dataresultlayer._layers
					options2.value = dataresultlayer._layers
					// console.log(dataresultlayer._layers)
					if (Object.keys(dataresultlayer._layers).length != 0) { //判断搜索出来的结果是否为空
						const firstid = dataresultlayer._leaflet_id - 1; //搜索到的第一个对象
						const i = Object.keys(dataresultlayer._layers).length; //搜索到的结果的个数
						ElMessage("为您找到" + i + "个结果");
						let id = firstid; //赋予每个对象的id
						//遍历每个点的信息
						let lng = 0; //初始经度值
						let lat = 0; //初始纬度值
						for (id; id <= firstid + i; id++) {
							if (id != firstid + 1) {
								let tips;
								lng = lng + dataresultlayer._layers[id].feature.geometry.coordinates[0]
								lat = lat + dataresultlayer._layers[id].feature.geometry.coordinates[1]
								// console.log(dataresultlayer._layers[id].feature.properties)
								if (dataresultlayer._layers[id].feature.properties.hasOwnProperty('NUM_5A')) {
									tips =
										`<table class="maptable1">
									<tr>
									    <th>名称</th>
										<td>${dataresultlayer._layers[id].feature.properties.NAME}</td>
									</tr>
									<tr>
									    <th>3A</th>
										<td>${dataresultlayer._layers[id].feature.properties.NUM_3A}</td>
									</tr>
									<tr>
									    <th>4A</th>
										<td>${dataresultlayer._layers[id].feature.properties.NUM_4A}</td>
									</tr>
									<tr>
									    <th>5A</th>
										<td>${dataresultlayer._layers[id].feature.properties.NUM_5A}</td>
									</tr>
									</table>`
								} else if (dataresultlayer._layers[id].feature.properties.hasOwnProperty('等级')) {
									tips =
										`<table class="maptable1">
									   <tr>
									       <th>名称</th>
										   <td>${dataresultlayer._layers[id].feature.properties.NAME}</td>
									   </tr>
									   <tr>
									       <th>地址</th>
										   <td>${dataresultlayer._layers[id].feature.properties.地址}</td>
									   </tr>
									   <tr>
									       <th>所在区县</th>
										   <td>${dataresultlayer._layers[id].feature.properties.所在区县}</td>
									   </tr>
									   <tr>
									       <th>所在市州</th>
										   <td>${dataresultlayer._layers[id].feature.properties.所在市州}</td>
									   </tr>
									   <tr>
									       <th>等级</th>
									   	   <td>${dataresultlayer._layers[id].feature.properties.等级}</td>
									   </tr>
									   <tr>
									       <th>经度</th>
									   	   <td>${dataresultlayer._layers[id].feature.properties.经度}</td>
									   </tr>
									   <tr>
									       <th>纬度</th>
									   	   <td>${dataresultlayer._layers[id].feature.properties.纬度}</td>
									   </tr>
									</table>`
								} else {
									tips = dataresultlayer._layers[id].feature.properties.NAME
								};
								dataresultlayer._layers[id].bindPopup(tips,{
									maxWidth:1200,
									autoPanPaddingTopLeft:[50,100],
								});
							}
						};
						let positionZoom//缩放比例
						if (i == 1) {
							positionZoom = 10
						} else if (i < 10) {
							positionZoom = 9
						} else {
							positionZoom = 8
						}
						map.flyTo(L.latLng(lat / i, lng / i), positionZoom) //移动视野到查询出来的要素的几何中心并进行相应缩放
					} else {
						ElMessage("抱歉，未查到含" + "【" + place + "】" + "的结果！")
					}
				});
			};

			function navigate() {//导航栏显隐
				daohang.value = true;
			};
			
			function addSearch(){//导航输入框的增加
				form.value.push([])
			}
			
			function removeSearch(){//导航输入框的移除
				if (form.value.length>2){
					form.value.pop()
					webresultlayer && map.removeLayer(webresultlayer);
					for(let i in pointLayers){
						if(pointLayers[i]){
							pointLayers[i].clearLayers()
						}
					}
				}			
			}

            function addPoint(point,index){
				
				dataresultlayer && map.removeLayer(dataresultlayer);
				webresultlayer && map.removeLayer(webresultlayer);
				//pointLayers[index]对应相应的el-select的搜索结果图层
				//如果该搜索框存在之前搜索的图层，则清空
				if(pointLayers[index]){
					pointLayers[index].clearLayers()
				}
				//交换经纬度
				let Point=[point[1], point[0]]
				//移动视野到该点
				map.flyTo(Point)
				//将该点放入图层
				let pointLayer=new L.featureGroup([])
				let markerTitle
				if(index==0){
					markerTitle="起点"
				}else{
					markerTitle="目的地"+index
				}
				new L.marker(Point,{
					title:markerTitle
				}).addTo(pointLayer)
				//将该图层放置在导航el-select图层组里面
				pointLayers[index]=pointLayer
				//在地图上添加该点图层
				map.addLayer(pointLayers[index])
            }

			function networkchaxun(body) {//路径规划（导航）函数
		    	resultlayer && map.removeLayer(resultlayer);
				dataresultlayer && map.removeLayer(dataresultlayer);
				webresultlayer && map.removeLayer(webresultlayer);

				if(body.some(item=>{return item==""||item==undefined||item==null})){
					ElMessage("请输入完整信息！")
					return
				}//判断输入值是否有空值，有空值则该函数后面不执行
				for (let item in body){
					addPoint(body[item],item)
				}
				let newArr=body.map(item=>{
					return L.point(item)
				})	
				
				// let layers=[]
				// let newArr1=body.map(item=>{
				// 	let layer=L.marker([item.jw[1], item.jw[0]]);//批量添加地点
				// 	layers.push(layer)//将这些点放入一个图层，便于清除
				// 	return item.jw
				// })	
				// Pmarker=L.layerGroup(layers)
				// map.addLayer(Pmarker)
				let center=[0,0]
				for(let i=0;i<body.length;i++){
					center[0]=center[0]+body[i][1]
					center[1]=center[1]+body[i][0]
				}
				center[0]=center[0]/body.length
				center[1]=center[1]/body.length

				let findPathService = L.supermap.networkAnalystService(networkURL);
				//创建最佳路径分析参数实例
				let resultSetting = new SuperMap.TransportationAnalystResultSetting({
					returnEdgeFeatures: true,
					returnEdgeGeometry: true,
					returnEdgeIDs: true,
					returnNodeFeatures: true,
					returnNodeGeometry: true,
					returnNodeIDs: true,
					returnPathGuides: true,
					returnRoutes: true
				});
				//网络分析通用参数类设置
				let analystParameter = new SuperMap.TransportationAnalystParameter({
					resultSetting: resultSetting,
					weightFieldName: "length"
				});
				let findPathParameter = new SuperMap.FindPathParameters({
					isAnalyzeById: false,
					nodes: newArr,
					parameter: analystParameter
				});
				//进行路径查找
				findPathService.findPath(findPathParameter, function(serviceResult) {
					let result = serviceResult.result;
					result.pathList.map(function(result) {
						webresultlayer = L.geoJSON(result.route).addTo(map);
						let length = result.weight;
						ElMessage("您预计需要【" + Math.ceil(length / 1000 / 5.35) + "】小时到达")
						// console.log(length)
						let positionZoom
						if(length<50000){
							positionZoom=10
						}else if(length<100000){
							positionZoom=9
						}else if(length<900000){
							positionZoom=6.5
						}else{
							positionZoom=5.5
						}
						map.flyTo(center, positionZoom)
					})
				});
				
			}

			function vec() { //制作切换矢量图层功能
				layers.tianditu_vec_w.setZIndex(0);
				layers.tianditu_vec_w.addTo(map);
				layers.tianditu_img_w.remove(map);
				layers.tianditu_ter_w.remove(map);
			};

			function img() { //制作切换影像图层功能
				layers.tianditu_img_w.setZIndex(0);
				layers.tianditu_img_w.addTo(map);
				layers.tianditu_vec_w.remove(map);
				layers.tianditu_ter_w.remove(map);
			};

			function ter() { //制作切换地形图层功能
				layers.tianditu_ter_w.setZIndex(0);
				layers.tianditu_ter_w.addTo(map);
				layers.tianditu_vec_w.remove(map);
				layers.tianditu_img_w.remove(map);
			};
			
			function none() {//无景点等级图层
				// layers.tianditu_ter_w.setZIndex(0);
				interest_layers.AAA.remove(map);
				interest_layers.AAAA.remove(map);
				interest_layers.AAAAA.remove(map);
				interest_layers.allA.remove(map);
			};

			function AAA() {//AAA图层显示
				// layers.tianditu_ter_w.setZIndex(0);
				interest_layers.AAA.addTo(map);
				interest_layers.AAAA.remove(map);
				interest_layers.AAAAA.remove(map);
				interest_layers.allA.remove(map);
			};

			function AAAA() {//AAAA图层显示
				// layers.tianditu_ter_w.setZIndex(0);
				interest_layers.AAAA.addTo(map);
				interest_layers.AAA.remove(map);
				interest_layers.AAAAA.remove(map);
				interest_layers.allA.remove(map);
			};

			function AAAAA() {//AAAAA图层显示
				// layers.tianditu_ter_w.setZIndex(0);
				interest_layers.AAAAA.addTo(map);
				interest_layers.AAA.remove(map);
				interest_layers.AAAA.remove(map);
				interest_layers.allA.remove(map);
			};

			function allA() {//allA图层显示
				// layers.tianditu_ter_w.setZIndex(0);
				interest_layers.allA.addTo(map);
				interest_layers.AAA.remove(map);
				interest_layers.AAAA.remove(map);
				interest_layers.AAAAA.remove(map);
			};
			
			return {
				vec,img,ter,
				inputsql,query,addPoint,
				daohang,navigate,form,addSearch,removeSearch,networkchaxun,				
				options1,options2,
				clear,
				none,AAA,AAAA,AAAAA,allA,					
			}
		},
	}
</script>

<style>
	.mapbody{
		height: 700px;
		background: linear-gradient(220.55deg, #72EDF2 0%, #A7BFE8 100%);
	}
	#map {
		width: 1050px;
		height: 650px;
		z-index: 0;
		border-radius: 15px;
	}

	.wrapper {
		position: relative;
	}

	.layer {
		position: absolute;
		right: 50px;
		top: 20px;
		z-index: 1;
	}

	.interest {
		position: absolute;
		right: 200px;
		top: 20px;
		z-index: 1;
	}

	.chaxun {
		position: absolute;
		left: 50px;
		top: 20px;
		z-index: 1;
	}

	.illustration1 {
		
		margin-top: 50px;
		margin-left: 20px;
		/* bottom: 20px; */

	}
	
	.illustration2 {
		margin: 0 auto;
		margin-top: 60px;
		/* position: absolute; */
		/* left: 40px;
		top: 20px; */
		/* z-index: 1; */
	}
	
	.el-input {
		width: 300px;
		margin-left: 10px;
		margin-right: 20px;
	}

	.dropdown {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.navigation {
		width: 400px;
		top: 20px;
		left: 50px;
		position: absolute;
		z-index: 1;
		background: url("@/assets/background/negivation.png")  0 0 no-repeat,linear-gradient(to bottom,#a0cfff 0%, #79bbff 100%);
		
		/* background-image: linear-gradient(to right,#ecf5ff 0%, #a0cfff 100%),linear-gradient(to bottom,#a0cfff 0%, #79bbff 100%); */
		/* background-color: #3d93fd; */
		box-shadow: 6px 6px 12px 0 rgba(0, 0, 12, 0.3);
		border-radius: 4px;
	}

    .maptable,.maptable1{
		font-family: OPPO;
		border-collapse: collapse;
		border: 1px dashed white;
	}
	.maptable tbody{
		/* display: block; */
	}
	.maptable thead,
	.maptable tbody tr,.maptable1 thead,
	.maptable1 tbody tr{
		width: 100%;
		display: table;
		table-layout: fixed;
	}
	.maptable caption{
		font-size: 30px;
	}
	.maptable td:nth-child(6){
		width: 200px;
	}
	.maptable th:nth-child(6){
		width: 200px;
	}
/* 	.maptable tr td:nth-child(9){
		background-color: white;
	} */
	.maptable tr:nth-child(even){
		background-color: #FFFFFF;
	}
	.maptable1 tr:nth-child(even){
		background-color: #8ed5ed;
	}
	.maptable tr:nth-child(odd){
		background-color: #9acbeb;
	}
	.maptable1 tr:nth-child(odd){
		background-color: #f9f8f8;
	}
	.maptable th:nth-child(odd){
		background-color: #CCCCFF;
	}
	.maptable{
		width: 900px;
	}
	.maptable1{
		width: 500px;
	}
	.maptable th,.maptable1 th{
		/* color: white; */
		height: 30px;
		font-size: 15px;
		font-weight: lighter;
		letter-spacing: 2px;
		/* border-radius: 5px; */
		/* background-color: #FED68F; */
		border: 0px;
		text-align: center;
	}
	.maptable tr td,.maptable1 tr td{
		/* border: 1px dotted white; */
		height: 20px;
		text-align: center;
	}
	.maptable tr:hover,.maptable1 tr:hover{
		background-color: #CCDDFF;
	}
</style>