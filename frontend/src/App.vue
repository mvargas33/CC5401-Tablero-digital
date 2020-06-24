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
    nuevoUsuario (data) {
      console.log(data)
      this.$store.dispatch('newUserEvent', data)
    }
  }
};
</script>

<style>
</style>
