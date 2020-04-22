<template>
  <div id="login-view">
    <div id="form-container" class="col-11">
      <h1 id="login-title" class="mb-2 text-primary">Tablero Digital</h1>
      <h3 class="mb-4 text-primary">Log-in</h3>

      <b-alert v-if="new_user" variant="success" show>Regitro existoso, ahora puedes ingresar.</b-alert>
      <b-alert v-if="wrong_credentials" variant="danger" show>Credenciales incorrectas.</b-alert>
      
      <b-form @keypress="wrong_credentials = false" @submit.prevent="submitForm">
        <label class="sr-only" for="inline-form-input-name">Name</label>
        <b-input v-model="username" class="mb-3" type="email" placeholder="Email" />
        <b-input
          v-model="password"
          style="margin-bottom:1rem;"
          type="password"
          placeholder="Contraseña"
        />
        <b-button type="submit" variant="primary" block>Entrar</b-button>
      </b-form>
      <br />
      <div>
        <span>¿No tienes cuenta? Regístrate </span>
        <router-link to="/signup">aquí</router-link>
        <span>!</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      wrong_credentials: false,
    };
  },
  props: {
    new_user: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    submitForm() {
      // Sends the user to the Home view if credentials are right, else shows
      // an error.
      this.$router.login(this.username, this.password).catch(() => {
        this.wrong_credentials = true;
      });
    }
  }
};
</script>

<style scoped>
#login-view {
  background-color: #52a5ff;
  height: 100%;
  width: 100%;
  overflow: auto;
  position: absolute;
}

#form-container {
  margin: 100px auto;
  width: 30rem;
  border-radius: 5px;
  background: white;
  padding: 34px;
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
  text-align: center;
}

</style>