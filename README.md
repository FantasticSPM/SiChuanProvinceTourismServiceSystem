# 四川旅游资源服务平台
**一、作品简介**
艰苦卓绝的三年新冠疫情抗争接近尾声，2023年随着疫情防控政策逐渐放开，旅游业努力克服多重因素影响，统筹做好疫情防控和恢复发展。四川省有着得天独厚的自然资源、璀璨夺目的文化瑰宝、五彩斑斓的民俗生活，有着“天府之国”美誉的四川省一直以来作为旅游强省吸引八方游客，于是本系统应运而生。本系统是针对四川省旅游资源服务的B/S端系统平台，可以对四川省范围内地点（居民点，景点）进行搜索定位，并可以对点之间进行路径分析规划、点击地点出现点的相关信息、点击行政区范围出现该行政区内旅行社相关信息；也可以对相关地点进行天气、内置旅游攻略的查询；可以实现游客体验分享功能（博客），供使用该平台的用户进行搜索用户的分享体验，增加对旅游景点的了解；可以实现对九寨沟景点的实时数据监控，并用相关的可视化方法进行展示。

该项目参加第21届SuperMap杯GIS大赛命题开发组，荣获一等奖

**二、数据制作与处理**
开发团队根据命题组所提供的数据，以SuperMap iDesktop 11i为数据处理与数据制作工具，完成了以下系统数据的处理与制作：
1.将“A级旅游景区名录.xlsx”和“旅行社名录.xlsx”导入SuperMap iDesktop 11i，使用数据导入功能增加点数据集“A级旅游景区”,存储四川省A级旅游景区数据；再次利用数据导入功能，在SiChuan.udbx数据源中，增加属性表数据集“旅行社”，存储旅行社信息数据。
2.将四川省行政区划图导入到“SiChuanMap”中，配置标签专题图，并设置标签专题图的可见比例尺范围，修改图层风格，达到地图和系统界面美观协调的效果。
3.对数据集“Network”进行拓扑构网，构建二维网络数据集。

**三、技术路线**
以SuperMap iserver为GIS服务器，用于对地理空间数据的存储和发布，以Django与MySQL相结合，实现对其他类型数据的存储和提取。前端使用vue+element plus，用于快速构建用户界面，使用vuex进行状态管理，使用vue-router进行路由管理，相关的可视化图表使用Echart进行展示渲染，通过SuperMap iClient JavaScript for Leaflet与SuperMap iserver建立通信，实现GIS的相关功能；后端部分使用Django框架构建非GIS功能模块，通过axios进行前后端通信。
