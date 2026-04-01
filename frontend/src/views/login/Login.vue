<template>
  <v-main class="white-bg center-content">
    <!-- กล่องหลักที่เก็บเนื้อหาทั้งหมดของฟอร์ม login -->
    <div class="login-container">
      <div>
        <v-btn class="back-btn" variant="text" @click="goToMain">
          <v-icon left>mdi-arrow-left</v-icon>
          กลับหน้า Main
        </v-btn>
      </div>
      <!-- โลโก้ -->
      <div class="logo">
        <img src="@/assets/images/logo_app.png" width="150" height="150" />
      </div>

      <!-- หัวข้อ -->
      <div class="center-box">
        <h2 class="login-title">เข้าสู่ระบบ</h2>
      </div>

      <!-- ฟอร์ม -->
      <form @submit.prevent="handleLogin">
        <!-- 🔑 ฟิลด์ username -->
        <div class="form-group">
          <label for="username">ซี่อผู้ใช้:</label>
          <input type="text" id="username" v-model="username" required />
        </div>

        <!-- 🔑 ฟิลด์ password -->
        <div class="form-group">
          <label for="password">รหัสผ่าน:</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <!-- 🔘 ปุ่มเข้าสู่ระบบ -->
        <button class="login-btn" type="submit" :disabled="loading">
          {{ loading ? "กำลังเข้าสู่ระบบ..." : "เข้าสู่ระบบ" }}
        </button>
      </form>
      <!--  แสดงค่าผิดพลาด message! -->
      <p v-if="message" class="message-error">{{ message }}</p>
    </div>
  </v-main>
</template>

<script setup>
// ref ใช้สร้าง reactive variable
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { API_BASE_URL } from "@/assets/config";

const loading = ref(false);
const username = ref("");
const password = ref("");
const message = ref("");
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  message.value = "";

  try {
    const res = await axios.post(
      `${API_BASE_URL}/login`,
      {
        username: username.value,
        password: password.value,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      },
    );

    if (res.data.access_token) {
      const token = res.data.access_token;

      //ชื่อ key ตรง backend
      const expiresAt = Date.now() + 2 * 60 * 60 * 1000;
      // 2 จำนวนชั่วโมง 60 นาทีต่อชั่วโมง 60 วินาทีต่อหนึ่งนาที 1000 มิลลิวินาทีต่อหนึ่งวินาที = 1756568878973 วินาที

      localStorage.setItem("access_token", token);
      localStorage.setItem("expiresAt", expiresAt);

      console.log("access_token: ", token);
      console.log("expiresAt: ", expiresAt);

      message.value = "เข้าสู่ระบบสำเร็จ";

      await router.push("/home"); // เปลี่ยนเส้นทางไปยังหน้า home
    } else {
      message.value = "เกิดข้อผิดพลาด Token ไม่ถูกต้อง";
    }
  } catch (err) {
    // ✅ แสดง error message ชัดเจน
    if (err.response && err.response.data && err.response.data.message) {
      message.value = err.response.data.message;
    } else if (err.response && err.response.data && err.response.data.error) {
      message.value = err.response.data.error;
    } else {
      message.value = "เกิดข้อผิดพลาดในการเชื่อมต่อเซิร์ฟเวอร์";
    }
  } finally {
    loading.value = false;
  }
};

const goToMain = () => {
  router.push("/main");
};
</script>

<style scoped></style>
