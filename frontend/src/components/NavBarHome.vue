<template>
  <b-navbar id="navbar" type="dark" variant="primary">
    <router-link to="/" class="navbar-brand font-weight-bold">Tablero Digital</router-link>
    <b-navbar-nav class="ml-auto">
      <b-nav-text id="user-name" class="text-white">{{ user.full_name }}</b-nav-text>
      <b-nav-item-dropdown right>
        <b-dropdown-item href="#" @click="$router.logout()">Salir</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>
  </b-navbar>
</template>

<script>
export default {
  name: "NavBarHome",
  props: {
    user: {
      type: Object,
      default: () =>
        Object({
          full_name: "John Doe"
        })
    }
  }
};
</script>

<style>
#navbar {
  box-shadow: 0 3px 3px rgba(0, 0, 0, 0.3);
  z-index: 500;
}
</style>