<template>
  <li
    class="post-it-small"
    :class="postit.status"
    @click="$emit('post-it-selected');"
  >
  {{text}}
  </li>
</template>

<script>
export default {
  name: "PostItSmall",
  props: ["postit"],
  computed: {
    text(){
      // Text to show inside the postit.

      if (this.postit.title.length < 40)
        return this.postit.title;
      return this.postit.title.slice(0, 40) + '...';
    }
  },
};
</script>

<style>
.post-it-small {
  position: relative;
  list-style: none;
  color: white;
  text-align: center;
  max-width: 10rem;
  max-height: 6rem;
  margin-right: 1rem;
  margin-bottom: 1.2rem;
  padding: 0.7rem 1rem;
  border-radius: 2px;
  box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.5);
  cursor: pointer;
  transition-property: transform, filter;
  transition-duration:  0.15s;
  filter: brightness(1);
  transform: rotate(2deg);
  z-index: 0;
  font-weight: 500;
}

.post-it-small:nth-child(2n){
  transform: rotate(-2deg);
}

.post-it-small:nth-child(3n){
  transform: rotate(2deg);
}

.post-it-small:nth-child(4n-1){
  transform: rotate(-3deg);
}

.post-it-small:nth-child(8n-1){
  transform: rotate(3deg);
}

.post-it-small:hover{
  transform: scale(1.25);
  filter: brightness(1.1);
  z-index: 100;
}


/* Colors for the different states of the post-its */

.O{ /* Open */
  background-color: #FDD835;
  color: var(--dark);
}

.A{ /* Approved */
  background-color: var(--green);
  color: white;
}

.R{ /* Rejected */
  background-color:var(--red);
  color: white;
}
</style>