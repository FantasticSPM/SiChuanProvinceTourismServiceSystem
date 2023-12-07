<template>
	<el-container>
		<el-header>
			<el-row :gutter="20">
				<el-col :span="2"></el-col>
				<el-col :span="18">
					<el-input v-model="search" placeholder="搜索共享" size="large" class="research"
						@keydown.enter="searchShare" clearable>
						<template #append>
							<el-button @click="searchShare">
								<el-icon>
									<Search />
								</el-icon>
							</el-button>
						</template>
					</el-input>
				</el-col>
				<el-col :span="4">
					<el-button @click="fabu=!fabu" color="rgba(255,255,255,0.5)" round>
						<el-icon>
							<Position />
						</el-icon>发布心情
					</el-button>
				</el-col>
			</el-row>

		</el-header>
		<el-container>
			<!-- 			<el-aside>
				<el-menu mode="vertical">
					<el-menu-item index="1"><el-icon>
							<ChatLineRound />
						</el-icon>话题榜</el-menu-item>
					<el-menu-item index="2"><el-icon>
							<Histogram />
						</el-icon>热搜榜</el-menu-item>
					<el-menu-item index="3"><el-icon>
							<Document />
						</el-icon>要闻榜</el-menu-item>
				</el-menu>
			</el-aside> -->
			<el-main class="shareBody">
				<!-- action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15" "-->
				<el-dialog v-model="fabu" title="发布" width="700px" append-to-body>
					<el-input id="useShareInput" type="textarea" v-model="ruleForm.content" placeholder="把想分享的写下来吧!" :rows="5">
						
					</el-input>
					<Emoji ref="getEmoji" @changeText='changeText' style="width: 100px;"></Emoji>		
					<el-upload :file-list="fileList" action="" list-type="picture-card" :limit="1"
						:on-change="UploadImage" :disabled="isdisabled" :on-preview="handlePictureCardPreview"
						:on-remove="handleRemove" :auto-upload="false" :on-exceed="Pictureexceed">
						<el-icon>
							<Plus />
						</el-icon>
					</el-upload>
					<el-dialog v-model="dialogVisible" style="line-height: 0;">
						<img style="width: 100%;height: 100%;" :src="dialogImageUrl" alt="" />
					</el-dialog>

					<template #footer>
						<span class="dialog-footer">
							<el-button @click="fabu = false">取消</el-button>
							<el-button type="primary" @click="upload">上传</el-button>
						</span>
					</template>
				</el-dialog>
				<el-menu mode="horizontal" router style="background: transparent;">
					<el-menu-item index="/zhuye/usershare/hot">🔥热门</el-menu-item>
					<el-menu-item index="/zhuye/usershare/mine">🌐我的</el-menu-item>
					<el-menu-item ></el-menu-item>					
				</el-menu>
				<router-view name="share"></router-view>
			</el-main>
		</el-container>
		<el-footer>

		</el-footer>
	</el-container>


</template>

