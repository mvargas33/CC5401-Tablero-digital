<template>
  <b-modal @show="isCreateButtonDisabled = false" id="create-post-it" :title="selectedSection.title">
    <b-form @submit="onSubmit" id="create-post-it-form">
      <b-form-input
        v-model="form.title"
        required placeholder="Título"
        class="mb-2"
      />
      <b-form-textarea
        required
        v-model="form.description"
        placeholder="Descripción"
        class="description-textarea"
      />
    </b-form>
    <template v-slot:modal-footer="{cancel}">
      <b-button
        :disabled="isCreateButtonDisabled"
        variant="primary"
        class="mr-auto"
        type="submit"
        form="create-post-it-form"
      >
        Crear
      </b-button>
      <b-button @click="cancel()">Cancelar</b-button>
    </template>
  </b-modal>
</template>

<script>
import axios from "@/custom_axios.js";

export default {
  name: "CreatePostIt",
  props: {
    currentBoard: Object,
    selectedSection: Object,
  },
  data() {
    return {
      form: {
        title: "",
        description: "",
        board: "",
        section: "",
        status: "O"
      },
      isCreateButtonDisabled: false,
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.isCreateButtonDisabled = true; // Disable create button.
      // Add fields to the new postit and send it.
      this.form.board = this.currentBoard.id;
      this.form.section = this.selectedSection.value;
      this.postPostIt(this.form);
    },
    postPostIt(form) {
      axios
        .post("postit/", form)
        .then(response => {
          // Clear form, add new postit and hide modal.
          this.clearForm();
          this.$emit('postit-created', response.data);
          this.$emit('board-changes-saved');
          this.$bvModal.hide('create-post-it');
        })
        .catch(error => {
          console.log(error);
        });
    },
    clearForm(){
      this.form = {
        title: "",
        description: "",
        board: "",
        section: "",
        status: "O"
      };
    },
  }
};
</script>

<style scoped>
.description-textarea{
  min-height: 8rem;
}
</style>