<template>
  <b-navbar id="navbar" type="dark" variant="primary" class="sticky-top">
    <router-link :to="{name: 'Home'}" class="navbar-brand homeIcon mr-3">
      <font-awesome-icon icon="home" />
    </router-link>

    <b-navbar-nav class="ml-0">
      <b-nav-item-dropdown right toggle-class="p-0">
      <template v-slot:button-content>
          <h1 
            id="navbar-board-name"
            class="navbar-text h5 m-0 p-0 mr-1 text-white text-ellip"
          >
            {{ board.name }}
          </h1>
      </template>
        <b-dropdown-item
          @click="$bvModal.show('board-details-modal')"
        >
          Detalles
        </b-dropdown-item>
        <b-dropdown-item
          @click="beforeDeleteBoard"
        >
          Eliminar tablero
        </b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>

    <span class="navbar-text ml-3 saved-message text-ellip" :class="{ active: savedChanges }">
      Cambios guardados
      <b-spinner small variant="light" type="grow" label="Spinning" style="vertical-align: baseline"></b-spinner>
    </span>

    <b-badge
      class="user-info ml-auto"
      variant="info"
      v-b-popover.hover.top.v-info="'Perteneces a este equipo.'"
    >
      {{ team }}
    </b-badge>
    <b-badge
      v-if="workIn.is_leader"
      class="user-info ml-2"
      variant="info"
      v-b-popover.hover.top.v-info="'Eres líder de equipo y tienes permiso para votar.'"
    >
      Líder
    </b-badge>
    <b-badge
      v-if="isProjectLeader"
      class="user-info ml-2"
      variant="info"
      v-b-popover.hover.top.v-info="'Eres el dueño del tablero. Puedes eliminar el tablero y a sus colaboradores.'"
    >
      Dueño
    </b-badge>

    <button v-b-modal.modal-users type="button" class="button-circle mx-4">
      <font-awesome-icon icon="users" />
    </button>
    <button v-b-modal.modal-add-collab class="button-circle">
      <font-awesome-icon icon="user-plus" />
    </button>

    <b-navbar-nav class="ml-3">
      <b-nav-item-dropdown right :text="user.full_name" text-class="text-white">
        <template v-slot:button-content>
            <span class="text-white mr-1">{{ user.full_name }}</span>
          </template>
        <b-dropdown-item :to="{name: 'Home'}">Mis tableros</b-dropdown-item>
        <b-dropdown-item @click="$router.logout()">Salir</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>

    <collaborators-modal 
      :collaborators="collaborators"
      :board="board"
      :user="user"
      :is-project-leader="isProjectLeader"
      :workIn="workIn"
      @collaborator-deleted="collaboratorDeleted"
      @changed-leader="changedLeader"

    />

    <b-modal
      id="delete-board"
      title="Eliminar tablero"
      header-text-variant="danger"
      header-close-variant="danger"
      content-class="border-danger"
    >
      ¿Está seguro que quiere eliminar el tablero <strong>{{board.name}}</strong>?
      Al realizar esto perderá todos los datos del tablero.
      <template v-slot:modal-footer="{cancel}">
        <b-button variant="danger" class="mr-auto" @click="deleteBoard()">Confirmar</b-button>
        <b-button class="" @click="$bvModal.hide('delete-board')">Cancelar</b-button>
      </template>
    </b-modal>

    <new-collaborator-form-modal
      @new-collaborator="addCollaborator"
      id="modal-add-collab"
      :board="board"
    />

    <board-details-modal
      :board="board"
      :owner="projectLeader"
    />
  </b-navbar>
</template>


<script>
import axios from "@/custom_axios.js";
import NewCollaboratorFormModal from "@/components/NewCollaboratorFormModal.vue";
import CollaboratorsModal from "@/components/CollaboratorsModal.vue";
import BoardDetailsModal from "@/components/BoardDetailsModal.vue";


export default {
  name: "NavBar",
  components: {
    NewCollaboratorFormModal,
    CollaboratorsModal,
    BoardDetailsModal,
  },
  props: {
    user: Object,
    board: Object,
    workIn: Object,
    collaborators: Array,
    savedChanges: Boolean
  },
  data() {
    return { selectedCollab: "" };
  },
  computed: {
    team() {
      const teams = {
        'S': 'Stakeholder',
        'D': 'Desarrollador',
        'U': 'Sin equipo',
      };
      return teams[this.workIn.team]; 
    },
    isProjectLeader() {
      return this.board.project_leader == this.user.id;
    },
    projectLeader() {
      const leader = this.collaborators.filter(collab => collab.user.id == this.board.project_leader)[0];
      return leader == undefined? {} : leader.user;
    },
  },
  methods: {
    addCollaborator(collaborator) {
      this.$emit("new-collaborator", collaborator);
    },
    beforeDeleteBoard() {
      // Checks that the current user is the owner of the board, if the user
      // is the owner then shows the modal for deleting the board, else shows
      // a modal with a message that the board cannot be deleted.
      
      if (this.isProjectLeader){
        this.$bvModal.show('delete-board');
      }else{
        const message = 'No eres el dueño del tablero, no puedes eliminarlo.'
        const modalConfig = {
          title: 'Permiso denegado',
          headerTextVariant: 'danger',
          contentClass: 'border-danger',
          headerCloseVariant: 'danger',
          hideHeaderClose: false,
          okVariant: 'danger',
        };
        this.$bvModal.msgBoxOk(message, modalConfig);
      }
    },
    deleteBoard() {
      axios
        .delete(`board/`, { data: this.board })
        .then(response => {
          this.$bvModal.hide("delete-board");
          this.$router.push("/");
        })
        .catch(error => {
          console.log(error);
        });
    },
    collaboratorDeleted(collaborator){
      this.$emit('collaborator-deleted', collaborator);
    },
    changedLeader(collaborator){
      console.log("cambiando lider");
      this.$emit('changed-leader', collaborator);
    }
  }
};
</script>

<style scoped>
.button-circle {
  font-size: 1.2rem;
  height: 2.7rem;
  width: 2.7rem;
  background: white;
  color: #007bff;
  border-radius: 3rem;
  padding: 0;
  border: 2px solid #d4d7db;
  outline: none;
  flex-shrink: 0;
}

#navbar-board-name{
  max-width: 15rem;
  vertical-align: bottom;
}

.text-ellip {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.group-text {
  margin-left: 10px;
  width: 40vw;
}

#navbar {
  box-shadow: 0 3px 3px rgba(0, 0, 0, 0.3);
  z-index: 500;
}

.homeIcon {
  opacity: 0.5;
  -webkit-transition: opacity 0.2s ease-in-out;
  -moz-transition: opacity 0.2s ease-in-out;
  -ms-transition: opacity 0.2s ease-in-out;
  -o-transition: opacity 0.2s ease-in-out;
  transition: opacity 0.2s ease-in-out;
}

.homeIcon:hover {
  opacity: 1;
}

.saved-message {
  vertical-align: bottom;
  opacity: 0;
  transition: opacity 0.4s;
}

.saved-message.active {
  opacity: 1;
}

.user-info{
  font-size: 1.2rem;
}
</style>