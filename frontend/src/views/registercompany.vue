<template>
  <div class="container mt-5">
    <h3>Register Company</h3>

    <form @submit.prevent="handleRegister">
      <input
        v-model="company_name"
        placeholder="Company Name"
        class="form-control mb-2"
        required
      />

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="form-control mb-2"
        required
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="form-control mb-3"
        required
      />

      <input v-model="hr_contact" 
      class="form-control mb-3" 
      placeholder="HR Contact Number" 
      required 
      /> 
      
      <input v-model="website" 
      class="form-control mb-4" 
      placeholder="Company Website" 
      />

      <button type="submit" class="btn btn-primary w-100">
        Register
      </button>
    </form>
  </div>
</template>

<script>
import api from "../services/api"

export default {
  data() {
    return {
      company_name: "",
      email: "",
      password: ""
    }
  },

  methods: {
    async handleRegister() {
      console.log("Company POST sending")

      try {
        const res = await api.post("/auth/register/company", {
          company_name: this.company_name,
          email: this.email,
          password: this.password,
          hr_contact: this.hr_contact,
          website: this.website 
        })

        alert(res.data.message)
      } catch (err) {
        alert(err.response?.data?.message || "Registration failed")
      }
    }
  }
}
</script>