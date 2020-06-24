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
      <b-button type="submit" form="new-collab-form" variant="primary" class="btn btn-primary mr-auto">Agregar</b-button>
    </b-form>

    
    <template v-slot:modal-footer>
      <div class="container">
        <div class="row">
          <div class="col"> <h5> Enlace de invitación </h5> </div>
          <div class="col"> <toggle-button @change="enableLink" :value="show_link " color="#007bff" :width=95 :labels="{checked: 'Deshabilitar', unchecked: 'Habilitar'}"/> </div>
        </div>

        <div v-if="show_link" class="row" id="invitationLink">
          <div class="col"> <p class="m-0 p-3">{{ invitation_link }}</p> </div>
          <div class="col">
              <b-button
              @click="newLink"
              variant="primary"
              class="mr-2"
              >
              Generar nuevo
              </b-button>
          </div>
        </div>
      </div>

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
      show_link: false,
      invitation_link: '',
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

    enableLink(){
      if(!this.show_link){
      axios      
        .post(`board/${this.board.id}/generate_link/`)
        .then(response => {
          this.invitation_link = response.data.detail;
        })
        .catch(error => {
          console.log(error);
        })
      }
      else{
        axios
          .post(`board/${this.board.id}/disable_link/`)
          .then(response =>{
            this.invitation_link = '';
          })
          .catch(error => {
            console.log(error)
          })
      }
      this.show_link = !this.show_link;
    },

    newLink(){
      axios      
        .post(`board/${this.board.id}/generate_link/`)
        .then(response => {
          this.invitation_link = response.data.detail;
        })
        .catch(error => {
          console.log(error);
        })
    },
  }
};
</script>

<style scoped>

</style>