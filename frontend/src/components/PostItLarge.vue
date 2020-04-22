<template>
  <li
    @click="$emit('click')"
    :class="postit.status"
    class="post-it-large p-3 mr-4 mb-4"
  >
    <h3 class="">{{ title }}</h3>
    <p class="post-it-description p-0">{{ description }}</p>
  </li>

</template>

<script>

function textEllipsis(text, length){
  // Cuts text and appends ellipsis if text.length is greater than length.

  if (text.length < length)
    return text;
  return text.slice(0, length) + '...';
}


export default {
  name: "PostItLarge",
  props: ["postit"],
  computed: {
    title(){
      return textEllipsis(this.postit.title, 50);
    },
    description(){
      return textEllipsis(this.postit.description, 140);
    },
  }
};
</script>

<style>
/* Post-it colors where defined in PostItSmall.vue */

.post-it-large{
  cursor: pointer;
  max-width: 20rem;
  min-width: 15rem;
  min-height: 15rem;
  box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.4);
  border-radius: 3px;
  list-style: none;
}

.post-it-description{
  font-size: 1.2rem;
}

</style>