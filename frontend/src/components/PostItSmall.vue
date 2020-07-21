<template>
  <li
    class="post-it-small"
    :class="postit.status"
    @click="$emit('post-it-selected')"
  >
  {{text}}
  <ul class="concurrent-container">
      <user-icon-large
              v-for="user in usuarios_postit"
              class="concurrent-container rounded-circle"
              :user_icon="user"
              :tipo="small"
              :key="user.id"
      />
    </ul>
  </li>

</template>

<script>
  import UserIconLarge from "./UserIconLarge";

export default {
  name: "PostItSmall",
  props: ["postit"],
  components: {
    UserIconLarge
  },
  data() {
    return { small: "small" };
  },
  computed: {
    text(){
      // Text to show inside the postit.
      const as_words = this.postit.title.split(" ");
      let short_title = "";
      let pos;
      let word;
      for (pos in as_words) {
        word = as_words[pos];
        if (word.length >= 15){
          short_title += word.slice(0, 15) + "- ";
          let remaining_word = word.slice(15, word.length);
          while (remaining_word.length >= 15) {
            short_title += remaining_word.slice(0, 15) + "- ";
            remaining_word = remaining_word.slice(15, remaining_word.length);
          }
          short_title += remaining_word + " ";
        }
        else {
          short_title += word + " ";
        }
      }
      short_title = short_title.slice(0, short_title.length - 1);
      if (short_title.length < 40)
        return short_title;
      return short_title.slice(0, 40) + '...';
    },
    usuarios_postit(){
      const test = [
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 0,'name': "Alexis", 'last_name': 'Garmendia', 'team':'Stakeholders'},
        {'id': 1,'name': "Bárbara", 'last_name': 'Venegas', 'team':'Developer'}
        ]
      console.log(test)
      return test; // TODO CALL VUEX
    }
  },
  methods: {
    positSmallStyle(){ // TODO BYNAMIC SIZE BASED ON ACTIUVE USERES IN POSTIT
      return ``
    }
  }
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