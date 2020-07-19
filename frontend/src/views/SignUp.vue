<template>
  <div id="login-view">
    <div id="form-container" class="col-11">
      <h1 class="text-primary text-center mb-4">Registro de cuenta</h1>

      <b-form @submit.prevent="sendForm">
        <b-form-group label="Ingresa tu dirección de email:" label-for="email">
          <b-input @keypress="resetUsernameFeedback()" :class="{'is-invalid': !(valid_username && api_valid_username)}"
            v-model="user.username" id="email" type="email" placeholder="Email" required></b-input>
          <small class="form-text" :class="classes_username">
            Email requerido. 150 caracteres máximo.
          </small>
          <b-form-invalid-feedback v-html="api_username_feedback" :state="api_valid_username">
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group label="Ingresa tu nombre:" label-for="first-name">
          <b-input @keypress="valid_first_name = true" v-model="user.first_name" id="first-name" :class="{'is-invalid': !valid_first_name}" type="text" placeholder="Nombre" required></b-input>
          <small class="form-text" :class="classes_first_name">
            Campo requerido. 30 caracteres máximo.
          </small>
        </b-form-group>
        <b-form-group label="Ingresa tu apellido:" label-for="last-name">
          <b-input @keypress="valid_last_name = true" v-model="user.last_name" id="last-name" :class="{'is-invalid': !valid_last_name}" type="text" placeholder="Apellido" required></b-input>
          <small class="form-text" :class="classes_last_name">
            Campo requerido. 150 caracteres máximo.
          </small>
        </b-form-group>
        <b-form-group label="Ingresa tu contraseña:" label-for="password">
          <b-input @keypress="valid_password = true;valid_repeated_password = true"
          @keydown.delete="valid_password = true;valid_repeated_password = true"
          v-model="user.password" id="password" :class="{'is-invalid': !valid_password}" type="password" placeholder="Contraseña" required></b-input>
          <small class="form-text" :class="classes_password">
            Campo requerido.
          </small>
        </b-form-group>
        <!-- Repetición de contraseña -->
        <b-form-group label="Repite tu contraseña:" label-for="repeated_password">
          <b-input @keypress="valid_password = true;valid_repeated_password = true"
          @keydown.delete="valid_password = true;valid_repeated_password = true"
          
          v-model="repeated_password" id="password_rep" :class="{'is-invalid': !valid_repeated_password}" type="password" placeholder="Repita la Contraseña" required></b-input>
          <small class="form-text" :class="classes_rep_password" v-if="!valid_repeated_password">
            Las contraseñas no coinciden.
          </small>
        </b-form-group>
        <!-- Botón de crear -->
        <b-button type="submit" block variant="success">Crear</b-button>
      </b-form>

      <br />
  
      <div class="text-center">
        <span>¿Ya tienes cuenta? Ingresa </span>
        <router-link to="/login">aquí!</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/custom_axios.js';

function computClasses(is_valid) {
  return {
    'text-danger': !is_valid,
    'text-muted': is_valid,
  };
}

export default {
  name: "SignUp",
  data() {
    return {
      user: {
        username: '', // The email of the user
        first_name: '',
        last_name: '',
        password: '',
      },
      api_username_feedback: '', // Feedback from REST API
      api_valid_username: true,
      valid_username: true,
      valid_first_name: true,
      valid_last_name: true,
      valid_password: true,
      valid_repeated_password: true,
      repeated_password: ''
    }
  },
  computed: {
      // Classes for form text
      classes_username() { return computClasses(this.valid_username && this.api_valid_username); },
      classes_first_name() { return computClasses(this.valid_first_name); },
      classes_last_name() { return computClasses(this.valid_last_name); },
      classes_password() { return computClasses(this.valid_password); },
      classes_rep_password() { return computClasses(this.valid_repeated_password); },
  },
  methods: {
    formIsValid() {
      // Validates each field from the form, and returns true if all fields
      // are valid.

      this.user.username = this.user.username.trim();
      const username_length = this.user.username.length
      if (username_length <= 0 || username_length > 150){
        this.valid_username = false
      }
      
      this.user.first_name = this.user.first_name.trim();
      const first_name_length = this.user.first_name.length;
      if (first_name_length <= 0 || first_name_length > 30){
        this.valid_first_name = false;
      }

      this.user.last_name = this.user.last_name.trim();
      const last_name_length = this.user.last_name;
      if (last_name_length <= 0 || last_name_length > 150){
        this.valid_last_name = false;
      }

      if (this.user.password.length <= 0){
        this.valid_password = false;
      }

      // Repeated password confirmation
      if (this.user.password != this.repeated_password){
        this.valid_repeated_password = false;
      }
      
      return this.valid_username &&
        this.valid_first_name &&
        this.valid_last_name &&
        this.valid_password &&
        this.valid_repeated_password
    },
    sendForm(){
      // Sends the information to create a new user, if success, then sends the
      // user to Login, else shows username related problems.

      if (!this.formIsValid())
        return

      axios.post('user/', this.user)
        .then(() => this.$router.push({name: 'Login', query: {new_user: true}}))
        .catch(error => {
          console.log(error);
          const error_data = error.response.data;
          if ('username' in error_data){
            // Show error messages to user.
            this.resetUsernameFeedback();
            for(let feedback of error_data.username)
              this.api_username_feedback += '<p>' + feedback + '</p>';
            this.api_valid_username = false;
          }
        });
    },
    resetUsernameFeedback(){
      this.valid_username = true;
      this.api_valid_username = true;
      this.api_username_feedback = '';
    }
  },
};
</script>

<style scoped>
#login-view {
  background-color: #52a5ff;
  height: 100%;
  width: 100%;
  overflow:auto;
  position: absolute;
}

#form-container {
  margin: 100px auto;
  width: 30rem;
  border-radius: 5px;
  background: white;
  padding: 34px;
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.6);
}

</style>