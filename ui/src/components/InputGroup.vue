<template>
    <div class="text_group">
        <div class="input_group" :class="{'is-invalid': error}">
            <!-- 输入框 -->
            <input
                :type="type"
                :placeholder="placeholder"
                :value="value"
                :name="name"
                @input="$emit('input',$event.target.value)"
            >
            <!-- 输入框后面的内容 -->
            <button v-if="btnTitle" @click="$emit('btnClick')" :disabled="disabled" style="border-radius 8px;">{{btnTitle}}</button>
        </div>
        <!-- 验证提示 -->
        <div v-if="error" class="invalid-feedback">{{error}}</div>
    </div>
</template>
<script>
    export default {
        name:"inputGroup",
        props:{
            type: {
                type: String,
                default: "text"
            },
            placeholder:String,
            value:String,
            name:String,
            disabled:Boolean,
            btnTitle:String,  //input框中的文字
            error:String  //验证不正确提示
        }
    }
</script>
