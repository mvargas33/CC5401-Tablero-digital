<template>
  <div>
    <!--  Navbar -->
    <nav-bar-project
      @new-collaborator="addCollaborator"
      @collaborator-deleted="deleteCollaborator"
      @changed-leader="updateLeader"
      :user="user"
      :work-in="workIn"
      :collaborators="collaborators"
      :board="board"
      :saved-changes="savedChangesCounter > 0"
    />

    <!-- Normal board view -->
    <div v-show="!isZoomedIn" class="grid-container">
      <Section
        v-for="section in sections"
        :key="section.title"
        v-model="selectedPostIt"
        :section="section"
        @zoom-in-section="currentSection = section; isZoomedIn = true;"
        @create-post-it="newPostIt(section)"
        @post-it-selected="selectPostIt"
      />
    </div>

    <!-- Zommed section view -->
    <div v-show="isZoomedIn">
      <h2
        id="zoom-section-title"
        class="d-inline-block text-secondary font-weight-bolder mx-4 mb-0 mt-4"
      >
        <font-awesome-icon :icon="currentSection.icon" />
        {{ currentSection.title }}
        <section-info-pop-over target="zoom-section-title" :section="currentSection" />
      </h2>
      <hr class="mx-4 mt-2 mb-4" />
      <p v-if="currentSection.postits.length == 0" class="h3 text-secondary no-post-it-text">
        <span>No hay post-its en esta sección.</span>
      </p>
      <ul v-else class="d-flex flex-wrap px-4 align-items-center">
        <post-it-large
          v-for="postit in currentSection.postits"
          :key="postit.id"
          @click="selectPostIt(postit)"
          :postit="postit"
        />
      </ul>
      <!-- Zoom out button -->
      <b-button
        class="zoom-section-button rounded-circle"
        style="right: 20px;"
        @click="isZoomedIn = false"
      >
        <font-awesome-icon icon="compress-arrows-alt" />
      </b-button>
      <!-- Create postit -->
      <b-button
        @click="newPostIt(currentSection)"
        class="zoom-section-button rounded-circle"
        style="right: 130px;"
      >
        <font-awesome-icon icon="plus" />
      </b-button>
    </div>

    <!-- Hidden modal de modificar post-it/ Se activa con eventos post-it-edit-begin/post-it-edit-end -->
    <!-- <create-post-it
      @postit-created="addPostIt"
      :current-board="board"
      :selected-section="currentSection"
      @board-changes-saved="incrementSavedChanges"
    /> -->
    <view-modify-post-it
      :selected-post-it="selectedPostIt"
      @post-it-edit-begin="isEditingPostIt = true"
      @post-it-edit-end="isEditingPostIt = false"
      @postit-changed="changePostit"
      @board-changes-saved="incrementSavedChanges"
      :work_in="workIn"
      :user="user"
    />
    <select-team-modal id="select-team-modal" :work-in="workIn" />
  </div>
</template>
<script>
import axios from "@/custom_axios.js";
import NavBarProject from "../components/NavBarProject.vue";
import Section from "../components/Section.vue";
import ViewModifyPostIt from "../components/ViewModifyPostIt.vue";
//import CreatePostIt from "../components/CreatePostIt.vue";
import PostItLarge from "../components/PostItLarge.vue";
import SelectTeamModal from "@/components/SelectTeamModal.vue";
import SectionInfoPopOver from "@/components/SectionInfoPopOver.vue";
import { mapState } from "vuex";

