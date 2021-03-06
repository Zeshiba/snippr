import Vue from 'vue';
import router from './router';
import store from './store';
import EventBusCallbacks from './plugins/event-bus-callbacks';

import eventBus from './plugins/event-bus';
import App from './components/App.vue';
require('./stylesheets/index.scss');

import { library } from '@fortawesome/fontawesome-svg-core'
import { faArrowAltCircleUp, faArrowAltCircleDown, faCommentAlt, faUser, faKey, faWrench, faPlus, faSearch, faStar, faBullhorn} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faArrowAltCircleUp, faArrowAltCircleDown, faCommentAlt, faUser, faKey, faWrench, faPlus, faSearch, faStar, faBullhorn);

(async () => {
    router.beforeEach(async (to, from, next) => {
      if(localStorage.getItem('token')) {
        if(await store.dispatch('auth/refreshLogin')) {
          store.dispatch('auth/getProfile');
        }
      }
      
      const isLoggedIn = store.getters['auth/isLoggedIn'];

      if (to.meta.loginRequired && !isLoggedIn) {
          return next({replace: true, name: 'home'});
      } else if (to.meta.loginRequired === false && isLoggedIn) {
          return next({replace: true, name: 'feed'});
      }
      next();
    });
})();

Vue.use(EventBusCallbacks, eventBus);
Vue.component('font-awesome-icon', FontAwesomeIcon)

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});
