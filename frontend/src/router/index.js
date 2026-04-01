// นำเข้า Vue Router
import { createRouter, createWebHistory } from "vue-router";

// นำเข้า Vue Router
import login from "../views/login/Login.vue";
import home from "../views/home/Home.vue";
import home_view from "../views/home/Home_View.vue";
import reg from "../views/register/Register.vue";
import reg_view from "../views/register/Register_View.vue";
import map from "../views/map/Map.vue";
import map_view from "../views/map/Map_Views.vue";
import main from "../views/main/Main.vue";
import main_view from "../views/main/Main_View.vue";

// ฟังก์ชันตรวจสอบ access_token
function checkToken() {
  const access_token = localStorage.getItem("access_token");
  const expiresAt = localStorage.getItem("expiresAt");

  if (!access_token || !expiresAt) return false;

  if (Date.now() > Number(expiresAt)) {
    // หมดอายุแล้ว → ลบ access_token
    localStorage.removeItem("access_token");
    localStorage.removeItem("expiresAt");

    return false;
  }

  return true;
}

// กำหนดเส้นทางสำหรับแอปพลิเคชัน
const routes = [
  {
    path: "/",
    component: main,
    meta: { public: true },
    children: [
      {
        path: "",
        component: main_view,
        meta: { public: true },
      },
    ],
  },
  {
    path: "/main",
    component: main,
    meta: { public: true },
    children: [
      {
        path: "",
        component: main_view,
        meta: { public: true },
      },
    ],
  },
  {
    path: "/login",
    component: login,
    meta: { public: true },
  },
  {
    path: "/home",
    component: home,
    meta: {
      requiresAuth: true,
    }, // ต้องล็อกอิน
    children: [{ path: "", component: home_view }],
  },
  {
    path: "/map",
    component: map,
    meta: {
      requiresAuth: true,
    }, // ต้องล็อกอิน
    children: [{ path: "", component: map_view }],
  },
  {
    path: "/reg",
    component: reg,
    meta: {
      requiresAuth: true,
    }, // ต้องล็อกอิน
    children: [{ path: "", component: reg_view }],
  },
];

// สร้าง router instance
// กำหนด base path เป็น "/project_vue/" ตามที่ระบุใน vite.config.mjs
const router = createRouter({
  history: createWebHistory("/project_vue/"),
  routes,
});

// 🔒 ตรวจสอบ access_token ก่อนเข้าหน้า
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !checkToken()) {
    // ถ้า access_token หมดอายุหรือไม่มี → ไปหน้า login
    next("/login");
  } else {
    next();
  }
});

// กำหนดการตรวจสอบเส้นทาง
export default router;
