<template>
  <b-modal :id="id" title="Nuevo tablero">
    <b-form id="new-board-form" @submit.prevent="submitForm">
      <b-form-input
        v-model="name"
        class="mb-3"
        type="text"
        placeholder="Título"
        required
      />
      <b-form-textarea
        v-model="description"
        placeholder="Descripción"
        style="min-height: 8rem"
        required
      />
    </b-form>
    <template v-slot:modal-footer="{cancel}">
      <button type="submit" form="new-board-form" class="btn btn-primary mr-auto">Crear</button>
      <button type="button" class="btn btn-secondary" @click="cancel()">Cancelar</button>
    </template>
  </b-modal>
</template>

<script>
import axios from "@/custom_axios.js";

export default {
  name: "NewBoardFormModal",
  props: {
    id: String,
    userId: Number
  },
  data() {
    return {
      name: "",
      description: ""
    };
  },
  methods: {
    submitForm() {
      //Create board:
      axios
        .post("board/", {
          name: this.name,
          description: this.description
        })
        .then(res => {
          const newBoard = res.data;
          this.$router.push({
            name: "Board",
            params: { boardId: newBoard.id }
          });
        })
        .catch(err => console.log(err));
    }
  }
};
</script>