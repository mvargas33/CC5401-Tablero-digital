<template>
  <b-button class="user-icon-large" v-b-tooltip.hover :title="whole_name">
    <p>{{ letters }}</p>
  </b-button>
</template>

<script>
export default {
  name: "UserIconLarge",
  props: ["user_icon"],
  computed: {
    letters(){
      return this.user_icon.name[0] + this.user_icon.last_name[0];
    },
    whole_name(){
      return this.user_icon.name + " " +
              this.user_icon.last_name + " - " +
              this.user_icon.team;
    }
  }
};
</script>

<style>

  .user-icon-large{
    height: 30px;
    width: 30px;
    color: white;
    background-color: #52a5ff;
  }

</style>
