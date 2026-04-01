<!-- ส่วนเนื้อหา -->
<template>
  <!-- ส่วนเนื้อหาหลักของหน้า -->
  <v-main class="white-bg map-main">
    <!-- <v-container>: เป็น container สำหรับจัด layout -->
    <v-container>
      <!-- แถวปุ่มเพิ่มข้อมูลสมาชิก -->
      <!-- <v-row> + <v-col>: ใช้จัด grid สำหรับปุ่ม “เพิ่มข้อมูลสมาชิก” -->
      <v-row class="align-center">
        <v-col cols="auto" class="pa-0 ml-3">
          <!-- ปุ่มเพิ่มสมาชิก -->
          <v-btn color="success" @click="add">
            <v-icon start>mdi-account-plus</v-icon>
            เพิ่มข้อมูลสมาชิก
          </v-btn>
        </v-col>
      </v-row>
      <!-- เว้นวรรค -->
      <div style="height: 24px"></div>

      <!-- ตารางสมาชิก -->
      <v-card
        title="ตารางข้อมูลสมาชิก"
        class="custom-table"
        prepend-icon="mdi-account-plus"
        flat
      >
        <template v-slot:text>
          <v-text-field
            v-model="search"
            label="ค้นหา"
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            hide-details
            single-line
            class="custom-search"
          ></v-text-field>
        </template>

        <v-data-table
          :headers="headers"
          :items="users"
          :items-per-page="10"
          :search="search"
          class="custom-headers"
        >
          <template v-slot:headers="{ columns }">
            <tr>
              <th
                v-for="column in columns"
                :key="column.key"
                class="custom-headers-table"
              >
                {{ column.title }}
              </th>
            </tr>
          </template>
          <!-- ปรับสลับสี -->
          <template v-slot:item="{ item, index }">
            <tr :class="index % 2 === 0 ? 'row-even' : 'row-odd'">
              <td class="tr">{{ index + 1 }}</td>
              <td class="tr">{{ item.user_name }}</td>
              <td class="tr">{{ item.email }}</td>
              <td class="tr">{{ formatDate(item.created_date) }}</td>
              <td class="tr">{{ formatDate(item.updated_date) }}</td>
              <td class="tr">
                {{
                  statuss.find(
                    (s) => s.id === (item.status ?? item.user_status)
                  )?.status_name || "ไม่ทราบสถานะ"
                }}
              </td>
              <!-- ปิด dialog แก้ไข -->
              <td class="text-left">
                <v-avatar
                  color="yellow-darken-2"
                  size="32"
                  class="elevation-1"
                  style="cursor: pointer"
                  @click="edit(item.user_id)"
                >
                  <v-icon color="white" icon="mdi-pencil" size="20" />
                </v-avatar>
              </td>

              <!-- เปิด dialog ยืนยันลบ -->
              <td class="text-left">
                <v-avatar
                  color="red-darken-2"
                  size="32"
                  class="elevation-1"
                  style="cursor: pointer"
                  @click="del(item.user_id)"
                >
                  <v-icon color="white" icon="mdi-delete" size="20" />
                </v-avatar>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-card>
    </v-container>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="2000">
      {{ snackbar.text }}
    </v-snackbar>
    <!-- Dialog สำหรับเพิ่ม/แก้ไขข้อมูลผู้ใช้ -->
    <v-dialog v-model="dialog" max-width="850">
      <v-card
        class="dialog-popup"
        style="background-color: #ffffff; color: #000000"
      >
        <v-toolbar flat :color="isEditing ? 'warning' : 'success'">
          <v-card-title class="dialog-title text-white">
            {{ isEditing ? "แก้ไขข้อมูลผู้ใข้" : "เพิ่มข้อมูลผู้ใช้" }}
          </v-card-title>
        </v-toolbar>
        <!-- ฟอร์มข้อมูล -->
        <v-card-text
          :class="isEditing ? 'card-text-warning' : 'card-text-success'"
        >
          <v-row>
            <v-col cols="12" md="6">
              <!-- ชื่อผู้ใช้ disabled เมื่อ edit -->
              <v-text-field
                v-model="record.user_name"
                label="ซื่อผู้ใช้"
                variant="outlined"
                color="success"
                class="custom-input"
                :rules="[required]"
                :disabled="isEditing"
              />
            </v-col>
            <v-col cols="12" md="6">
              <!-- อีเมล -->
              <v-text-field
                v-model="record.email"
                label="อีเมล"
                variant="outlined"
                color="success"
                class="custom-input"
                :rules="[required, emailRule]"
              />
            </v-col>
            <v-col cols="12" md="6">
              <!-- รหัสผ่าน -->
              <v-text-field
                v-model="record.password"
                label="รหัสผ่าน"
                variant="outlined"
                color="success"
                class="custom-input"
                :rules="isEditing ? [] : [required]"
              />
            </v-col>
            <v-col cols="12" md="6">
              <!-- ยื่นรหัสผ่าน -->
              <v-text-field
                v-model="record.confirmPassword"
                label="ยื่นยันรหัสผ่าน"
                variant="outlined"
                color="success"
                class="custom-input"
                :rules="isEditing ? [] : [required, passwordMatch]"
              />
            </v-col>
            <v-col cols="12" md="6">
              <!-- สถานะ -->
              <v-select
                v-model="record.status"
                :items="statuss"
                label="สถานะ"
                variant="outlined"
                color="success"
                class="custom-inpput"
                :rules="isEditing ? [] : [required]"
                item-title="status_name"
                item-value="id"
                return-object
              />
            </v-col>
          </v-row>
        </v-card-text>
        <v-divider />

        <!-- ปุ่มบันทึกและยกเลิก -->
        <v-card-actions
          :class="[
            'd-flex justify-end',
            isEditing ? 'action-warnimg' : 'action-success',
          ]"
        >
          <v-btn
            color="red-darken-1"
            variant="flat"
            class="text-white"
            @click="dialog = false"
            >ยกเลิก
          </v-btn>

          <v-btn
            color="green-darken-1"
            variant="flat"
            class="text-white"
            @click="save"
            >บันทึก
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- ควบคุมการลบข้อม฿ล confirmDeleteDialog -->
    <v-dialog v-model="confirmDeleteDialog" max-width="400">
      <v-card class="confirm-delete-dialog">
        <v-card-title class="text-h6 confirm-delete-title">
          ยืนยันการลบ
        </v-card-title>
        <v-card-text class="confirm-delete-text">
          คุณต้องการลบผู้ใช้งานใช้หรือไม่ ???
        </v-card-text>
        <v-card-actions class="confirm-delete-action">
          <v-spacer />
          <v-btn
            color="red-darken-1"
            variant="flat"
            @click="confirmDeleteDialog = false"
          >
            ยกเลิก
          </v-btn>
          <v-btn color="green-darken-1" variant="flat" @click="confirmDelete">
            ลบ
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-main>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import { API_BASE_URL } from "@/assets/config";

