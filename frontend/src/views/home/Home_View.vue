<template>
  <!-- ส่วนเนื้อหาหลักของหน้า -->
  <v-main class="white-bg map-main">
    <!-- <v-container>: เป็น container สำหรับจัด layout -->
    <v-container>
      <div class="map-wrapper">
        <div ref="mapRef" class="map"></div>

        <!-- ปุ่มสำหรับเพิ่มข้อมูล fullscreen, zoom in/out,  -->
        <div class="zoom-buttons">
          <v-tooltip text="เต็มหน้าจอ" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="FullScreen"
              >
                <v-icon>mdi-fullscreen</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <!-- เปลี่ยนแผนที่ เพิ่ม-->
          <v-tooltip text="เปลี่ยนแผนที่" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="switchBaseMap"
              >
                <v-icon>mdi-map</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <v-tooltip text="ซูมเข้า" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="ZoomIn"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <v-tooltip text="ซูมออก" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="ZoomOut"
              >
                <v-icon>mdi-minus</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <v-tooltip text="หมุนขวา 30°" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="rotateRight30"
              >
                <v-icon>mdi-rotate-right</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <v-tooltip text="หมุนซ้าย 30°" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="rotateLeft30"
              >
                <v-icon>mdi-rotate-left</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <v-tooltip text="รีเซ็ตการหมุน" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="resetRotation"
              >
                <v-icon>mdi-rotate-3d-variant</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <!-- เพิ่ม ปุ่มวาดเส้น / ลบเส้น -->
          <v-tooltip text="วาดเส้น" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="LineString"
              >
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <!-- เพิ่ม ปุ่มวัดพื้นที่ //เพิ่ม -->
          <v-tooltip text="วัดพื้นที่" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="Area"
              >
                <v-icon>mdi-pencil-box-outline</v-icon>
              </v-btn>
            </template>
          </v-tooltip>

          <v-tooltip text="ลบเส้น/ลบพื้นที่" location="right">
            <template #activator="{ props }">
              <v-btn
                size="default"
                color="success"
                v-bind="props"
                @click="ClearLines"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </template>
          </v-tooltip>
        </div>
      </div>

      <div ref="popupRef" class="ol-popup">
        <div ref="popupContent"></div>
      </div>

      <!-- แสดงพิกัดของ marker ปัจจุบัน -->
      <div class="coords" style="margin-top: 10px">
        Lon: {{ mapLongitude.toFixed(6) }}, lat: {{ mapLatitude.toFixed(6) }}
      </div>

      <!-- Snackbar แจ้งเตือนสถานะ -->
      <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        timeout="1000"
      >
        <v-icon
          icon="mdi-alert-circle-outline"
          class="mr-2"
          size="large"
          color="white"
        />
        {{ snackbar.text }}
      </v-snackbar>

      <!-- dialog points รายละเอียดตำแหน่ง -->
      <v-dialog v-model="detailDialog" max-width="400">
        <v-card
          class="dialog-popup"
          style="background-color: #ffffff; color: black"
        >
          <v-toolbar flat color="success">
            <v-card-title class="dialog-title text-white">
              รายละเอียดตำแหน่ง
            </v-card-title>
          </v-toolbar>

          <v-card-text v-if="selectedLocation">
            <div style="color: #f44336; font-size: 12px">
              ID: {{ selectedLocation.id }}
            </div>
            <strong style="font-size: 16px">
              {{ selectedLocation.name }}
            </strong>
            <div>
              {{ selectedLocation.description || "-" }}
            </div>

            <v-divider class="my-2" />
            <dv>Lat: {{ Number(selectedLocation.latitude).toFixed(6) }}</dv>
            <br />
            <dv>Lon: {{ Number(selectedLocation.longitude).toFixed(6) }}</dv>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="red-darken-1"
              variant="flat"
              class="text-white"
              @click="detailDialog = false"
            >
              <v-icon start>mdi-close</v-icon>
              ปิด
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </v-main>
</template>
<script setup>
import { ref, onMounted, onBeforeMount } from "vue";
import { useRoute } from "vue-router";

/* axios url */
import api from "axios";
import { API_BASE_URL } from "@/assets/config";

/* OpenLayers Imports */
import Map from "ol/Map";
import View from "ol/View";
import TileLayer from "ol/layer/Tile";

import { OSM } from "ol/source";
import XYZ from "ol/source/XYZ";

import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";

