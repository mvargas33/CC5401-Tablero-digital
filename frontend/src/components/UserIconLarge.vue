<template>
  <b-button :style="iconClass(tipo)" v-b-tooltip.hover :title="whole_name">
    <p :style="textClass(tipo)">{{ letters }}</p>
  </b-button>
</template>

<script>
export default {
  name: "UserIconLarge",
  props: ["user_icon","tipo"],
  computed: {
    letters(){
      return this.user_icon.name[0] + this.user_icon.last_name[0];
    },
    whole_name(){
      return this.user_icon.name + " " +
              this.user_icon.last_name + " - " +
              this.user_icon.team;
    },
    
  },
  methods: {
    iconClass(tipe){
        console.log(tipe)
        var randomColor = "#"+((1<<24)*Math.random()|0).toString(16);
        if(tipe === "small"){
          console.log("retorno small")
          return `height: 1.7rem;
                  width: 1.7rem;
                  color: white;
                  background-color: `+ randomColor +`;
                  border-radius: 1.5rem;
                  border: 1px solid #d4d7db;`

        }else{
          return `height: 2.7rem;
                  width: 2.7rem;
                  color: white;
                  background-color: `+ randomColor +`;
                  border-radius: 3rem;
                  border: 2px solid #d4d7db;`
                  
        }
    },
    textClass(tipe){
      if(tipe === "small"){
        return `margin: auto;
                width: 50%;
                text-align: center;
                font-size: 0.7rem;`

      }else{
        return `margin: auto;
                width: 50%;
                text-align: center;
                font-size: 0.9rem;`
                
      }
    }
  }
};
</script>

<style>

</style>
