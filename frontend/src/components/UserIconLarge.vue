<template>
  <li
          class="user-icon-large"
  >
    <h3 class="">{{ letter }}</h3>
  </li>

</template>

<script>
export default {
  name: "UserIconLarge",
  props: ["user_icon"],
  computed: {
    letter(){
      return this.user_icon.name[0];
    }
  }
};
</script>

<style>
  /* Post-it colors where defined in PostItSmall.vue */

  .user-icon-large{
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

</style>