import Style from "ol/style/Style";
import { fromLonLat, toLonLat } from "ol/proj";
import CircleStyle from "ol/style/Circle";
import Fill from "ol/style/Fill";
import Stroke from "ol/style/Stroke";
import Feature from "ol/Feature";
import Point from "ol/geom/Point";

// เพิ่ม Line และ Area
import Text from "ol/style/Text";
import Draw from "ol/interaction/Draw";
import { getLength } from "ol/sphere";
import { getArea } from "ol/sphere";

// interaction + control
import { defaults as defaultInteractions } from "ol/interaction";
import { defaults as defaultControls, Zoom } from "ol/control";

// เพิ่ม Icon สำหรับแผนที่
import Icon from "ol/style/Icon";

// popup points
import Overlay from "ol/Overlay";

let popupOverlay = null;
const popupRef = ref(null);

const detailDialog = ref(false);
const selectedLocation = ref(null);

/* -----------------------------
   สร้างตัวแปรสำหรับจุด
------------------------------ */
let locationSource = null;
let locationLayer = null;

/* -----------------------------
   Refs และตัวแปรหลัก
------------------------------ */
const router = useRoute();
const mapRef = ref(null); //ref ของ div สำหรับ map
let map = null;
// let baseLayer = null;

/* -----------------------------
   วาดเส้น
------------------------------ */
let linelayer = null; //วาดเส้น
let draw = null; //วาดเส้น

const startMarkerSource = ref(null);
const lineMarkerSource = ref(null);
const distanceResult = ref("ยังไม่วัดระยะ");

// let markerSource = null; //vector layer สำหรับ marker
const mapLatitude = ref(13.769717); //เก็บพิกัดปัจจุบัน
const mapLongitude = ref(100.542119); //เก็บพิกัดปัจจุบัน

/* -----------------------------
   เปลี่ยนแผนที่ เพิ่ม
------------------------------ */
const currentBaseMap = ref("osm");
const baseMapOrder = ["osm", "satellite", "gray"];

/* -----------------------------
   สร้างจุดด้วย Pin
------------------------------ */
locationSource = new VectorSource();
locationLayer = new VectorLayer({
  source: locationSource,
  style: function (feature) {
    return new Style({
      image: new Icon({
        src: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        scale: 0.05,
        acchor: [0.5, 1],
      }),
      text: new Text({
        text: feature.get("name"), // 👈 ใช้ได้แล้ว
        offsetY: -25,
        font: "bold 14px sans-serif",
        fill: new Fill({ color: "#ff0000" }),
        stroke: new Stroke({ color: "#ffffff", width: 0.5 }),
      }),
    });
  },
});

/* -----------------------------
    Snackbar แจ้งเตือนสถานะ
------------------------------ */
const snackbar = ref({
  show: false,
  text: "",
  color: "success",
});

// ตัวแปรเก็บข้อมูลผู้ใช้ทั้งหมด (จาก API)
const locations = ref([]);

/* -----------------------------
   ตรวจสอบ token ก่อนใช้งาน
------------------------------ */
onMounted(() => {
  startMarkerSource.value = new VectorSource();
  lineMarkerSource.value = new VectorSource();

  const token = localStorage.getItem("access_token");
  const expiresAt = localStorage.getItem("expiresAt");

  if (!token || !expiresAt) {
    router.push("/login");
    return;
  }

  initMap(); //เรียกแผนที่ initMap
  getLocations(); //เรียกใช้ดึงข้อมูล
});

/* -----------------------------
   ดึงข้อมูล
------------------------------ */
const getLocations = async () => {
  try {
    const response = await api.get(`${API_BASE_URL}/locations/read`);

    if (Array.isArray(response.data)) {
      locations.value = response.data;
      console.log("locations : ", locations.value);
      renderPoints(); //เรียก Point
    }
  } catch (err) {
    console.error("โหลด locations ไม่สำเร็จ", err);
    locations.value = [];
  }
};

/* -----------------------------
   สร้าง Points
------------------------------ */
const renderPoints = () => {
  if (!locationSource) return;

  locationSource.clear();

  locations.value.forEach((item) => {
    if (!item.latitude || !item.longitude) return;

    const feature = new Feature({
      geometry: new Point(
        fromLonLat([Number(item.longitude), Number(item.latitude)]),
      ),
    });

    // จะตึงไปฝสใน Points
    feature.setProperties({
      id: item.id,
      name: item.name,
      default: item.description,
      latitude: item.latitude,
      longitude: item.longitude,
    });

    console.log("feature :", feature.getProperties());
    locationSource.addFeature(feature);
  });
};

