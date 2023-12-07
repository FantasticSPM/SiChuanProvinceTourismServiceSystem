<!-- 借鉴于网络 emoji表情组件-->
<template>
    <div class="chatIcon">
        <el-popover popper-class="biaoqing"  :width="400" trigger="click">
            <template #reference>
                <el-button class="emotionSelect">&#128514</el-button>
            </template>
            <div class="emotionList">
				<!-- javascript:void(0)伪代码，确保不跳转 -->
                <a href="javascript:void(0);" @click="getEmo(item)" v-for="(item,index) in faceList" :key="index"
                    class="emotionItem">{{item}}</a >
            </div>
        </el-popover>
 
    </div>
</template>
<script>
import appData from "@/assets/emoji"
export default {
    mounted() {
        for (let i in appData) {
            this.faceList.push(appData[i].char);
        }
    },
    data() {
        return {
            faceList: [],
            emojiItem: null,
        };
    },
    methods: {
        getEmo(index) {
            this.emojiItem = index;
            this.$emit("changeText",this.emojiItem)
        }
    }
}
</script>
<style scoped>
.emotionSelect {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.emotionSelect img {
    width: 14px;
    height: 14px;
}
.chatIcon {
    padding: 0 10px;
    font-size: 25px;
}
.emotionList {
    display: flex;
    flex-wrap: wrap;
    padding: 5px;
}
.emotionItem {
    width: 10%;
    font-size: 20px;
    text-align: center;
}
/*包含以下四种的链接*/
.emotionItem {
    text-decoration: none;
}
/*正常的未被访问过的链接*/
.emotionItem:link {
    text-decoration: none;
}
/*已经访问过的链接*/
.emotionItem:visited {
    text-decoration: none;
}
/*鼠标划过(停留)的链接*/
.emotionItem:hover {
    text-decoration: none;
}
/* 正在点击的链接*/
.emotionItem:active {
    text-decoration: none;
}
</style>