export default {
  name: "Board",
  components: {
    NavBarProject,
    Section,
    ViewModifyPostIt,
    //CreatePostIt,
    PostItLarge,
    SelectTeamModal,
    SectionInfoPopOver
  },
  data() {
    return {
      sections: [
        {
          title: "Objetivos",
          cssClass: "grid-goals",
          icon: "flag",
          postits: [],
          value: 0,
          description: `Se busca poder definir el objetivo de este canvas de procesamiento
          de datos con el fin de identificar el propósito fundamental y donde
          se pueda exponer de forma clara y precisa el resultado final que se
          pretende alcanzar con este trabajo.`
        },
        {
          title: "Usuarios",
          cssClass: "grid-users",
          icon: "users",
          postits: [],
          value: 1,
          description: `Los usuarios son las personas claves que harán uso de los indicadores
          o modelos que se generen por medio del procesamiento de los datos. Su
          perfilamiento es importante para poder comprender si las ideas
          plasmadas en este canvas permiten dar respuesta a las necesidades de
          estos.`
        },
        {
          title: "Fuentes",
          cssClass: "grid-sources",
          icon: "database",
          postits: [],
          value: 2,
          description: `Las fuentes alimentan a los conceptos, entender el tipo, el volumen,
          la frecuencia de actualización entre otros aspectos es de vital
          importancia para poder comprender los desafíos que existen a la hora
          de extraer, transformar y cargar la información de las fuentes en los
          conceptos.`
        },
        {
          title: "Conceptos",
          cssClass: "grid-concepts",
          icon: "lightbulb",
          postits: [],
          value: 3,
          description: `Los conceptos son las unidades más básicas de toda forma de
          conocimiento sobre el negocio, en particular construcciones, por
          medio de las cuales comprendemos la naturaleza y funcionamiento de
          un negocio en particular.`
        },
        {
          title: "Métricas e Indicadores",
          cssClass: "grid-indicators ",
          icon: "chart-bar",
          postits: [],
          value: 4,
          description: `Las métricas, a veces llamadas métricas de negocio, son medidas
          cuantificables que se utilizan para medir el rendimiento o el
          progreso de un negocio. Para crear una métrica, se toman datos de los
          conceptos (es decir, es información que se actualiza constantemente
          con nueva información) y se monitorean estos para seguir el progreso
          hacia el objetivo de negocio.`
        },
        {
          title: "Generación de Conceptos",
          cssClass: "grid-concept-gen",
          icon: "brain",
          postits: [],
          value: 5,
          description: `Mover la información desde las fuentes a los conceptos o la
          generación de nuevos conceptos a través de la unión o el procesamiento
          de conceptos nuevos o existentes necesita de un conjunto de
          actividades, por ejemplo actividades de extracción, de transformación,
          de procesamiento complejo y de carga, las cuales orquestadas permitan
          tener toda la información necesaria para generar las métricas e
          indicadores necesarios para el negocio.`
        },
        {
          title: "Generación de Métricas",
          cssClass: "grid-indicator-gen",
          icon: "ruler",
          postits: [],
          value: 6,
          description: `Existen diferentes actividades que se realizan para generar métricas
          desde la información que se tiene de uno o varios conceptos de
          negocio, poder identificar esas actividades, fórmulas u operaciones
          es fundamental con el fin de enteder si se tiene toda la información
          necesaria o si se dispone de la frecuencia de los datos correcta para
          su generación.`
        },
        {
          title: "Visualización, notificación y acción",
          cssClass: "grid-visualization",
          icon: "desktop",
          postits: [],
          value: 7,
          description: `Tanto una métrica como un indicador pueden necesitar de una
          visualización como un gráfico de barras, una alerta visual o sonora,
          o de una acción como el envío de un correo electrónico.
          Adicionalmente las métricas e indicadores pueden ser interactivos,
          permitiendo a los operadores del negocio interactuar con estos, o
          estáticos como un informe puntual.`
        },
        {
          title: "Entorno",
          cssClass: "grid-environment",
          icon: "mountain",
          postits: [],
          value: 8,
          description: `Al procesar los datos para generar valor para el negocio es
          necesario también tomar en cuenta aspectos del entorno que pueden
          impactar en el procesamiento. Los aspectos del entorno relevante
          están relacionados con diferentes restricciones tecnológicas,
          aspectos de seguridad, entre otros factores`
        }
      ],
      board: {}, // The current board
      selectedPostIt: {}, // Postit currently selected by the user
      isEditingPostIt: false, // True if the user is editing selectedPostIt
      currentSection: {}, // Current section selected by the user
      isZoomedIn: false, // True if currentSection is zoomed in
      collaborators: [], // A list of workIn relations for the current board
      workIn: {}, // The workIn relation for the current user and board
      savedChangesCounter: 0, // Number of changes saved in the last 3 seconds
      updateInterval: 0 // Identifier used in created()
    };
  },
  computed: {
    ...mapState(["user"])
  },
  created() {
    // Gets board, users and postits.

    this.currentSection = this.sections[0]; // Set to avoid errors
    this.getBoard();
    this.getBoardUsers().then(() => {
      this.getPostIts();
      // Clear updateInterval at beforeDestroy().
      this.updateInterval = setInterval(() => {
        this.getBoardUsers();
        this.getPostIts();
      }, 1000 * 10); // Update every 10 seconds
    });
  },
  beforeDestroy() {
    // Clears the update interval.

    clearInterval(this.updateInterval);
  },
  methods: {
    getBoard() {
      // Gets the info for the current board.

      axios
        .get(`board/${this.$route.params.boardId}/`)
        .then(response => {
          this.board = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    getPostIts() {
      // Gets postits for the current board and adds them to the corresponding
      // sections.

      axios
        .get(`postit/?board=${this.$route.params.boardId}`)
        .then(response => {
          // Empty sections before the update.
          for (let section of this.sections) {
            section.postits = [];
          }

          for (let postit of response.data) {
            this.addPostIt(postit);
          }
        })
        .catch(error => {
          console.log(error);
        });
    },
    getBoardUsers() {
      // Gets collaborators for this board. And checks if the current user
      // has a team. Returns a resolved promise if success, else a rejected
      // promise.

      return axios
        .get(`workin/?board=${this.$route.params.boardId}`)
        .then(res => {
          this.collaborators = []; // Empty collaborators before the update
          res.data.forEach(workIn => {
            const user = workIn.user;
            user.full_name = user.first_name + " " + user.last_name;
            if (this.user.id == user.id) {
              this.workIn = workIn;
              // Check if current user has team.
              if (workIn.team == "U") {
                this.$bvModal.show("select-team-modal");
              }
            }
          });
          this.collaborators = res.data;
          return Promise.resolve();
        })
        .catch(err => {
          console.log(err);
          return Promise.reject();
        });
    },
    addCollaborator(collaborator) {
      this.collaborators.push(collaborator);
    },
    deleteCollaborator(collaborator) {
      for (let i = 0; i < this.collaborators.length; i++) {
        if (this.collaborators[i].user == collaborator) {
          this.collaborators.splice(i, 1);
          break;
        }
      }
    },
    updateLeader(collaborator) {
      for (let i = 0; i < this.collaborators.length; i++) {
        if (this.collaborators[i].user == collaborator) {
          this.collaborators[i].is_leader = true;
        } 
        if (this.collaborators[i].user.id == this.user.id){
          this.collaborators[i].is_leader = false;
        }
      }
    },
    addPostIt(postit) {
      // Adds a postit to its corresponding section. If the user is editing the
      // selectedPostit with the same id, then adds selectedPostit instead.

      if (this.selectedPostIt.id == postit.id) {
        if (this.isEditingPostIt) {
          // Don't replace if the user is editing.
          postit = this.selectedPostIt;
        } else {
          this.selectedPostIt = postit;
        }
      }
      const section = postit.section;
      this.sections[section].postits.push(postit);
      this.setVoted(postit);
    },
    changePostit(oldPostit, newPostit) {
      // Changes a postit, moves it to another section if necessary.

      this.setVoted(newPostit);
      const section = this.sections[oldPostit.section];
      const index = section.postits.indexOf(oldPostit);
      if (oldPostit.section == newPostit.section) {
        this.$set(section.postits, index, newPostit);
      } else {
        // Move postit to the new section.
        section.postits.splice(index, 1);
        const newSection = this.sections[newPostit.section];
        newSection.postits.push(newPostit);
      }
    },
    incrementSavedChanges() {
      // Increments savedChangesCounter by 1 and sets a timeout to decrement
      // it by 1 after 3 seconds. This allows to show the user a "saved"
      // message for at least 3 seconds.

      this.savedChangesCounter++;
      setTimeout(() => this.savedChangesCounter--, 3000);
    },
    selectPostIt(postit) {
      // Set the current selected postit and show the postit modal.

      this.selectedPostIt = postit;
      this.$bvModal.show("modify-post-it");
    },
    setVoted(postit) {
      // Sets postit.voted to true if the user is a team leader and has voted,
      // else sets it to false. If the user is not a team leader, the
      // postit.voted is not set.

      if (this.workIn.is_leader) {
        if (this.workIn.team == "S")
          postit.voted = postit.stakeholders_vote != 2;
        else if (this.workIn.team == "D")
          postit.voted = postit.developers_vote != 2;
      }
    },
    newPostIt(seccion){
      this.currentSection = seccion;
      // PostIt vacío
      var new_postit = {
        title: "",
        description: "",
        board: this.board.id,
        section: this.currentSection.value,
        status: "O"
      }
      // Push a endpoint en el back
      axios
        .post("postit/", new_postit)
        .then(response => {
          console.log(response)
          this.addPostIt(response.data);      // Poner el post-it en la sección
          this.incrementSavedChanges();       // ¿? Save message ¿?
          this.selectPostIt(response.data);
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
};
</script>
 
 <style>
/* General board view */
.grid-container {
  display: grid;
  grid-template-columns: repeat(16, 1fr);
  grid-gap: 3px;
  padding: 0;
  background-color: #dcdfe0;
}

/* Zoomed-in section */
#zoom-section-title {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  cursor: pointer;
}

.zoom-section-button {
  position: fixed;
  bottom: 20px;
  opacity: 0.5;
  height: 5rem;
  width: 5rem;
  font-size: 2.5rem;
  line-height: 2.5rem;
  transition: opacity 0.2s ease-in-out;
}

.zoom-section-button:hover {
  opacity: 1;
}

.no-post-it-text {
  position: absolute;
  top: 0;
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: -1;
}
</style>

