<template>
  <div class="container mt-5">
    <div class="card p-4 shadow col-md-6 mx-auto">

  <h3 class="text-center mb-4">Student Registration</h3>

  <form @submit.prevent="handleRegister">

    <input v-model="name" class="form-control mb-3" placeholder="Full Name" required />

    <input v-model="email" type="email" class="form-control mb-3" placeholder="Email" required />

    <input v-model="password" type="password" class="form-control mb-3" placeholder="Password" required />

    <!-- Degree -->
    <select v-model="degree" class="form-select mb-3" required>
      <option disabled value="">Select Degree</option>
      <option>B.Tech / B.E</option>
      <option>B.Sc</option>
      <option>B.Com</option>
      <option>BBA</option>
      <option>BA</option>
      <option>MBA</option>
      <option>M.Sc</option>
      <option>M.Tech / M.E</option>
      <option>MA</option>
      <option>MBBS</option>
      <option>Other</option>
    </select>

    <!-- Field / Major -->
    <input v-model="branch" class="form-control mb-3" placeholder="Major / Field of Study" required />

    <!-- CGPA -->
    <input v-model="cgpa" type="number" step="0.1" class="form-control mb-3" placeholder="CGPA / Percentage" required />

    <!-- Year -->
    <select v-model="year" class="form-control mb-3" required>
      <option value="">Select Year</option>

      <option value="1">1 (First Year)</option>
      <option value="2">2 (Second Year)</option>

      <option value="3">3 (Third Year)</option>
      <option value="3f">3 (Final Year)</option>

      <option value="4">4 (Fourth Year)</option>
      <option value="4f">4 (Final Year)</option>

      <option value="5f">5 (Final Year)</option>
    </select>

    <!-- University -->
    <input v-model="college" class="form-control mb-4" placeholder="University / College Name" required />

    <button class="btn btn-primary w-100">
      Register
    </button>

  </form>

</div>

  </div>
</template>

<script>
import api from "../services/api"

export default {

  data(){
    return{
      name:"",
      email:"",
      password:"",
      degree:"",
      branch:"",
      cgpa:"",
      year:"",
      college:""
    }
  },

  methods:{

    async handleRegister(){

      try{

        await api.post("/auth/register/student",{
          name:this.name,
          email:this.email,
          password:this.password,
          branch:this.branch,
          cgpa:this.cgpa,
          year:this.year
        })

        alert("Student Registered Successfully")

        this.$router.push("/")

      }catch(err){

        alert(err.response?.data?.message || "Registration failed")

      }

    }

  }

}
</script>