/* -----------------------------
   ฟังก์ชันอัพเดต marker
------------------------------ */
const updateMarker = (coordinate) => {
  if (!startMarkerSource.value) return;
  startMarkerSource.value.clear(); // ล้าง marker เก่าก่อน
  const feature = new Feature({ geometry: new Point(coordinate) });
  startMarkerSource.value.addFeature(feature); //สร้าง marker ใหม่ที่ตำแหน่ง coordinate
};

/* -----------------------------
   ฟังก์ชันเริ่มต้นแผนที่
------------------------------ */
const initMap = () => {
  // startMarkerSource = new VectorSource(); //สร้าง VectorSource สำหรับ marker

  const markerStyle = new Style({
    image: new CircleStyle({
      radius: 8,
      fill: new Fill({ color: "red" }),
      Stroke: new Stroke({ color: "white", width: 2 }),
    }),
  });

  //สร้าง VectorLayer สำหรับ marker
  const markerLayer = new VectorLayer({
    source: startMarkerSource.value,
    style: markerStyle,
  });

  // add Layer Line + label
  linelayer = new VectorLayer({
    source: lineMarkerSource.value,
    style: (feature) => {
      const geom = feature.getGeometry(); //ดึง geometry ของ feature (เช่น LineString) มาใช้
      if (!geom) return null;

      // ======วัดเส้น ======= //
      if (geom.getType() === "LineString") {
        const length = getLength(geom); //คำนวณความยาวของ geometry นั้น ๆ แล้วเก็บในตัวแปร length
        const labelText =
          length > 1000
            ? (length / 1000).toFixed(2) + " km."
            : length.toFixed(0) + " m.";

        return new Style({
          stroke: new Stroke({ color: "#ff0000", width: 3 }),
          text: new Text({
            text: labelText,
            font: "bold 16px sans-serif",
            fill: new Fill({ color: "#000" }),
            stroke: new Stroke({ color: "#fff", width: 3 }),
            placement: "line",
            overflow: true,
          }),
        });
      }

      // ====== วัดพื้นที่ ======
      if (geom.getType() === "Polygon") {
        const area = getArea(geom); //คำนวณพื้นที่
        const labelText =
          area > 1000000
            ? (area / 1000000).toFixed(2) + " sq.km."
            : area.toFixed(0) + " sq.m";

        return new Style({
          fill: new Fill({ color: "rgba(0, 150, 136, 0.3)" }),
          stroke: new Stroke({ color: "#009688", width: 3 }),
          text: new Text({
            text: labelText,
            font: "bold 16px sans-serif",
            fill: new Fill({ color: "#000" }),
            stroke: new Stroke({ color: "#fff", width: 3 }),
            overflow: true,
          }),
        });
      }
    },
  });

  //สร้าง TileLayer จาก OSM
  // baseLayer = new TileLayer({
  //   source: new OSM({
  //     attributions: "", // ลบ Credit OSM
  //   }),
  // });

  /* ================= Base Maps ================= */
  //OSM
  const osmLayer = new TileLayer({
    source: new OSM({ attributions: "" }),
    visible: true,
    properties: { title: "osm" },
  });

  // Satellite (ESRI)
  const satelliteLayer = new TileLayer({
    source: new XYZ({
      url:
        "https://services.arcgisonline.com/ArcGIS/rest/services/" +
        "World_Imagery/MapServer/tile/{z}/{y}/{x}",
    }),
    visible: false,
    properties: { title: "satellite" },
  });

  // Gray map (Carto)
  const grayLayer = new TileLayer({
    source: new XYZ({
      url: "https://{a-d}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
    }),
    visible: false,
    properties: { title: "gray" },
  });

  // locationSource = new VectorSource();
  // locationLayer = new VectorLayer({
  //   source: locationSource,
  // });

  //สร้าง map พร้อม View, interaction, controls
  map = new Map({
    target: mapRef.value,
    layers: [
      osmLayer,
      satelliteLayer,
      grayLayer,
      markerLayer,
      linelayer,
      locationLayer,
    ],
    view: new View({
      center: fromLonLat([mapLongitude.value, mapLatitude.value]),
      zoom: 16,
    }),
    interactions: defaultInteractions(), //ต้ตอบกับแผนที่ได้ เช่น ลาก ซูม หมุน ลือก
    controls: defaultControls().extend([new Zoom()]), // Zoom Control ของ OL
  });

  // คลิกบนแผนที่ → อัพเดท marker + พิกัด
  map.on("click", (evt) => {
    const coordinate = evt.coordinate;
    const lonLat = toLonLat(coordinate);
    mapLatitude.value = lonLat[1];
    mapLongitude.value = lonLat[0];
    updateMarker(coordinate);
  });

  // เพิ่ม cursor เปลี่ยนเป็น pointer เวลา hover pin
  map.on("pointermove", function (evt) {
    const hit = map.hasFeatureAtPixel(evt.pixel);
    map.getTargetElement().style.cursor = hit ? "pointer" : "";
  });

  // Popup Overlay กล่องข้อมูลลอยอยู่บนแผนที่
  popupOverlay = new Overlay({
    element: popupRef.value,
    positioning: "buttom-center",
    stopEvent: false,
    offset: [0, -15],
  });

  map.addOverlay(popupOverlay);

  // singleclick
  map.on("singleclick", function (evt) {
    const feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
      return feature;
    });

    if (feature && feature.get("name")) {
      selectedLocation.value = {
        id: feature.get("id"),
        name: feature.get("name"),
        description: feature.get("default"),
        latitude: feature.get("latitude"),
        longitude: feature.get("longitude"),
      };
      detailDialog.value = true;
    } else {
      detailDialog.value = false;

      const coordinate = evt.coordinate;
      const lonLat = toLonLat(coordinate);

      mapLatitude.value = lonLat[1];
      mapLongitude.value = lonLat[0];

      updateMarker(coordinate);
    }
  });
};

