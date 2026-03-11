<template>
<div class="container mt-4">

<h2>Create Placement Drive</h2>

<form @submit.prevent="createDrive">

<div class="mb-3">
<label class="form-label">Job Title</label>
<input v-model="form.title" class="form-control" required>
</div>

<div class="mb-3">
<label class="form-label">Job Description</label>
<textarea v-model="form.job_description" class="form-control"></textarea>
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

<div class="mb-3">
<label class="form-label">Eligible Year</label>

<select v-model="form.eligible_year" class="form-control">

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
<label class="form-label">Minimum CGPA</label>
<input v-model="form.min_cgpa" type="number" class="form-control">
</div>

<div class="mb-3">
<label class="form-label">CTC / Stipend</label>
<input v-model="form.ctc" class="form-control" placeholder="e.g. 8 LPA or 25,000/month">
</div>

<div class="mb-3">
<label class="form-label">Application Deadline</label>
<input v-model="form.deadline" type="date" class="form-control">
</div>

<button class="btn btn-primary">Create Drive</button>

</form>

<hr>

<h3>Your Placement Drives</h3>

<table class="table">
<thead>
<tr>
<th>Title</th>
<th>Status</th>
<th>Applicants</th>
</tr>
</thead>

<tbody>
<tr v-for="d in drives" :key="d.id">
<td>{{ d.title }}</td>
<td>{{ d.status }}</td>
<td>{{ d.applicants }}</td>
</tr>
</tbody>
</table>

</div>
</template>

<script>
import api from "../services/api"

export default {

data() {
return {
drives: [],
form: {
job_title: "",
job_description: "",
eligible_branch: "",
eligible_year: "",
min_cgpa: "",
ctc: "",
deadline: ""
}
}
},

async mounted() {
const res = await api.get("/company/dashboard")
this.drives = res.data
},

methods: {

async createDrive() {

await api.post("/company/create-drive", this.form)

alert("Drive created")

location.reload()

}

}

}
</script>