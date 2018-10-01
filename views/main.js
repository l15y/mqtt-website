Vue.component('child', {
    props: ['dizhi'],
    template: '<embed :src="dizhi" width=18 style="margin-left: 6;margin-right: 6;position: relative;top: -2px;"/>'
})
Vue.component('kaiguan', {
    props: ['miaoshu', 'pw', 'activetext', 'inactivetext'],
    template: '<div>{{miaoshu}}：<el-switch v-model="value" active-color="#13ce66" inactive-color="#ff4949" :active-text="activetext" :inactive-text="inactivetext"></el-switch></div>',

    data: function () {
    return {
      value: true
    }
  },
    watch: {
        value: function(val) {
            app.loading = true
            send(val ? 1 : 0, this.pw)
        },
    }
})
var app = new Vue({
    delimiters: ['{[', ']}'],
    el: "#app",
    data: {
        loading: false,
        value2: true,
        tableData: tableData
    },
    watch: {
        value2: function(val) {
            this.loading = true
            send(val ? 1 : 0, 1234)
        }
    }
});