<template>
  <b-modal @hide="success = false" :id="id" title="Añadir colaborador">
    <b-form id="new-collab-form" @submit.prevent="addCollaborator">
      <b-form-input
        v-model="user_email"
        type="email"
        placeholder="Ingrese un correo electrónico"
        @input="error_message = ''; success = false;"
        required
      />
      <small v-if="error_message != ''" class="form-text text-danger mb-0 mt-2">
        {{ error_message }}
      </small>
      <small v-if="success" class="form-text text-success mb-0 mt-2">
        El usuario ha sido agregado al tablero.
      </small>
      <small class="form-text text-secondary">El usuario podrá elegir su equipo al entrar al tablero.</small>
    </b-form>
    <template v-slot:modal-footer="{cancel}">
      <button type="submit" form="new-collab-form" class="btn btn-primary mr-auto">Agregar</button>
      <button type="button" class="btn btn-secondary" @click="cancel()">Cancelar</button>
    </template>
  </b-modal>
</template>

<script>
import axios from '@/custom_axios.js';

export default {
  name: "NewCollaboratorFormModal",
  props: {
    id: String, // Document id of for the modal
    board: Object // The current board
  },
  data() {
    return {
      user_email: '',
      error_message: '',
      success: false,
    };
  },
  methods: {
    addCollaborator(){
      // Tries to add the new user to the board, if success, emits a
      // new-collaborator event with the workIn data as extra argument,
      // else, shows the errors to the user.

      axios.post(`board/${this.board.id}/add_collaborator/`, {
        email: this.user_email
      }).then(response => {
        if (response.status == 201){
          // The user was added to the board.
          this.user_email = '';
          this.error_message = '';
          const collaborator = response.data.user;
          collaborator.full_name = collaborator.first_name + ' ' + collaborator.last_name;
          this.$emit('new-collaborator', response.data);
          this.success = true;
        }else{
          // The user already works in this board.
          console.log(response.data);
          this.error_message = response.data.detail;
        }
      }).catch(error => {
        // There is no user for that email, or another error occurred.
        console.log(error);
        this.error_message = error.response.data.detail;
      });
    },
  }
};
</script>

<style scoped>

</style>