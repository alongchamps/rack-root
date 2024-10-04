/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'

// core/utility pages
import index from '../pages/index.vue'
import fourohfour from '../pages/404.vue'
import settings from '../pages/Settings.vue'

// pages relating to inventory items
import allItems from '../pages/items/AllItems.vue'
import singleItem from '../pages/items/SingleItem.vue'
import newItem from '../pages/items/NewItem.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Index',
      component: index
    },
    {
      path: '/items',
      name: 'AllItems',
      component: allItems
    },
    {
      path: '/items/:id(\\d+)',
      name: 'SingleItem',
      component: singleItem
    },
    {
      path: '/items/new',
      name: 'NewItem',
      component: newItem
    },
    {
      path: '/settings',
      name: 'Settings',
      component: settings
    },
    {
      path: '/:path*',
      name: 'FourOhFour',
      component: fourohfour
    }
  ]
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
