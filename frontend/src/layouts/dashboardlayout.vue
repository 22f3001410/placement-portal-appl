<template>
  <div class="layout">
    <div class="sidebar">
      <h4 class="logo">Placement Cell Portal</h4>

      <div class="menu">
        <div
          v-for="item in menuItems"
          :key="item.label"
          class="menu-item"
          @click="scrollTo(item.ref)"
        >
          {{ item.label }}
        </div>

        <div class="menu-item logout" @click="logout">
          Logout
        </div>
      </div>
    </div>

    <div class="main">
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  props: ["menuItems"],
  methods: {
    scrollTo(ref) {
      if (!ref) return
      const el = document.getElementById(ref)
      if (el) el.scrollIntoView({ behavior: "smooth" })
    },
    logout() {
      if (confirm("Are you sure you want to logout?")) {
        localStorage.removeItem("token")
        localStorage.removeItem("role")
        this.$router.push("/")
      }
    }
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
  background: #f4f6f9;
}

.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #1e1e2f, #27293d);
  color: white;
  padding: 20px;
}

.logo {
  margin-bottom: 30px;
  font-weight: 600;
}

.menu-item {
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  color: #c7c7d3;
  transition: 0.3s;
}

.menu-item:hover {
  background: #3a3f58;
  color: white;
}

.logout {
  margin-top: 30px;
  color: #ff6b6b;
}

.main {
  flex: 1;
  padding: 30px;
}
</style>