<template>
  <v-footer class="app-bar" height="40" app>
    <a
      v-for="item in items"
      :key="item.title"
      :href="item.href"
      :title="item.title"
      class="d-inline-block mx-2 social-link"
      rel="noopener noreferrer"
      target="_blank"
    >
      <v-icon
        :icon="item.icon"
        :size="item.icon === '$vuetify' ? 24 : 16"
      />
    </a>

    <div
      class="text-caption text-disabled"
      style="position: absolute; right: 16px;"
    >
      &copy; 2025-{{ (new Date()).getFullYear() }} <span class="d-none d-sm-inline-block">Project, VUE</span>
      —
      <a
        class="text-decoration-none on-surface"
        href="https://phichasignon-code.web.app/"
        rel="noopener noreferrer"
        target="_blank"
      >
        pHicha.Sign.On
      </a>
    </div>
  </v-footer>
</template>

<script setup>
  const items = [
    {
      title: 'คู่มือ',
      icon: `mdi-file-pdf-box`,
      href: '', // ลิงค์มือ
    },
  ]
</script>

<style scoped lang="sass">
  .social-link :deep(.v-icon)
    color: rgba(var(--v-theme-on-background), var(--v-disabled-opacity))
    text-decoration: none
    transition: .2s ease-in-out

    &:hover
      color: rgba(25, 118, 210, 1)
</style>
