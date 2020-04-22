<template>
  <div>
    <nav-bar-home :user="this.$store.state.user" />
    <div class="container pt-4">
      <h3 class="m-0 text-secondary">Mis Tableros</h3>
      <hr class="mt-1 mb-4" />

      <div v-if="boards.length==0">
        <h4 class="text-center text-muted mt-5">No tienes tableros, añade uno</h4>
        <b-button
          v-b-modal.new-board-modal
          class="rounded-circle align-self-center mx-auto d-block mt-4 new-project-button"
          variant="primary"
        >
          <font-awesome-icon icon="plus" />
        </b-button>
      </div>

      <b-card-group v-else deck class="flex-row flex-wrap">
        <div
          v-for="board in boards"
          :key="board.id"
          class="card mb-4 project-card"
          @click="$router.push({ name: 'Board', params: { boardId: board.id } })"
        >
          <div class="card-body d-flex p-3">
            <font-awesome-icon
              :style="{fontSize: '1.5rem'}"
              class="mr-3 align-self-end text-primary"
              icon="sticky-note"
            />
            <h6 class="card-title m-0 text-ellip">{{ board.name }}</h6>
          </div>
        </div>
        <div class="card border-0 mb-4 d-flex justify-content-center add-card-button-container">
          <b-button
            v-b-modal.new-board-modal
            class="rounded-circle align-self-center new-project-button"
            variant="primary"
          >
            <font-awesome-icon icon="plus" />
          </b-button>
        </div>
      </b-card-group>

      <new-board-form-modal id="new-board-modal" :user="this.$store.state.user" />
    </div>
  </div>
</template>

<script>
import NewBoardFormModal from "@/components/NewBoardFormModal.vue";
import NavBarHome from "@/components/NavBarHome.vue";
import axios from "@/custom_axios.js";

export default {
  name: "Home",
  components: {
    NavBarHome,
    NewBoardFormModal
  },
  data() {
    return {
      boards: [],
      updateInterval: 0, // Interval identifier for updating boards
    };
  },
  methods: {
    getBoards() {
    // Get user boards:
    axios
      .get(`/board/`)
      .then(res => (this.boards = res.data))
      .catch(err => console.log(err));
    }
  },
  created() {
    this.getBoards();
    // Clear updateInterval at beforeDestroy().
    this.updateInterval = setInterval(() =>{
      this.getBoards();
    }, 1000 * 10); // Update every 10 seconds
  },
  beforeDestroy() {
    // Clears the update interval.

    clearInterval(this.updateInterval);
  },
};
</script>

<style scoped>
.project-card,
.add-card-button-container {
  width: 14rem;
  margin-right: 15px;
  margin-left: 15px;
  flex: 1 1 auto;
  cursor: pointer;
}

.project-card,
.new-project-button{
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

@media (min-width: 992px) {
  .project-card,
  .add-card-button-container {
    max-width: 290px;
  }
}

@media (min-width: 1200px) {
  .project-card,
  .add-card-button-container {
    max-width: 255px;
  }
}

.text-ellip {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.new-project-button {
  width: 3rem;
  height: 3rem;
}
</style>