<script>
	import {
		ElMessage
	} from 'element-plus'
	import Emoji from '@/components/emoji.vue'
	export default {
		name: "usershare",
		components:{
			Emoji
		},
		data() {
			return {
				search: "",//搜索文本框
				fabu: false,//分享框的显隐性
				//提交信息
				ruleForm: {
					usename: "",
					content: "",
					img: ""
				},
				fileList: [],//照片
				dialogImageUrl: "",//照片url
				dialogVisible: false,//照片预览显隐性
				isdisabled: false,//照片上传限制
			}
		},
		methods: {
			UploadImage(file, filelist) {
				// let fd=new FormData()
				// // console.log(fd)
				// fd.append('img',file.raw)
				// console.log(filelist.length)
				// console.log(fd.get('img'))
				// this.$axios.post('http://localhost:8000/uploadfile/uploadimage/',fd,{Headers:{'Content-Type':'multipart/form-data'}}).then(response=>{
				// 	console.log("上传数据到:"+response.data)
				// // 	this.image=response.data
				// })
				this.ruleForm.img = file.raw
				// console.log(file.raw)
			},
			handleRemove(file, fileList) { //图片移除功能
				console.log(file, fileList)
			},
			handlePictureCardPreview(file) { //图片预览功能
				console.log(file.url)
				this.dialogVisible = true
				this.dialogImageUrl = file.url
			},
			Pictureexceed(file, filelist) { //图片超限功能
				this.isdisabled = true
				ElMessage.warning("最多只能上传一张图片！")
			},
			upload() {
				//用FormData装照片文件
				let fd = new FormData()
				fd.append("usename", this.ruleForm.usename)
				const patt = /[\ud800-\udbff][\udc00-\udfff]/g; // 检测utf16字符正则，将emoji字符进行转码储存数据库
				this.ruleForm.content = this.ruleForm.content.replace(patt, (char) => {
				    let H;
				    let L;
				    let code;
				    let s;				
				    if (char.length === 2) {
				        H = char.charCodeAt(0); // 取出高位
				        L = char.charCodeAt(1); // 取出低位
				        code = (H - 0xD800) * 0x400 + 0x10000 + L - 0xDC00; // 转换算法
				        s = `&#${code};`;
						console.log(s)
					} else {
				        s = char;
				    }				
				return s;
				});
				fd.append("content", this.ruleForm.content)
				fd.append("img", this.ruleForm.img)

				if (this.ruleForm.content == "") {
					ElMessage("请输入内容")
				} else {
					this.$axios.post(this.$store.state.Url+':8000/article/article_create/', fd, {
						Headers: {//请求头
							'Content-Type': 'multipart/form-data'
						}
					}).then(res => {
						ElMessage("发布成功！");
						setTimeout(function(){
							location.reload()
						},2000)//延迟一秒刷新页面

					}).catch(err => {
						console.log(err)
					})
				}
			},
			searchShare() {
				if(this.search==''){
					return
				}
				//vuex中获取体验分享信息，并进行筛选
				this.$store.dispatch("asyncUsershare").then(res => {
					let FilteredArticles = []
					res.articles.map(item => {
						if (item.fields.content.indexOf(this.search) > -1) {
							FilteredArticles.push(item)
						}
					})
					if(FilteredArticles.length!=0){
						ElMessage("搜索成功！")
					}else{
						ElMessage("抱歉，没有搜索到含" + "【" + this.search + "】" + "的分享！")
					}
					//vuex中提交筛选后的信息
					this.$store.commit('updateData', FilteredArticles)					
				})
				
			},
			changeText(data) {
				//接收emoji组件中接受emoji
				let textArea = document.getElementById('useShareInput');
				function changeSelectedText(obj, str) {
				    if (window.getSelection) {
				        // 非IE浏览器
				        textArea.setRangeText(str);
				          // 在未选中文本的情况下，重新设置光标位置
				        textArea.selectionStart += str.length;
				        textArea.focus()
				    } else if (document.selection) {
				         // IE浏览器
				        obj.focus();
				        var sel = document.selection.createRange();
				        sel.text = str;
				        }
				}
				changeSelectedText(textArea, data);
				this.ruleForm.content = textArea.value;// 要同步data中的数据		
			},
		},
		mounted() {
			//从本地仓库中获取用户名，用于发表体验感受，将体验与用户名绑定，以供后端进行数据库操作
			this.ruleForm.usename = JSON.parse(localStorage.getItem('Info')).usename;
		}
	}
</script>

<style scoped>

	.research {
		width: 800px;
	}

	.el-input__inner {
		background-color: transparent;
		opacity: 1;
		box-shadow: 2px 2px 0 0 rgba(0, 0, 0, 0.2);
	}

	.el-header {
		height: 100px;
		text-align: center;
		background: url('@/assets/background/share-header.png');
	}

	.el-row {
		margin-top: 30px;
		text-align: center;
		/* 	align-items: center; */
		vertical-align: middle;
	}

	.el-aside {
		text-align: center;
	}

	.lable {
		font-size: 30px;
		text-align: center;
	}

	.el-dialog {
		position: absolute;
		z-index: 2;
		overflow: hidden;
	}

	.input-with-select .el-input-group__prepend {
		background-color: var(--el-fill-color-blank);
	}
	.shareBody{
		background: url('@/assets/background/robot.png');
		background-repeat: no-repeat;
		/* background-position: top right; */
	}
</style>