import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import store from './store'
//import VueSocketIO from 'vue-socket.io'
import VueSocketIOExt from 'vue-socket.io-extended'
import SocketIO from "socket.io-client"

// FontAwesome imports:
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faCompressArrowsAlt,
  faExpandArrowsAlt,
  faPlus,
  faStickyNote,
  faLink,
  faEllipsisH,
  faUserPlus,
  faEdit,
  faHome,
  faUsers,
  faFlag,
  faDatabase,
  faLightbulb,
  faChartBar,
  faBrain,
  faRuler,
  faDesktop,
  faMountain,
  faThumbsUp,
  faThumbsDown,
  faTimes,
  faInfoCircle,
  faEllipsisV,
  faLaptopCode,
  faBriefcase,
  faTrash,
  faSave,
  faWindowClose,
} from '@fortawesome/free-solid-svg-icons' // Import icons here
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// FontAwesome configs:
library.add(faCompressArrowsAlt, // Add the imported icons like this
  faExpandArrowsAlt,
  faPlus,
  faStickyNote,
  faEllipsisH,
  faUserPlus,
  faLink,
  faEdit,
  faHome,
  faUsers,
  faFlag,
  faDatabase,
  faLightbulb,
  faChartBar,
  faBrain,
  faRuler,
  faDesktop,
  faMountain,
  faThumbsUp,
  faThumbsDown,
  faTimes,
  faInfoCircle,
  faEllipsisV,
  faLaptopCode,
  faBriefcase,
  faTrash,
  faSave,
  faWindowClose
)
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false

// Add store to router, so we can perform redirects based on state.
router.store = store;

// Socket.io config
// Vue.use(new VueSocketIO({
//   debug: true,
//   connection: SocketIO('http://localhost:3000'),
//   vuex: {
//     store,
//     actionPrefix: 'SOCKET_',
//     mutationPrefix: 'SOCKET_'
//   }
// }))
const socket = SocketIO('http://localhost:3000')
Vue.use(VueSocketIOExt, socket)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
