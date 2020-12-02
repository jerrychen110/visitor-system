export default {
    path: '/mgt',
    component: () => import('./mgt.vue'),
    meta:{
      title: '随访系统'
    },
    children: [
      {
        path:'/',
        component: () => import('./Main.vue'),
       
        meta:{
          title: '病人管理',
          icon: 'el-icon-s-check'
        },
        children: [
          {
            path: '/',
            name: 'patientList',
            component: () => import('./patients/List.vue')
          },
          {
            path: 'patients/creat',
            name: 'patientCreat',
            component: () => import('./patients/Creat.vue'),
            meta:{
              title: '录入病人信息'
            },
          },
          {
            path: 'editor/:id',
            name: 'patientEditor',
            component: () => import('./patients/Creat.vue'),
            meta:{
              title: '编辑病人信息'
            },
          }
        ]
      },
      {
        path:'voices',
        component: () => import('./Main.vue'),
        meta:{
          title: '语音管理',
          icon: 'el-icon-microphone'
        },
        children: [
          {
            path: '/',
            name: 'voiceList',
            component: () => import('./voices/List.vue')
          },
          {
            path: 'creat',
            name: 'voiceCreat',
            component: () => import('./voices/Creat.vue'),
            meta:{
              title: '录入语音信息'
            },
          },
          {
            path: 'editor/:id',
            name: 'voiceEditor',
            component: () => import('./voices/Creat.vue'),
            meta:{
              title: '编辑语音信息'
            },
          }
        ]
      },
      {
        path: 'system',
        component: () => import('./Main.vue'),
        meta:{
          title: '参数管理',
          icon: 'el-icon-s-order'
        },
        children: [
          {
            path: '/',
            name: 'system',
            component: () => import('./system/Edit.vue'),
            meta:{
              title: '编辑参数'
            },
          }
        ]
      },
      {
        path: 'users',
        component: () => import('./Main.vue'),
        meta:{
          title: '用户管理',
          icon: 'el-icon-s-custom',
          role: ['超级管理员']
        },
        children: [
          {
            path: '/',
            name: 'usersList',
            component: () => import('./users/List.vue')
          },
          {
            path: 'creat',
            name: 'usersCreat',
            component: () => import('./users/Creat.vue'),
            meta:{
              title: '新建用户'
            },
          },
          {
            path: 'editor/:id',
            name: 'usersEditor',
            component: () => import('./users/Creat.vue'),
            meta:{
              title: '编辑用户'
            },
          }
        ]
      }
    ]
  }