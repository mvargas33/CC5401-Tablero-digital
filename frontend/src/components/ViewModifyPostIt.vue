<template>
  <div>
    <b-modal
      id="modify-post-it"
      no-close-on-backdrop

      hide-footer
      @shown="$emit('post-it-edit-begin')"
      @hidden="$emit('post-it-edit-end')"
    >

  <b-container class="text-center">
      <b-form
        @submit.prevent="onSubmit"
        id="edit-post-it-form"
      >
        <b-form-input
          v-model="modifiedPostIt.title"
          placeholder="Título"
          class="mb-2"
        />
      </b-form>
  </b-container>
    <b-container class="text-center">
      <b-form
          @submit.prevent="onSubmit"
          id="edit-post-it-form"
        >
        <b-form-textarea
          v-model="modifiedPostIt.description"
          placeholder="Descripción"
          class="description-textarea mb-2"
        />
        <b-form-select v-model="modifiedPostIt.section" required :options="sectionOptions" />
      </b-form>
    </b-container>

      <!-- Botones Guardar cambios -->

      <!-- <hr/>  -->

      <b-container class="text-center pt-3">
        <b-row align-h="start">
          <b-col style="text-align: left">
            <b-button
            type="submit"
            form="edit-post-it-form"
            variant="primary"
            class="mr-auto"
            >
            <font-awesome-icon icon="save" />
            Guardar
            </b-button>
          </b-col>
          <b-col >
            <b-button @click="cancel()">
              <font-awesome-icon icon="window-close" />
              Cancelar</b-button>
          </b-col>
          <b-col style="text-align: right">
            <b-button variant="danger"  @click="$bvModal.hide('modify-post-it');$bvModal.show('confirm-delete')">

            <font-awesome-icon icon="trash" />
            Eliminar
            </b-button>
          </b-col>
        </b-row>
      </b-container>

      <!-- Estado de votación del postit -->
      <div v-if="work_in.is_leader">
        <hr/>

        <p class="mb-4 mt-4 text-center h6 text-secondary">{{ votingMessage }}</p>

        <b-container class="text-center">
          <b-row align-h="start">
            <b-col style="text-align: left">
              <b-button
                class="px-5"
                variant="success"
                @click="vote(1)"
                :disabled="selectedPostIt.voted || !work_in.is_leader"
              >
                <font-awesome-icon icon="thumbs-up" />
              </b-button>
            </b-col>
            <b-col >
                <b-badge
                  class="p-2"
                  :class="stateBadgeConfig.class"
                  v-b-popover.hover.left.v-info="'Estado del post-it.'"
                >
                  {{ stateBadgeConfig.text }}
                </b-badge>

            </b-col>
            <b-col style="text-align: right">
              <b-button
            class="px-5"
            variant="danger"
            @click="vote(0)"
            :disabled="selectedPostIt.voted || !work_in.is_leader"
          >
            <font-awesome-icon icon="thumbs-down" />
          </b-button>
            </b-col>
          </b-row>
        </b-container>
      </div>

      <!-- Resutlado de votación del postit -->

      <hr/>

      <div class="d-flex flex-wrap w-100 text-center justify-content-around pb-3">
        <div class="mt-4">
          <h3 class="text-secondary h4">Stakeholders</h3>
          <p
            class="h5"
            :class="stakeholdersVoteInfo.class"
          >
            {{ stakeholdersVoteInfo.message }}
          </p>
        </div>
        <div class="mt-4">
          <h3 class="text-secondary h4">Desarrolladores</h3>
          <p
            class="h5"
            :class="developersVoteInfo.class"
          >
            {{ developersVoteInfo.message }}
          </p>
        </div>
      </div>
    </b-modal>

    <b-modal
    id="confirm-delete"
    no-close-on-backdrop
    title="Confirmar eliminación"
    >
    <p>¿Está seguro de que desea eliminar el postit?</p>
    <template v-slot:modal-footer>
      <b-button
        @click="$bvModal.hide('confirm-delete');$bvModal.show('modify-post-it');"
      >
        Cancelar
      </b-button>
      <b-button
        variant="primary"
        class="mr-2"
        @click="deletePostit();$bvModal.hide('confirm-delete');"
      >
        Confirmar
      </b-button>

      </template>
    </b-modal>
  </div>
</template>


<script>
import axios from "@/custom_axios.js";

