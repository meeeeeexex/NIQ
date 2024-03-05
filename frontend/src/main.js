import {createApp} from 'vue';
import {createRouter, createWebHistory} from "vue-router";

import App from './App.vue';
import TheForm from "@/components/TheForm";
import TheList from "@/components/TheList";
import TheDelete from "@/components/TheDelete";
import TheEdit from "@/components/TheEdit";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {path: '/', component: TheForm},
        {path: '/main', component: TheList},
        {path: '/delete', component: TheDelete},
        {path: '/edit', component: TheEdit}
    ]
});
createApp(App).use(router).mount('#app');