/* -----------------------------
   ปุ่ม Zoom
------------------------------ */
const ZoomIn = () => {
  if (map) {
    const view = map.getView();
    view.setZoom(view.getZoom() + 1);
  }
};
const ZoomOut = () => {
  if (map) {
    const view = map.getView();
    view.setZoom(view.getZoom() - 1);
  }
};
/* -----------------------------
   ปุ่ม Fullscreen
------------------------------ */
const FullScreen = () => {
  const mapDiv = mapRef.value;
  if (!document.fullscreenElement) {
    mapDiv.requestFullscreen().catch((err) => {
      console.log(
        `Error attempting to enable full-screen mode: ${err.message}`,
      );
    });
  } else {
    document.exitFullscreen();
  }
};

/* -----------------------------
   เปลี่ยนแผนที่
------------------------------ */

const switchBaseMap = () => {
  //ตรวจสอบว่า map ถูกสร้างแล้วหรือยัง
  if (!map) return;

  // หา index ปัจจุบัน baseMapOrder = ["OSM", "Satellite", "gray"];
  const currentIndex = baseMapOrder.indexOf(currentBaseMap.value);

  // เลื่อนไปตัวถัดไป (วนกลับ)
  const nextIndex =
    currentIndex === baseMapOrder.length - 1 ? 0 : currentIndex + 1;

  // ดึงชื่อ Base Map ตัวถัดไปจาก array
  const nextBase = baseMapOrder[nextIndex];

  // อัปเดตค่า Base Map ปัจจุบัน (Vue reactive)
  currentBaseMap.value = nextBase;

  // เปิด layer ที่ตรงชื่อ
  // วนลูปทุก layer ที่อยู่ใน map
  map.getLayers().forEach((layer) => {
    // ดึงค่า title ที่กำหนดไว้ตอนสร้าง layer
    const title = layer.get("title");
    if (title) {
      layer.setVisible(title === nextBase);
    }
  });
};

/* -----------------------------
   หมุนขวาทีละ 30°
------------------------------ */

const rotateRight30 = () => {
  if (!map) return; // map ยังไม่ได้ถูกสร้าง → หยุดการทำงาน (ป้องกัน error)
  const view = map.getView(); // ดึง view ปัจจุบันของแผนที่
  const currentRotation = view.getRotation(); // หมุนอยู่ในหน่วย radians ค่าปกติ = 0 rad
  view.setRotation(currentRotation + Math.PI / 6); // หมุนขวา 30°
};

/* -----------------------------
   หมุนช้ายทีละ 30°
------------------------------ */
const rotateLeft30 = () => {
  if (!map) return; // map ยังไม่ได้ถูกสร้าง → หยุดการทำงาน (ป้องกัน error)
  const view = map.getView(); // ดึง view ปัจจุบันของแผนที่
  const currentRotation = view.getRotation(); // หมุนอยู่ในหน่วย radians ค่าปกติ = 0 rad
  view.setRotation(currentRotation - Math.PI / 6); // หมุนช้าย 30°
};

