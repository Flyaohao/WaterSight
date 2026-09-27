<template>
  <div>
    <div style="height: 100vh; overflow: hidden; display: flex; align-items: center; justify-content: center">
      <div style="font-size: 40px">404 找不到页面 <router-link to="/front/home">返回首页</router-link></div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'NotFound',
  data() {
    return {}
  },
  created() {

  },
  methods: {}
}
</script>

<style scoped>

</style>