// ควบคุม Dialog เพิ่ม/แก้ไขข้อมูล
const dialog = ref(false);
const isEditing = ref(false);

// ควบคุม Dialog ลบข้อมูล
const confirmDeleteDialog = ref(false);
const deleteId = ref(null);

// ตัวแปรเก็บข้อมูลสังกัด (statuss) และ record สำหรับฟอร์ม
const statuss = ref([]);

// ตัวแปรเก็บข้อมูลสมาชิก (User) และ record สำหรับฟอร์ม
const users = ref([]);

// Snackbar แจ้งเตือนสถานะ
const snackbar = ref({
  show: false,
  text: "",
  color: "success",
});

// ฟังก์ชันแปลงวันที่ให้อ่านง่ายแบบไทย
const formatDate = (dateString) => {
  if (!dateString) return "-";
  const date = new Date(dateString);
  return date.toLocaleDateString("th-TH", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

// statuss.value = [
//   { id: 1, name: "ผู้ใช้งานทั่วไป" },
//   { id: 2, name: "ผู้ดูแลระบบ" },
//   { id: 3, name: "ผู้ดูแลระบบ (Dev)" },
// ];

// ค้นหาข้อมูลในตาราง
const search = ref("");

//กฏที่ตั้งไว้
// !!"hello"   // true
// !!0         // false
// !!null      // false
// !!123       // true
const required = (v) => !!v || "กรุณาเลือกกรอกข้อมูล";

// ตัวแปรเก็บข้อมูลผู้ใช้ทั้งหมด (จาก API)
const record = ref({});
const DEFAULT_RECORD = {
  user_id: null,
  user_name: "",
  email: "",
  password: "",
  confirmPassword: "",
  status: null,
};

// // เมื่อ component โหลดขึ้นมา
onMounted(() => {
  // โหลดข้อมูลผู้ใช้จาก API
  fetchUsers();
  fetchStatus();
});

// เตรียมเปิดฟอร์มแก้ไขข้อมูล โดยดึงข้อมูลผู้ใช้ตาม id
const add = () => {
  isEditing.value = false;
  dialog.value = true;
  record.value = { ...DEFAULT_RECORD };
};

// ลบข้อมูล โดยดึงข้อมูลผู้ใช้ตาม id
const del = (id) => {
  deleteId.value = id;
  confirmDeleteDialog.value = true;
};
// ลบผู้ใช้จริงๆ หลังยืนยัน
const confirmDelete = async () => {
  try {
    const token = localStorage.getItem("access_token");
    await axios.delete(`${API_BASE_URL}/user/delete/${deleteId.value}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    // ลบ user ออกจาก array ทันที
    users.value = users.value.filter((user) => user.user_id !== deleteId.value);
    showSnackBar("ลบข้อมูลแล้ว", "error");
    await fetchUsers(); // โหลดข้อมูลใหม่
  } catch (error) {
    showSnackBar("เกิดข้อผิดพลาดในการลบ", "error");
    console.error("Error deleting user : ", error);
  } finally {
    confirmDeleteDialog.value = false;
  }
};

// แสดง snackbar แจ้งเตือน
const showSnackBar = (Message, type = "success") => {
  snackbar.value.text = Message;
  snackbar.value.color = type;
  snackbar.value.show = true;
};

// ดึงข้อมูล Status API
const fetchStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/user_status`);
    statuss.value = response.data;
    console.log("Response.data_status : ", response.data);
  } catch (error) {
    console.error("Error Fetching status", error);
    showSnackBar("เกิดข้อผิดพลาดในการดึงข้อมูล API", "error");
  }
};

// ดึงข้อมูล Users API
const fetchUsers = async () => {
  try {
    const token = localStorage.getItem("access_token");
    // console.log("access_token", token);

    const response = await axios.get(`${API_BASE_URL}/user`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    //ค่าที่ได้จาก API ค่า users
    users.value = response.data;
    console.log("Response.data : ", response.data);
  } catch (error) {
    console.error("Error Fetching users", error);
    showSnackBar("เกิดข้อผิดพลาดในการดึงข้อมูล API", "error");
  }
};

// เตรียมเปิดฟอร์มแก้ไขข้อมูล โดยดึงข้อมูลผู้ใช้ตาม id
const edit = (id) => {
  isEditing.value = true;
  const found = users.value.find((user) => user.user_id === id);
  if (found) {
    // แปลง id เป็น number เผื่อ string มา
    const userStatudId = Number(found.user_status || found.status);
    const statusObj = statuss.value.find((s) => s.id === userStatudId);

    record.value = {
      ...DEFAULT_RECORD,
      ...found,
      password: "",
      confirmPassword: "",
      status: statusObj || null,
    };
  }
  dialog.value = true;
};

// บันทึกข้อมูลผู้ใช้ (เพิ่มหรือแก้ไข)
const save = async () => {
  try {
    // ตรวจสอบรหัสผ่านถ้ามีการกรอก
    if (
      record.value.password &&
      record.value.password !== record.value.confirmPassword
    ) {
      console.error("Eroror fetching users");
      showSnackBar("รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน", "error");
      return;
    }

    // เตรียมข้อมูลให้สอดคล้องกับ API payload และ config
    const payload = {
      user_id: isEditing.value ? record.value.user_id : undefined,
      user_name: record.value.user_name,
      email: record.value.email,
      status: record.value.status?.id || record.value.status,
    };

    // เพิ่ม password
    if (record.value.password) {
      payload.password = record.value.password;
    }
    //console.log("payload: ", payload);

    const token = localStorage.getItem("access_token");
    // console.log("token: ", token);

    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    };
    //console.log("config: ", config);

    if (isEditing.value) {
      // update → PUT
      //console.log("update: ");
      await axios.put(
        `${API_BASE_URL}/user/update/${record.value.user_id}`,
        payload,
        config
      );
    } else {
      // insert → POST
      //console.log("insert: ");
      await axios.post(`${API_BASE_URL}/user/insert`, payload, config);
    }

    showSnackBar("ยืนยันถูกต้อง", "success");
    await fetchUsers(); //โหลดข้อมูลใหม่ Users
    await fetchStatus(); //โหลดข้อมูลใหม่ Status
  } catch (error) {
    // ✅ ดึงข้อความ error จาก backend
    if (error.response && error.response.data && error.response.data.error) {
      showSnackBar(error.response.data.error, "error");
    } else {
      showSnackBar("เกิดข้อผิดพลาดในการบันทึก", "error");
    }
    console.error("Eroror fetching users", error);
  }
};
//ข้อมูลตาราง
const headers = [
  {
    align: "start",
    key: "num",
    sortable: false,
    title: "ลำดับ",
  },
  { key: "user_name", title: "ชื่อผู้ใช้" },
  { key: "email", title: "อีเมล" },
  { key: "create_date", title: "วันที่ลงทะเบียน" },
  { key: "update_date", title: "วันที่ปรับปรุ่ง" },
  { key: "status_user", title: "สถานะ" },
  { key: "edit", title: "แก้ไข", sortable: false },
  { key: "del", title: "ลบ", sortable: false },
];
// const users = [
//   {
//     num: "1",
//     user_name: "user_name_1",
//     email: "user_name@gmail.com",
//     create_date: "24/09/68",
//     update_date: "24/09/68",
//     status_user: "ผู้ใช้งานทั่วไป",
//   },
//   {
//     num: "2",
//     user_name: "user_name_2",
//     email: "user_name@gmail.com",
//     create_date: "24/09/68",
//     update_date: "24/09/68",
//     status_user: "ผู้ใช้งานทั่วไป",
//   },
//   {
//     num: "3",
//     user_name: "user_name_3",
//     email: "user_name@gmail.com",
//     create_date: "24/09/68",
//     update_date: "24/09/68",
//     status_user: "ผู้ใช้งานทั่วไป",
//   },
//   {
//     num: "4",
//     user_name: "user_name_4",
//     email: "user_name@gmail.com",
//     create_date: "24/09/68",
//     update_date: "24/09/68",
//     status_user: "ผู้ใช้งานทั่วไป",
//   },
// ];
</script>
<style scoped></style>
