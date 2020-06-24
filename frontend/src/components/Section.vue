<template>
  <div class="section" :class="section.cssClass">
    <!-- Título -->
    <h1 
      :id="'section-title-' + section.value"
      class="section-title text-secondary d-inline-block"
    >
      <font-awesome-icon :icon="section.icon" />
        {{section.title}}

      <section-info-pop-over
        :target="'section-title-' + section.value"
        :section="section"
       />
    </h1>
    <!-- Container de todos los postits -->
    <ul class="post-it-container">
      <post-it-small
        v-for="postit in section.postits"
        :key="postit.id"
        :postit="postit"
        @post-it-selected="$emit('post-it-selected', postit)"
      />
    </ul>
    <!-- Botón de Zoom IN -->
    <b-button
      @click="$emit('zoom-in-section')"
      class="zoom-section rounded-circle"
    >
      <font-awesome-icon icon="expand-arrows-alt"></font-awesome-icon>
    </b-button>
    <!-- Botón de crear post-it -->
    <b-button
     
      @click="$emit('create-post-it')"
      class="add-post-it rounded-circle"
    >
      <font-awesome-icon icon="plus"></font-awesome-icon>
    </b-button>
  </div>
</template>

<script>
import PostItSmall from "../components/PostItSmall.vue";
import SectionInfoPopOver from '@/components/SectionInfoPopOver.vue';


export default {
  name: "Section",
  components: {
    PostItSmall,
    SectionInfoPopOver,
  },
  props: ["section"],
};
</script>

<style>

.section {
  background-color: #fff;
  padding-left: 0.5rem;
  padding-bottom: 1rem;
  position: relative;
}

.grid-goals {
  grid-column: 1 / span 8;
  grid-row: 1;
}

.grid-users {
  grid-column: 9 / span 8;
  grid-row: 1;
}

.grid-sources {
  grid-column: 1 / span 5;
  grid-row: 2;
}

.grid-concepts {
  grid-column: 6 / span 6;
  grid-row: 2;
}

.grid-indicators {
  grid-column: 12 / span 5;
  grid-row: 2;
}

.grid-concept-gen {
  grid-column: 1 / span 6;
  grid-row: 3;
}

.grid-indicator-gen {
  grid-column: 7 / span 6;
  grid-row: 3;
}

.grid-visualization {
  grid-column: 13 / span 4;
  grid-row: 3;
}

.grid-environment {
  grid-column: 1 / span 16;
  grid-row: 4;
}

.post-it-container {
  width: 100%;
  padding-left: 0.5rem;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.grid-users,
.grid-goals,
.grid-environment {
  min-height: 25vh;
}

.grid-sources,
.grid-concepts,
.grid-indicators,
.grid-concept-gen,
.grid-indicator-gen,
.grid-visualization {
  min-height: 50vh;
}

.section-title {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  font-size: 1.3rem;
  margin: 1.2rem 0 1rem 0.5rem;
  font-weight: 600;
  cursor: pointer;
}

.add-post-it {
  position: absolute;
  right: 0;
  bottom: 0.25rem;
  margin: 10px;
  margin-right: calc(0.3rem + 60px);
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}

.zoom-section {
  position: absolute;
  margin: 10px;
  right: 0.3rem;
  bottom: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}

.section:hover .add-post-it {
  opacity: 0.5;
}
.section:hover .zoom-section {
  opacity: 0.5;
}

.section .add-post-it:hover {
  opacity: 1;
}

.section .zoom-section:hover {
  opacity: 1;
}

</style>