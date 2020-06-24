<template>
  <div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {},
  sockets: {
    new_user (data) {
      console.log('new_user')
      console.log(data)
      //this.$store.dispatch('newUserEvent', data)
    },
    connect: function () {
      console.log('socket connected')
    }
  }
};
</script>

<style>
</style>
