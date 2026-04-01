<template>
  <v-app-bar class="app-bar">
    <v-app-bar-nav-icon
      variant="text"
      @click.stop="drawer = !drawer"
    ></v-app-bar-nav-icon>
    <v-toolbar-title>Project_Vue</v-toolbar-title>
  </v-app-bar>

  <v-navigation-drawer v-model="drawer" app class="app-bar">
    <v-list>
      <v-list-item
        prepend-avatar="@/assets/images/logo_app.png"
        subtitle="Project"
        title="โปรเจค"
      >
      </v-list-item>
    </v-list>
    <!-- เส้นแบ่งระหว่าง Header กับ เมนู -->
    <v-divider></v-divider>

    <v-list density="compact" nav>
      <!-- เมนูทั่วไป -->
      <v-list-item
        v-for="(item, i) in menuItems"
        :key="i"
        :to="item.href"
        router
        exact
        @click="closeDrawer"
        :active="$route.path === item.href"
      >
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <!-- เส้นแบ่งระหว่าง เมนู กับ ออก -->
      <v-divider></v-divider>
      <!-- ปุ่ม Logout -->
      <!-- เรียก method logout() เพื่อลบ access_token และพาไปหน้า Login -->
      <v-list-item @click="logout">
        <v-list-item-icon>
          <v-icon>mdi-logout</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Logout (ออกจากระบบ)</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";

const menuItems = [
  { title: "Home (หน้าหลัก)", icon: "mdi-home", href: "/home" },
  { title: "Map (แผนที่)", icon: "mdi-map", href: "/map" },
  { title: "Register (ลงทะเบียน)", icon: "mdi-account-plus", href: "/reg" },
];

const drawer = ref(false);
const group = ref(null);
const router = useRouter();

watch(group, () => {
  drawer.value = false;
});

function closeDrawer(){
  drawer.value = false;
}

function logout(){
  // clear access_token และ expiresAt เวลาหมดอายุ
  localStorage.removeItem("access_token");
  localStorage.removeItem("expiresAt");

  // redirect ไป login
  router.push("/main");
}

</script>
