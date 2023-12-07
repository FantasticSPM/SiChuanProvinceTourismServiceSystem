import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
	  Url:" http://localhost",//服务器地址
	  information:""//存放筛选后的信息
  },
  getters: {
  },
  mutations: {
	  updateData(state,data){
		  state.information=data
	  }
  },
  actions: {
	  //请求文章评论数据
	  asyncUsershare({state}){
		  return new Promise((resolve)=>{
			  axios.get(state.Url+':8000/article/index/')
			  .then(res=>{
				  let data={
				  	  articles:[],
				  	  comments:[]
				  };
			  		for (let item in res.data.data){
			  			//将评论和文章中的emoji分别转码显示
			  			if (res.data.data[item].model=='article.article'){
							const patt = /&#\d+;/g;
							const arr = res.data.data[item].fields.content.match(patt) || [];
							let H,L,code;							
							for (let i = 0; i < arr.length; i += 1) {
							    code = arr[i];
							    code = code.replace('&#', '').replace(';', '');
							    H = Math.floor((code - 0x10000) / 0x400) + 0xD800;// 高位
							    L = ((code - 0x10000) % 0x400) + 0xDC00;// 低位
							    code = `&#${code};`;
							    const s = String.fromCharCode(H, L);
							    res.data.data[item].fields.content = res.data.data[item].fields.content.replace(code, s);
							}
			  				data.articles.push(res.data.data[item])			  				
			  			}else{
							const patt = /&#\d+;/g;
							const arr = res.data.data[item].fields.comment_content.match(patt) || [];
							let H,L,code;								
							for (let i = 0; i < arr.length; i += 1) {
							    code = arr[i];
							    code = code.replace('&#', '').replace(';', '');
							    H = Math.floor((code - 0x10000) / 0x400) + 0xD800;// 高位
							    L = ((code - 0x10000) % 0x400) + 0xDC00;// 低位
							    code = `&#${code};`;
							    const s = String.fromCharCode(H, L);
							    res.data.data[item].fields.comment_content = res.data.data[item].fields.comment_content.replace(code, s);
							}							
			  				data.comments.push(res.data.data[item])
			  			}						
			  		}
					data.articles=data.articles.reverse()
					resolve(data) 
			  })			  
		  })		   
	  },
  },
  modules: {
  }
})
