<template>
  <DashboardLayout :menuItems="menu">

    <div>

      <h2 class="mb-4">Company Dashboard</h2>

      <!-- Company Info -->
      <div id="company-info" class="card shadow-sm p-3 mb-4">
        <h5>Company</h5>
        <p class="mb-0">{{ company }}</p>
      </div>


      <!-- Create Drive -->
      <div id="create-drive" class="card shadow-sm p-4 mb-4">
        <h5 class="mb-3">Create Placement Drive</h5>

        <form @submit.prevent="createDrive">

          <div class="row g-3">

            <div class="col-md-6">
              <label class="form-label">Job Title</label>
              <input v-model="form.job_title" class="form-control" required>
            </div>

            <div class="col-md-6">
              <label class="form-label">Eligible Branch</label>

              <select v-model="form.eligible_branch" class="form-select">
                <option value="All">All</option>
                <option value="Computer Science">Computer Science</option>
                <option value="Electronics">Electronics</option>
                <option value="Mechanical">Mechanical</option>
                <option value="Civil">Civil</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div v-if="form.eligible_branch === 'Other'" class="col-md-6">
              <label class="form-label">Specify Branch</label>

              <input
                v-model="form.other_branch"
                class="form-control"
                placeholder="Enter branch name"
              >
            </div>

            <div class="col-md-6">
              <label class="form-label">Minimum CGPA</label>
              <input v-model="form.min_cgpa" type="number" step="0.1" class="form-control">
            </div>

            <div class="col-md-6">
              <label class="form-label">Eligible Year</label>

              <select v-model="form.eligible_year" class="form-select">

                <option value="Any">Any Year</option>

                <option value="1">1 (First Year)</option>
                <option value="2">2 (Second Year)</option>

                <option value="3">3 (Third Year)</option>
                <option value="3f">3 (Final Year)</option>

                <option value="4">4 (Fourth Year)</option>
                <option value="4f">4 (Final Year)</option>

                <option value="5f">5 (Final Year)</option>

              </select>

            </div>

            <div class="mb-3">
              <label class="form-label">CTC / Stipend</label>
              <input v-model="form.ctc" class="form-control" placeholder="e.g. 8 LPA or 25000/month">
            </div>

            <div class="col-md-6">
              <label class="form-label">Deadline</label>
              <input v-model="form.deadline" type="date" class="form-control" required>
            </div>

            <div class="col-12">
              <label class="form-label">Job Description</label>
              <textarea v-model="form.job_description"
                        class="form-control"
                        rows="3"></textarea>
            </div>

          </div>

          <button class="btn btn-primary mt-3">
            Create Drive
          </button>

        </form>

      </div>


      <!-- Drives Table -->
      <div class="card shadow-sm p-4">

        <h5 class="mb-3">Your Drives</h5>

        <table class="table table-striped">

          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Applicants</th>
              <th></th>
            </tr>
          </thead>

          <tbody>

            <tr v-for="d in drives" :key="d.id">

              <td>{{ d.id }}</td>
              <td>{{ d.title }}</td>
              <td>{{ d.status }}</td>
              <td>{{ d.applicants }}</td>

              <td>

                <button class="btn btn-sm btn-secondary"
                        @click="loadApplications(d.id)">
                  View Applicants
                </button>

              </td>

            </tr>

          </tbody>

        </table>

      </div>


      <!-- Applicants Section -->
      <div id="applicants" v-if="applications" class="card shadow-sm p-4 mt-4">
        <h5 class="mb-3">Applicants</h5>

        <table class="table table-hover">

          <thead>
            <tr>
              <th>ID</th>
              <th>Student Name</th>
              <th>Status</th>
              <th>Update</th>
              <th>Interview</th>
              <th>Resume</th>
            </tr>
          </thead>

          <tbody>

            <tr v-for="a in applications" :key="a.id">

              <td>{{ a.id }}</td>
              <td>{{ a.student }}</td>

              <td>
                <span v-if="a.status === 'Selected'" class="badge bg-success">Selected</span>
                <span v-else-if="a.status === 'Rejected'" class="badge bg-danger">Rejected</span>
                <span v-else-if="a.status === 'Shortlisted'" class="badge bg-info">Shortlisted</span>
                <span v-else-if="a.status === 'Interview Scheduled'" class="badge bg-primary">Interview Scheduled</span>
                <span v-else class="badge bg-warning text-dark">Applied</span>
              </td>

              <td>

                <select v-model="a.status"
                        class="form-select form-select-sm"
                        @change="updateStatus(a)">

                  <option>Applied</option>
                  <option>Shortlisted</option>
                  <option>Selected</option>
                  <option>Rejected</option>

                </select>

              </td>

              <td class="d-flex gap-2">

              <input
              type="datetime-local"
              v-model="a.interview_date"
              class="form-control form-control-sm"
              >

              <button
              class="btn btn-sm btn-primary"
              @click="scheduleInterview(a)"
              >
              Save
              </button>

              </td>

              <td>
                <a
                  v-if="a.resume"
                  :href="'http://localhost:5000/company/resume/' + a.resume"
                  target="_blank"
                  class="btn btn-sm btn-outline-primary"
                >
                  View
                </a>

                <span v-else class="text-muted">
                  No Resume
                </span>
              </td>

            </tr>

            <tr v-if="applications.length === 0">
            <td colspan="5" class="text-center">No applicants yet</td>
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

  components:{ DashboardLayout },

  data(){
    return{

      menu: [
        { label: "Dashboard",    ref: "company-info" },
        { label: "Create Drive", ref: "create-drive" },
        { label: "Applicants",   ref: "applicants" }
      ],

      company:"",

      drives:[],

      applications:[],

      form:{
        job_title:"",
        job_description:"",
        eligible_branch:"",
        other_branch:"",
        min_cgpa:"",
        eligible_year:"",
        ctc:"",
        deadline:""
      }

    }
  },

  async mounted(){

    await this.loadDashboard()

  },

  methods:{

    async loadDashboard(){

      const res = await api.get("/company/dashboard")

      this.company = res.data.company

      this.drives = res.data.drives

    },


    async createDrive() {
      if (this.form.eligible_branch === "Other") {
        this.form.eligible_branch = this.form.other_branch
      }

      try {
        await api.post("/company/create-drive", this.form)
        alert("Drive created. Waiting for admin approval.")
        this.loadDashboard()
      } catch (error) {
        if (error.response?.status === 401) {
          alert("Session expired. Please log in again.")
          this.$router.push('/login') // adjust to your login route
        } else {
          alert("Something went wrong. Please try again.")
          console.error(error)
        }
      }
    },


    async loadApplications(driveId) {
      const res = await api.get("/company/applications")
      this.applications = res.data
        .filter(a => a.drive_id === driveId)
        .map(a => ({
          ...a,
          interview_date: a.interview_date 
            ? a.interview_date.slice(0, 16)  // ✅ format for datetime-local input
            : ""
        }))
    },


    async updateStatus(app){

      try{

        await api.put(`/company/application/${app.id}/update`,{
          status: app.status
        })

        alert("Status updated")

      }
      catch{

        alert("Update failed")

      }

    },

    async scheduleInterview(app){

      try{

        await api.put(`/company/application/${app.id}/schedule`,{
          interview_date: app.interview_date
        })

        alert("Interview scheduled")

      }
      catch{

        alert("Scheduling failed")

      }

    }

  }

}
</script>