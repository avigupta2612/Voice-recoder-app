import Vue from 'vue';
import Router from 'vue-router';


Vue.use(Router);

//Container
const Container = () => import('@/components/Container')

//Views
// const Landing = () => import('@/views/Landing')
const Recorder = () => import('@/views/Recorder')
const Uploader = () => import('@/views/Uploader')
const Samples = () => import('@/views/Samples')

export default new Router ({
    mode :'history',
    routes: [
        {
            path: '/',
            name: 'Container',
            component: Container,
            children: [
                /* {
                    path: '/',
                    name: 'Landing',
                    component: Landing
                },*/
                {
                    path: '/upload',
                    name: 'Uploader',
                    component: Uploader
                },
                {
                    path: '/',
                    name: 'Recorder',
                    component: Recorder
                },
                {
                    path: '/samples',
                    name: 'Samples',
                    component: Samples
                }
            ]
        }
    ],
})