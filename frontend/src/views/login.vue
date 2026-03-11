<template>
  <div class="container mt-5">
    <div class="card p-4 shadow col-md-4 mx-auto">
      <h3 class="text-center mb-3">Login</h3>

      <form @submit.prevent="handleLogin">
        <input v-model="email" type="email" class="form-control mb-2" placeholder="Email" required />
        <input v-model="password" type="password" class="form-control mb-3" placeholder="Password" required />
        <button class="btn btn-primary w-100">Login</button>
      </form>

      <div class="text-center mt-3">
        <router-link to="/register-student">Register as Student</router-link><br>
        <router-link to="/register-company">Register as Company</router-link>
      </div>

      <p class="text-danger mt-2">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import api from "../services/api"

export default {
  data() {
    return {
      email: "",
      password: "",
      error: "",
      loading: false
    }
  },

  methods: {
    async handleLogin() {
      this.error = ""
      this.loading = true

      try {
        const res = await api.post("/auth/login", {
          email: this.email,
          password: this.password
        })

        const token = res.data.access_token
        localStorage.setItem("token", token)

        const payload = JSON.parse(atob(token.split(".")[1]))
        const role = payload.role

        localStorage.setItem("role", role)

        if (role === "admin") {
          this.$router.push("/admin")
        } else if (role === "company") {
          this.$router.push("/company")
        } else if (role === "student") {
          this.$router.push("/student")
        } else {
          this.error = "Invalid role"
        }

      } catch (err) {
        this.error = err.response?.data?.message || "Login failed"
      } finally {
        this.loading = false
      }
    }
  }
}
</script>