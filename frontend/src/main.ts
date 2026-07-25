import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import { createPinia } from 'pinia'
import { useThemeStore } from './stores/theme'

const app = createApp(App)

app.use(createPinia())
app.use(vuetify)
app.use(router)

const themeStore = useThemeStore()
themeStore.initTheme()

app.mount('#app')
