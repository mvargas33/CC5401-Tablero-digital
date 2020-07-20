import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import store from './store'
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

// Drag and drop library
import vDragDrop from 'v-drag-drop';
Vue.use(vDragDrop);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