function getVoteInfo(vote){
  // Returns an object with properties message and class according to the
  // vote passed as argument (that should be 0, 1, or 2).

  const index = parseInt(vote);
  const messages = ['Rechazan', 'Aprueban', 'Líder no ha votado'];
  const classes = ['danger', 'success', 'secondary'];
  return {message: messages[index], class: 'text-' + classes[index]};
}

export default {
  name: "ViewModifyPostIt",
  props: {
    selectedPostIt: Object,
    work_in: Object,
    user: Object,
  },
  data() {
    return {
      sectionOptions: [
        { value: null, text: "Selecciona la sección para el post-it" },
        { value: 0, text: "Objetivos" },
        { value: 1, text: "Usuarios" },
        { value: 2, text: "Fuentes" },
        { value: 3, text: "Conceptos" },
        { value: 4, text: "Métricas e Indicadores" },
        { value: 5, text: "Generación de conceptos" },
        { value: 6, text: "Generación de métricas" },
        { value: 7, text: "Visualización, notificación y acción" },
        { value: 8, text: "Entorno" }
      ]
    };
  },
  computed: {
    modifiedPostIt() {
      // This way we don't edit the original till we save it.
      return {...this.selectedPostIt};
    },
    votingMessage() {
      let message = "";
      if (this.work_in.is_leader){
        if(this.selectedPostIt.voted){
          message = "Ya votaste por este post-it.";
        }else{
          message = "¿Estás de acuerdo con este post-it?";
        }
      }else{
        message = "No eres lider de equipo, no puedes votar."
      }       
      return message;
    },
    stakeholdersVoteInfo() {
      return getVoteInfo(this.selectedPostIt.stakeholders_vote);
    },
    developersVoteInfo() {
      return getVoteInfo(this.selectedPostIt.developers_vote);
    },
    stateBadgeConfig() {
      const configs = {
        'O': {
          class: 'badge-open',
          text: 'En votación',
        },
        'A': {
          class: 'badge-approved',
          text: 'Aprobado',
        },
        'R': {
          class: 'badge-rejected',
          text: 'Rechazado',
        }
      };

      // Cuando recién se abre el tablero no hay postits seleccionados, o cuando otro elimina el posit que tenía seleccionado
      if(this.selectedPostIt.status === undefined){
        return configs['R'];
      }else{
        return configs[this.selectedPostIt.status];
      }
    }
  },
  methods: {
    onSubmit() {
      // Send changes to the server and modify the postit info on success.
      //console.log("onSubmit")
      //console.log(this.selectedPostIt)
      //console.log(this.modifiedPostIt)

      axios
        .put(`postit/${this.selectedPostIt.id}/`, this.modifiedPostIt)
        .then(response => {
          response.data.voted = false;
          // Notify that the postit has been changed and hide the modal.
          //console.log("submit response")
          //console.log(response.data)
          this.$emit('postit-changed', this.selectedPostIt, response.data);
          this.$emit('board-changes-saved');
          this.$bvModal.hide("modify-post-it");

        })
        .catch(error => {
          console.log(error);
        });
        
    },
    vote(vote) {
      // Sends vote to the server for the current post-it, vote = 0 means
      // reject and vote = 1 means approve.

      const action = vote == 1? 'approve': 'reject';
      axios
        .get(`postit/${this.selectedPostIt.id}/${action}/`)
        .then(response => {
          console.log("vote")
          console.log(response.data)
          this.$emit('postit-changed', this.selectedPostIt, response.data);
          this.$emit('board-changes-saved');
          //this.$bvModal.hide("info-post-it");
          this.$bvModal.hide("modify-post-it")
        })
        .catch(error => {
          console.log(error);
        });
    },

    deletePostit(){
      axios
        .delete(`postit/${this.selectedPostIt.id}/`)
        .then(response => {
          this.$emit('board-changes-saved');
          this.$emit('reset');
        })
        .catch(error => {
          console.log(error);
        });
    },
    cancel() {
      this.$bvModal.hide("modify-post-it");
    }
  }
};
</script>

<style scoped>
.post-it-description{
  min-height: 10rem;
}

.description-textarea{
  min-height: 8rem;
}

.badge-open{
  background-color: #FDD835;
  color: var(--dark);
}

.badge-approved{
  background-color: var(--success);
  color: white;
}

.badge-rejected{
  background-color: var(--danger);
  color: white;
}
</style>