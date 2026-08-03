<template>
  <div class="admin-layout">
    <nav class="sidebar">
      <router-link to="/admin/info">System Info</router-link>
      <router-link to="/admin/logs">Logs</router-link>
      <router-link to="/admin/settings">Settings</router-link>
    </nav>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 200px;
  padding: 20px;
  background: #f0f0f0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.content {
  flex: 1;
  padding: 20px;
}
.router-link-active {
  font-weight: bold;
}
</style>