/* -----------------------------
   reset
------------------------------ */
const resetRotation = () => {
  if (!map) return; // map ยังไม่ได้ถูกสร้าง → หยุดการทำงาน (ป้องกัน error)
  const view = map.getView(); // ดึง view ปัจจุบันของแผนที่
  view.setRotation(0); // หมุนไปที่ 0° ค่าปกติ = 0 rad
};

/* -----------------------------
   เพิ่ม ฟังก์ชันวาด LineString
------------------------------ */
const LineString = () => {
  if (!map) return; //ตรวจว่า map มีค่าไหม

  if (draw) {
    //ถ้ามี interaction การวาด (draw)
    map.removeInteraction(draw);
    draw = null;
  }

  //สร้าง interaction สำหรับให้ผู้ใช้วาดรูปทรงบนแผนที่ (Draw interaction ของ OpenLayers)
  draw = new Draw({
    source: lineMarkerSource.value,
    type: "LineString",
    condition: (evt) => evt.originalEvent.type !== "dblclick",
  });

  map.addInteraction(draw);

  //ผูก event listener กับเหตุการณ์ "drawend" ของ draw interaction
  draw.on("drawend", (evt) => {
    const geom = evt.feature.getGeometry(); // get LineString
    const length = getLength(geom);
    distanceResult.value =
      length > 1000
        ? (length / 1000).toFixed(2) + " km."
        : length.toFixed(0) + " m.";

    // เพิ่ม marker จุดเริ่มและจุดปลาย
    const coords = geom.getCoordinates(); //ดึงพิกัดของ LineString มาเป็นอาร์เรย์

    //สร้าง feature จุดเริ่มและจุดจบ:
    const startPoint = new Feature({ geometry: new Point(coords[0]) });
    const endPoint = new Feature({
      geometry: new Point(coords[coords.length - 1]),
    });

    // style marker
    const markerStyle = new Style({
      image: new CircleStyle({
        radius: 5,
        fill: new Fill({ color: "blue" }),
        stroke: new Stroke({ color: "#fff", width: 1 }),
      }),
    });

    //style feature
    startPoint.setStyle(markerStyle);
    endPoint.setStyle(markerStyle);
    lineMarkerSource.value.addFeature(startPoint);
    lineMarkerSource.value.addFeature(endPoint);

    evt.feature.changed();
    map.removeInteraction(draw);
    draw = null;
  });
};
/* -----------------------------
    หาพื้นที่
------------------------------ */
const Area = () => {
  //ตรวจสอบว่า map ถูกสร้างแล้วหรือยัง
  if (!map) return;

  // ลบ interaction เก่าก่อน เพราะ วัดเส้น + วัดพื้นที่ จะซ้อนกัน
  if (draw) {
    map.removeInteraction(draw);
    draw = null;
  }

  // สร้าง Draw Interaction สำหรับ Polygon
  draw = new Draw({
    source: lineMarkerSource.value,
    type: "Polygon",
  });

  //เพิ่ม interaction ลงในแผนที่
  map.addInteraction(draw);

  //สั่ง event เมื่อวาดเสร็จ
  draw.on("drawend", (evt) => {
    const geom = evt.feature.getGeometry(); //ดึง Geometry ที่วาดได้
    const area = getArea(geom); //คำนวณพื้นที่

    // แปลงหน่วย + แสดงผล
    console.log(
      "พื้นที่:",
      //ถ้าเกิน 1,000,000 m² → แปลงเป็น ตร.กม.
      // 1,000 เมตร = 1 กิโลเมตร
      // 1,000 เมตร x 1,000 เมตร = 1,000,000 ตรม
      // 1 กิโลเมตร x 1 กิโลเมตร = 1 ตร.กม
      area > 1000000
        ? (area / 1000000).toFixed(2) + " sq.km."
        : area.toFixed(0) + " sq.m.",
    );

    evt.feature.changed(); // บังคับ redraw label
    map.removeInteraction(draw); // ปิดโหมดวาดเมื่อเสร็จ
    draw = null;
  });
};

/* -----------------------------
   เพิ่ม ฟังก์ชันลบ ClearLines
------------------------------ */
const ClearLines = () => {
  if (!lineMarkerSource.value) return;
  lineMarkerSource.value.clear();

  if (draw) {
    map.removeInteraction(draw);
    draw = null;
  }
};

/* -----------------------------
   Cleanup เมื่อ component ถูก destroy → ปล่อย memory ของ map
------------------------------ */
onBeforeMount(() => {
  if (map) {
    map.setTarget(null);
    map = null;
  }
});
</script>
<style scoped></style>
