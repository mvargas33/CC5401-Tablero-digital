<template>
    <b-modal :id="id" size="xl" hide-footer hide-header centered
        no-close-on-backdrop no-close-on-esc>
        <h2 class="text-center text-secondary my-4">Selecciona un equipo</h2>
        <div class="row">
            <b-button
                variant="primary"
                @click="selectTeam('S')"
                class="col m-4 team-button"
            >
                Stakeholders
                <font-awesome-icon icon="briefcase"/>
            </b-button>
            <b-button
                variant="primary"
                @click="selectTeam('D')"
                class="col m-4 team-button"
            >
                Desarrolladores
                <font-awesome-icon icon="laptop-code"/>
            </b-button>
        </div>
    </b-modal>
  
</template>

<script>
import axios from '@/custom_axios.js';

export default {
    name: 'SelectTeamModal',
    props: {
        id: String,
        workIn: Object,
    },
    methods: {
        selectTeam(team){
            // Selects the team ('S' or 'D') for the current user and board.
            
            axios.post(`workin/${this.workIn.id}/select_team/`, { team })
                .then(response => {
                    this.workIn.team = response.data.team;
                    this.workIn.is_leader = response.data.is_leader;
                    this.$bvModal.hide(this.id);
                })
                .catch(error => {
                    console.log(error);
                });
        }
    }
}
</script>

<style>

.team-button{
    font-size: 3rem;
    height: 18rem;
    box-shadow: 0 5px 5px rgba(0, 0, 0, 0.3)
}
</style>