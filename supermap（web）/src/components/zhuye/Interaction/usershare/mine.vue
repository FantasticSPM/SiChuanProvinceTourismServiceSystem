<template>
	<div style="font-family: Zhuo;margin: 20px 0 20px 0;"><el-icon><StarFilled /></el-icon>我的发帖&#128512</div>
	<div class="hotBody">
     	<div v-for="(item,index) in articles" :key="index" style=" border: 2px solid #e6e6e6;box-shadow: 0 2px 8px 0 rgba(0, 0, 12, 0.3); margin-bottom: 5px;" >
     		<el-container>
     			<el-header style="height: 30px;">
     				<span style="display: flex;align-items: center;font-weight: bold;"><el-icon size="30"><UserFilled /></el-icon>{{item.fields.author}}</span>
     				<span style="float: right;" >
     				  <el-button @click="deleteArticle(item.pk)" style="border: 0;"><el-icon><Delete /></el-icon></el-button>
     				</span>
     				<!-- <div style="font-size: 5px;color: pink;">{{item.fields.publish_time.substring(0,10)}}&nbsp&nbsp{{item.fields.publish_time.substring(11,16)}}</div> -->
     			</el-header>
     			<el-main>
     				<div style="font-family: OPPO;white-space: pre-wrap;">{{item.fields.content}}</div>
     					<div v-if="item.fields.img_url!=null">
     						  <el-image 
     						    style="width: 100px; height: 100px"
     						    :src="fileurl+item.fields.img_url" 
     						    :preview-src-list="[fileurl+item.fields.img_url]">
     						  </el-image>
     					</div>
     			</el-main>
     			<el-footer style="height: 100%;">
					<Emoji ref="getEmoji" @changeText='changeText' @click="getIndex(index)"></Emoji>
     				<el-input v-model="comment[index]" :id="nameID(index)" prefix-icon="ChatDotSquare" placeholder="说点什么吧..." @keyup.enter="commentArticle(comment[index],item.pk,usename)"><template #append><el-button @click="commentArticle(comment[index],item.pk,usename)">发送</el-button></template></el-input>
     				<div v-for="(i,index) in comments" :key="index" style="margin-top: 10px;margin-bottom: 10px;">
     					<div v-if="item.pk==i.fields.article">
     						<span style="font-weight: bold;">{{i.fields.comment_author}}</span>:<span style="white-space: pre-wrap;">{{i.fields.comment_content}}</span>
     					</div>					
     				</div>
     			</el-footer>
     		</el-container>		
     	</div>
</div>
		 <el-empty v-show="articles==''" description="还没有分享任何内容,快来发布吧"></el-empty>
</template>

<script>
	import {
		ElMessage
	} from 'element-plus'
	import Emoji from '@/components/emoji.vue'
	
	export default{
		components:{
			Emoji
		},
		data() {
			return{
				articles:[],//接受的所有的体验分享
				comments:[],//接受所有的评论
				comment:[],//发表的评论
				fileurl:this.$store.state.Url+':8000/static/image/',//后端存放照片的路径
				isIMGvisable:false,//照片预览显隐性
				usename:"",//用户名
				inputIndex:''//输入框索引，用来合成动态id
			}
		},
		methods:{
			commentArticle(x,y,z){
				const patt = /[\ud800-\udbff][\udc00-\udfff]/g; // 检测utf16字符正则
				x = x.replace(patt, (char) => {
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
				this.$axios.post(this.$store.state.Url+':8000/article/comment_control/',JSON.stringify({
					comment_content:x,
					article_id:y,
					username:z
				})).then(res=>{
					ElMessage("评论成功")
					location.reload()
				})
			},
			deleteArticle(body){
				this.$axios.post(this.$store.state.Url+':8000/article/article_delete/',JSON.stringify({
					article_id: body,
				})).then(res=>{
					ElMessage("删除成功")
					location.reload()
				})
			},
			nameID(index){
				return 'INPUT'+index
			},
			getIndex(index){
				this.inputIndex=index
			},
			changeText(data) {
				let InputID='INPUT'+this.inputIndex
				let textArea = document.getElementById(InputID);
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
				this.comment[this.inputIndex] = textArea.value;// 要同步data中的数据		
			},

		},
		mounted() {
			this.usename = JSON.parse(localStorage.getItem('Info')).usename;
			this.$store.dispatch("asyncUsershare").then(res=>{
				// this.articles=res.articles;
				this.comments=res.comments;
				for(let item in res.articles){
					// console.log(res.articles[item].fields.author)
					if(res.articles[item].fields.author==this.usename){
						this.articles.push(res.articles[item])
					}
				}
			})			
		}
	}
	

</script>

<style scoped>
	.hotBody{
		background: url('@/assets/background/chat1.png');
	}
</style>