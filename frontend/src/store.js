import Vue from 'vue';
import Vuex from 'vuex';
import axios from '@/custom_axios.js';
import localforage from 'localforage';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    stateIsLoaded: false,
    isAuthenticated: false,
    user: {
      id: '',
      username: '',
      first_name: '',
      last_name: '',
      full_name: ''
    },
    active_users: { // Para usuarios activos en tablero
      users: []
    },
  },
  mutations: {
    setUser(state, { id, username, first_name, last_name }) {
      state.user = { id, username, first_name, last_name,
        full_name: first_name + ' ' + last_name };
    },
    setIsAuthenticated(state, isAuthenticated){
      state.isAuthenticated = isAuthenticated;
    },
    setStateIsLoaded(state, isLoaded){
      state.stateIsLoaded = isLoaded;
    },
    newUserEvent(user){
      Vue.set(state.active_users, 'users', [...user]) // [..myArray] will prevent changes to the object from other source to change your source, so it's a good idea to implement in getters too. https://stackoverflow.com/questions/50767191/vuex-update-an-entire-array/50767787
    }
  },
  actions: {
    getAuthorization(context, { username, password }) {
      // Gets access token cookie and user for the given username and
      // password, clearing the local storage and saving the state if success.

      return axios.post('login/', { username, password })
        .then(res => {
          context.commit('setUser', res.data);
          context.commit('setIsAuthenticated', true);
          context.commit('setStateIsLoaded', true);
          // Clear storage before a new session:
          localforage.clear().then(() => {
            context.dispatch('saveState');
          })
        });
    },
    saveState(context) {
      // Saves each property of the state in local storage.

      for(let [key, value] of Object.entries(context.state)){
        localforage.setItem(key, value).catch(err => console.log(err));
      }
    },
    loadState(context) {
      // Loads each property of the state. For each property it's assumed
      // there exists a mutation like 'set<property name>' with the property
      // name starting with uppercase.

      return localforage.iterate((value, key) => {
        const mutationName = 'set' + key.charAt(0).toUpperCase() + key.slice(1);
        context.commit(mutationName, value);
      })
    },
    checkState(context) {
      // Checks if state is loaded, or load it returning a resolved promise. If
      // the state couldn't be loaded returns a rejected promise.

      if(context.state.stateIsLoaded)
        return Promise.resolve();
      return localforage.getItem('isAuthenticated').then(isAuthenticated => {
        if(isAuthenticated)
          return context.dispatch('loadState');
        return Promise.reject();
      })
    },
    isAuthenticated(context){
      // Returns a resolved promise if state was checked correctly and the user
      // is authenticated, else returns a rejected promise.

      return context.dispatch('checkState').then(() =>{
        if(context.state.isAuthenticated)
          return Promise.resolve();
        return Promise.reject();
      })
    },
    clearStorage(){
      return localforage.clear();
    },
    newUserEvent(context, user){
      context.commit('newUserEvent', user) // Esta action llama a la mutation que hace la pega
    }
  }
});
