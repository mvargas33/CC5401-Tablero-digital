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
    active_users: [], //para el Board
    actualBoard: -1, //board que estoy revisando
    postItViews: []
  },
  mutations: {
    setUser(state, {id, username, first_name, last_name}) {
      state.user = {
        id, username, first_name, last_name,
        full_name: first_name + ' ' + last_name
      };
    },
    setIsAuthenticated(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
    setStateIsLoaded(state, isLoaded) {
      state.stateIsLoaded = isLoaded;
    },
    newUserEvent(state, data) {
      let newArray = Array.from(state.active_users);
      let otherArray = newArray.filter(users => {
        return users.username === data.user.username;
      });
      if (data.board === state.actualBoard && otherArray.length === 0 && state.user.username !== data.user.username) {
        state.active_users.push(data.user);
        console.log(state.active_users);
      }
    },
    userOutEvent(state, user) {
      let newArray = Array.from(state.active_users);
      newArray.filter(users => {
        return users.username !== user.username
      });
      Vue.set(state, 'active_users', newArray);
    },
    currentBoardEvent(state, data) {
      state.actualBoard = data;
    },
    activePostitEvent(state, data){
      if (typeof (state.postItViews[data.postit.id]) === 'undefined'){
        state.postItViews[data.postit.id] = new Array(data.user);
      }
      else {
        state.postItViews[data.postit.id].push(data.user);
      }
      console.log('activePostitEvent');
      console.log(state.postItViews);
    },
    leavePostitEvent(state, data){
      console.log('afirmativo');
      function checkUsername(username){
        return username === data.user.username;
      }
      let filtered = state.postItViews[data.postit].filter(checkUsername);
      state.postItViews[data.postit] = filtered;
      console.log(state.postItViews);
    }
  },
  actions: {
    getAuthorization(context, {username, password}) {
      // Gets access token cookie and user for the given username and
      // password, clearing the local storage and saving the state if success.

      return axios.post('login/', {username, password})
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

      for (let [key, value] of Object.entries(context.state)) {
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

      if (context.state.stateIsLoaded)
        return Promise.resolve();
      return localforage.getItem('isAuthenticated').then(isAuthenticated => {
        if (isAuthenticated)
          return context.dispatch('loadState');
        return Promise.reject();
      })
    },
    isAuthenticated(context) {
      // Returns a resolved promise if state was checked correctly and the user
      // is authenticated, else returns a rejected promise.

      return context.dispatch('checkState').then(() => {
        if (context.state.isAuthenticated)
          return Promise.resolve();
        return Promise.reject();
      })
    },
    clearStorage() {
      return localforage.clear();
    },
    newUserEvent(context, data) {
      context.commit('newUserEvent', data)
    },
    userOutEvent(context, user) {
      context.commit('userOutEvent', user)
    },
    currentBoardEvent(context, data) {
      context.commit('currentBoardEvent', data)
    },
    leavePostitEvent(context, data){
      context.commit('leavePostitEvent', data)
    },
    activePostitEvent(context, data){
      context.commit('activePostitEvent', data)
    }
  }
});
