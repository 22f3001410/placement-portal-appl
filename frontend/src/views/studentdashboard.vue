<template>
  <DashboardLayout :menuItems="menu">
    <div>

      <h3>Edit Profile</h3>

      <div id="profile" class="card p-3 mb-4">
        <div class="mb-2">
          <input v-model="profile.name" class="form-control" placeholder="Name">
        </div>

        <div class="mb-2">
          <input v-model="profile.branch" class="form-control" placeholder="Branch">
        </div>

        <div class="mb-2">
          <input v-model="profile.cgpa" class="form-control" placeholder="CGPA">
        </div>

        <div class="mb-2">
          <input v-model="profile.year" class="form-control" placeholder="Year">
        </div>

        <button class="btn btn-primary" @click="updateProfile">
          Update Profile
        </button>
      </div>

      <div class="card p-3 mb-4">

      <h5>Upload Resume</h5>

      <input type="file" @change="handleResume">

      <button class="btn btn-success mt-2" @click="uploadResume">
      Upload Resume
      </button>

      </div>

      <h2 class="mb-4">Student Dashboard</h2>

      <!-- Search -->
      <div class="card shadow-sm p-3 mb-4">
        <div class="d-flex gap-2">
          <input v-model="driveSearch"
                 class="form-control"
                 placeholder="Search drive by title" />
          <button class="btn btn-primary"
                  @click="searchDrives">
            Search
          </button>
        </div>
      </div>

      <!-- Available Drives -->
      <div id="drives" class="card shadow-sm p-4 mb-4">
        <h5 class="mb-3">Available Drives</h5>

        <table class="table table-hover table-striped">

          <thead>
            <tr>
              <th>ID</th>
              <th>Company</th>
              <th>Title</th>
              <th>CTC</th>
              <th>Min CGPA</th>
              <th></th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="drive in drives" :key="drive.id">
              <td>{{ drive.id }}</td>
              <td>{{ drive.company_name }}</td>
              <td>{{ drive.title }}</td>
              <td>{{ drive.ctc }}</td>
              <td>{{ drive.min_cgpa }}</td>

              <td>
                <button
                  class="btn btn-sm btn-primary"
                  :disabled="applications && applications.some(a => a.drive_id === drive.id)"
                  @click="apply(drive.id)"
                >
                  Apply
                </button>
              </td>
            </tr>
          </tbody>

        </table>
      </div>

      <!-- My Applications -->
      <div id="applications" class="card shadow-sm p-4">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5>My Applications</h5>
          <button class="btn btn-outline-dark btn-sm"
                  @click="exportData">
            Export CSV
          </button>
        </div>

        <table class="table table-hover table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Drive ID</th>
              <th>Status</th>
              <th>Interview</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.id">
              <td>{{ app.id }}</td>
              <td>{{ app.drive_id }}</td>
              
              <td>
                <span v-if="app.status === 'Selected'" class="badge bg-success">
                Selected
                </span>

                <span v-else-if="app.status === 'Rejected'" class="badge bg-danger">
                Rejected
                </span>

                <span v-else-if="app.status === 'Shortlisted'" class="badge bg-info">
                Shortlisted
                </span>

                <span v-else-if="app.status === 'Interview Scheduled'" class="badge bg-primary">
                Interview Scheduled
                </span>

                <span v-else class="badge bg-warning text-dark">
                Applied
                </span>
              </td>
              <td>
                <span v-if="app.status === 'Interview Scheduled' || app.status === 'Shortlisted'">
                  {{ app.interview_date 
                    ? new Date(app.interview_date).toLocaleDateString('en-GB') + " " + new Date(app.interview_date).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})
                    : "Not Scheduled" }}
                </span>
                <span v-else>Not Scheduled</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </DashboardLayout>
</template>

<script>
import api from "../services/api"
import DashboardLayout from "../layouts/DashboardLayout.vue"

export default {
  components: { DashboardLayout },

  data() {
    return {
    student_id: null,
      menu: [
        { label: "Dashboard",        ref: "profile" },
        { label: "Available Drives", ref: "drives" },
        { label: "My Applications",  ref: "applications" }
      ],

      drives: [],
      applications: [],
      driveSearch: "",

      profile: {
        name: "",
        branch: "",
        cgpa: "",
        year: ""
      }
    }
  },

  async mounted() {
    await this.loadDrives()
    await this.loadApplications()
    await this.loadProfile()
  },

  methods: {

    async loadProfile() {
      const res = await api.get("/student/profile")
      this.profile = res.data
      this.student_id = res.data.id  
    },

    async updateProfile() {
      try {
        await api.put("/student/update-profile", this.profile)
        alert("Profile updated successfully")
      } catch {
        alert("Update failed")
      }
    },

    handleResume(event){
      this.resumeFile = event.target.files[0]
    },

    async uploadResume() {
      if (!this.resumeFile) {
        alert("Please select a file first")
        return
      }

      const formData = new FormData()
      formData.append("resume", this.resumeFile)

      try {
        await api.post("/student/upload-resume", formData)  // ✅ remove headers override
        alert("Resume uploaded successfully")
      } catch(err) {
        console.error(err.response?.data)
        alert(err.response?.data?.message || "Upload failed")
      }
    },
    
    async loadDrives() {
      try {
        const res = await api.get("/student/dashboard")
        this.drives = res.data
      } catch (err) {

        if (err.response?.status === 401) {
          alert("Session expired. Please login again.")
          localStorage.removeItem("token")
          this.$router.push("/login")
          return
        }

        alert("Failed to load drives")
      }
    },

    async loadApplications() {
      try {
        const res = await api.get("/student/applications")
        this.applications = res.data
      } catch (err) {

        if (err.response?.status === 401) {
          alert("Session expired. Please login again.")
          localStorage.removeItem("token")
          this.$router.push("/login")
          return
        }

        alert("Failed to load applications")
      }
    },
    async searchDrives() {
      try {
        const res = await api.get(`/student/search-drives?title=${this.driveSearch}`)
        this.drives = res.data
      } catch {
        alert("Search failed")
      }
    },

    async apply(id) {
      try {
        const res = await api.post(`/student/apply/${id}`)
        alert(res.data.message)
        this.loadApplications()
      } catch (err) {
        alert(err.response?.data?.message || "Apply failed")
      }
    },

    async exportData() {
      try {
        const res = await api.get("/student/export")
        const taskId = res.data.task_id
        alert("Export started! Please wait...")

        let downloaded = false  

        const interval = setInterval(async () => {
          const status = await api.get(`/student/task-status/${taskId}`)
          console.log("Task status:", status.data)

          if (status.data.state === "SUCCESS" && !downloaded) {
            downloaded = true  
            clearInterval(interval)
            window.open(`http://localhost:5000/student/download-export/${this.student_id}`, "_blank")
            alert("✅ Export complete! Your CSV has been downloaded.")
          }

          if (status.data.state === "FAILURE") {
            clearInterval(interval)
            alert("Export failed. Please try again.")
          }

        }, 2000)

      } catch(err) {
        console.error(err)
        alert("Export failed")
      }
    }
  }
}
</script>