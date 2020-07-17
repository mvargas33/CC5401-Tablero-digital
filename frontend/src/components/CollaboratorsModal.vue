<template>
  <b-modal
    id="modal-users"
    size="lg"
    hide-footer
    title="Colaboradores"
    header-class="position-relative text-info"
    title-class="collaborators-modal-title"
    body-class="pt-0"
    header-close-variant="info"
    content-class="border-info"
  >
    <b-row class="justify-content-center">
      <div v-for="team in teams" :key="team.name" class="col collab-list mt-4">
        <h5 class="text-center mb-3 text-secondary">{{ team.name }}</h5>
        <ul class="p-0">
          <li v-for="collab in team.collaborators" :key="collab.id" class="collab-list-item">
            <span class="list-item-collab-name">{{ collab.user.full_name }}</span>
            <b-badge v-if="collab.is_leader" variant="info">Líder</b-badge>

            <!-- Si no se es líder o dueño del board, el dropdown no aparece -->
            <b-dropdown
              toggle-class="collab-item-menu"
              right
              :class="{'ml-auto': !collab.is_leader}"
              v-if="iOwnThisBoard || workIn.is_leader"
            >
              <template v-slot:button-content>
                <font-awesome-icon class="menu-icon" icon="ellipsis-v" />
              </template>

              <!-- Opción de cambiar líder sólo visible para líderes de equipo -->
              <b-dropdown-item
                v-if="team.name != 'No asignados' && workIn.is_leader"
                href="#"
                @click="beforeChangeLeader(collab)"
              >Líder de equipo</b-dropdown-item>

              <!-- Opción de eliminar colaboradores sólo para dueño del tablero -->
              <b-dropdown-item v-if="iOwnThisBoard" href="#" @click="beforeDeleteCollab(collab)">Eliminar</b-dropdown-item>
            </b-dropdown>
          </li>
        </ul>
      </div>
    </b-row>

    <b-modal
      id="delete-collab"
      title="Eliminar usuario"
      header-text-variant="danger"
      header-close-variant="danger"
      content-class="border-danger"
    >
      ¿Está seguro que quiere eliminar a
      <strong>{{selectedCollab.full_name}}</strong>
      del proyecto?
      <template v-slot:modal-footer="{cancel}">
        <b-button variant="danger" class="mr-auto" @click="deleteCollab()">Confirmar</b-button>
        <b-button @click="$bvModal.hide('delete-collab')">Cancelar</b-button>
      </template>
    </b-modal>
    <b-modal
      id="change-leader"
      title="Cambiar Líder"
      header-text-variant="danger"
      header-close-variant="danger"
      content-class="border-danger"
    >
      ¿Está seguro que quiere asignar a
      <strong>{{selectedCollabLeader.full_name}}</strong>
      como líder del proyecto? Al hacer esto, usted dejará de ser líder.
      <template
        v-slot:modal-footer="{cancel}"
      >
        <b-button variant="danger" class="mr-auto" @click="changeLeader()">Confirmar</b-button>
        <b-button @click="$bvModal.hide('change-leader')">Cancelar</b-button>
      </template>
    </b-modal>
  </b-modal>
</template>

<script>
import axios from "@/custom_axios.js";

function getTeam(teamType, collaborators) {
  // Gets all the users that belong to teamType ("S" = Stackeholders, "D" =
  // Developers, "U" = Unassigned).

  const team = [];
  collaborators.forEach(collab => {
    if (collab.team === teamType) {
      team.push(collab);
    }
  });
  return team;
}

