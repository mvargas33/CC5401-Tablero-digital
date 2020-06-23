import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Board from './views/Board.vue'
import Login from './views/Login.vue'
import axios from '@/custom_axios.js'

Vue.use(Router)

const router=  new Router({
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/board/:boardId',
      name: 'Board',
      component: Board
    },
    {
      path: '/',
      name: 'Login',
      component: Login,
      props: route => ({'new_user': route.query.new_user}),
    },
    {
      path: '/signup',
      name: 'SignUp',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/SignUp.vue')
    }
  ]
})

// A vuex store is expected to be added to the router for some of the
// functionality below:
router.store = {}

function checkInPaths(to, pathNames, next, onTrue, onFalse){
  // Check if to.name is in pathNames, using onTrue config for next() if true,
  // or using onFalse config otherwise.
  if(pathNames.includes(to.name)) next(onTrue);
  else next(onFalse);
}


router.beforeEach((to, from, next) => {
  // Check if the user is authenticated and redirect him or not depending on it.
  
  // Paths accessible if and only if the user is not authenticated:
  const noAuthPathNames = ['Login', 'SignUp'];

  router.store.dispatch('isAuthenticated')
    .then(() => checkInPaths(to, noAuthPathNames, next, {name: 'Home'}, {}))
    .catch(() => checkInPaths(to, noAuthPathNames, next, {}, {name: 'Login'}));
});


router.login = function(username, password){
  // Sends the user to Home if login is successful or returns a rejected
  // Promise otherwise.

  return this.store.dispatch('getAuthorization', { username, password })
    .then(() => this.push({name: 'Home'}));
}

router.logout = function(){
  // Clear user data and send the user to the Login view.

  axios.get('logout/').then(() => {
    // Clear session data:
    this.store.dispatch('clearStorage')
      // Reload the window to clear data from store, automatically redirecting
      // to the Login page:
      .then(() => window.location.reload());
  });
}

export default router;
