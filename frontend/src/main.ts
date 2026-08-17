import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import { createPinia } from 'pinia'
import { useThemeStore } from './stores/theme'
import { setupObservability } from './modules/core/observability'
import { axiosInstrumentation } from './plugins/axios-instrumentation'
import { routerInstrumentation } from './plugins/router-instrumentation'

setupObservability()

const app = createApp(App)

axiosInstrumentation()
routerInstrumentation(router)

app.use(createPinia())
app.use(vuetify)
app.use(router)

const themeStore = useThemeStore()
themeStore.initTheme()

app.mount('#app')