export default {
  name: "CollaboratorsModal",
  props: {
    collaborators: Array,
    board: Object,
    user: Object,
    isProjectLeader: Boolean,
    workIn: Object,
    iOwnThisBoard: Boolean
  },
  data() {
    return {
      selectedCollab: {},
      selectedCollabLeader: {}
    };
  },
  computed: {
    teams() {
      return [
        {
          name: "Stakeholders",
          collaborators: getTeam("S", this.collaborators)
        },
        {
          name: "Desarrolladores",
          collaborators: getTeam("D", this.collaborators)
        },
        {
          name: "No asignados",
          collaborators: getTeam("U", this.collaborators)
        }
      ];
    }
  },
  methods: {
    beforeDeleteCollab(collab) {
      // Checks that the current user is the owner of the board, if the user is
      // the owner then show the modal for deleting a collaborator, else show
      // a modal with a message that the action cannot be done.
      var message;
      if (this.isProjectLeader && collab.user.id != this.user.id) {
        if (!collab.is_leader) {
          this.asignDelete(collab.user);
          return;
        }
        else{
          message = "No puedes eliminar el líder de un equipo."  
        }
      } else {
        message = this.isProjectLeader
          ? "Eres el dueño del tablero, no puedes eliminarte."
          : "No eres el dueño del tablero, no puedes eliminar colaboradores.";
      }
      const modalConfig = {
        title: "Permiso denegado",
        headerTextVariant: "danger",
        contentClass: "border-danger",
        headerCloseVariant: "danger",
        hideHeaderClose: false,
        okVariant: "danger"
      };
      this.$bvModal.msgBoxOk(message, modalConfig);
    },
    deleteCollab() {
      axios
        .delete(`workin/`, {
          data: { board: this.board, delete_user: this.selectedCollab.id }
        })
        .then(response => {
          this.$bvModal.hide("delete-collab");
          this.$emit("collaborator-deleted", this.selectedCollab);
        })
        .catch(error => {
          console.log(error);
        });
    },
    asignDelete(collab) {
      this.selectedCollab = collab;
      this.$bvModal.show("delete-collab");
    },
    beforeChangeLeader(collab) {
      var message;
      if (this.workIn.is_leader) {
        if (collab.user.id != this.user.id) {
          if (collab.team == this.workIn.team) {
            this.asignLeader(collab);
            return;
          } else {
            message =
              "No puedes elegir de líder alguien que no pertenece a tu equipo.";
          }
        } else {
          message = "Ya eres líder del equipo";
        }
      } else {
        message =
          "No eres el líder de ningun equipo. Solo el líder puede cambiar el líder de su equipo.";
      }
      const modalConfig = {
        title: "Permiso denegado",
        headerTextVariant: "danger",
        contentClass: "border-danger",
        headerCloseVariant: "danger",
        hideHeaderClose: false,
        okVariant: "danger"
      };
      this.$bvModal.msgBoxOk(message, modalConfig);
    },
    asignLeader(collab) {
      this.selectedCollabLeader = collab.user;
      this.$bvModal.show("change-leader");
    },
    changeLeader() {
      axios
        .post(`workin/${this.workIn.id}/pass_leader_privileges/`, {
          user: this.selectedCollabLeader
        })
        .then(response => {
          this.$bvModal.hide("change-leader");
          this.$emit("changed-leader", this.selectedCollabLeader);
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>

<style>
.collaborators-modal-title {
  position: absolute;
  width: 100%;
  text-align: center;
  left: 0;
}

.collab-list {
  min-width: 15rem;
  max-width: 20rem;
}

.collab-list-item {
  list-style: none;
  padding: 0.5rem 1rem;
  border-radius: 3px;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
  display: flex;
  margin-bottom: 0.6rem;
}

.list-item-collab-name {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin-right: 1rem;
}

.collab-list-item .badge {
  font-size: 0.9rem;
  margin-left: auto;
}

.delete-user-button {
  font-size: 8px;
  padding-bottom: 3px;
  padding-top: 3px;
  padding-left: 5px;
  padding-right: 5px;
}

.menu-icon {
  color: var(--secondary);
}

.collab-item-menu {
  background-color: transparent !important;
  border: none !important;
  padding: 0;
  margin-left: 1rem;
  padding: 0 0.2rem;
}

.collab-item-menu::after {
  content: none;
}
</style>